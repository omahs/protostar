# pylint: disable=no-member
import gzip
import time
from starkware.cairo.lang.tracer.third_party.profile_pb2 import Profile
from protostar.profiler.transaction_profiler import TransactionProfile


class StringIDGenerator:
    def __init__(self):
        self.string_table = [""]
        self.string_ids = {"": 0}

    def get(self, val: str) -> int:
        if val not in self.string_ids:
            self.string_ids[val] = len(self.string_table)
            self.string_table.append(val)
        return self.string_ids[val]


def to_protobuf(profile_obj: TransactionProfile) -> Profile:
    profile = Profile()
    id_generator = StringIDGenerator()
    non_empty_samples = {k: v for k, v in profile_obj.samples.items() if v != []}

    profile.time_nanos = int(time.time() * 10**9)  # type: ignore
    sample_types_names = list(non_empty_samples.keys())

    # Move steps at the end of the list
    sample_types_names.remove("steps")
    sample_types_names.append("steps")

    for name in sample_types_names:
        sample_tp = profile.sample_type.add()  # type: ignore
        sample_tp.type = id_generator.get(name)
        sample_tp.unit = id_generator.get(name)

    for function in profile_obj.functions:
        func = profile.function.add()  # type: ignore
        func.id = id_generator.get(function.id)
        func.system_name = func.name = id_generator.get(function.id)
        func.filename = id_generator.get(function.filename)
        func.start_line = function.start_line

    for inst in profile_obj.instructions:
        location = profile.location.add()  # type: ignore
        location.id = inst.id
        location.address = inst.pc
        location.is_folded = False
        line = location.line.add()
        line.function_id = id_generator.get(inst.function.id)
        line.line = inst.line

    for name, samples in non_empty_samples.items():
        for smp in samples:
            sample = profile.sample.add()  # type: ignore
            for instr in smp.callstack:
                sample.location_id.append(instr.id)
            idx = sample_types_names.index(name)
            for i in range(len(sample_types_names)):
                if i == idx:
                    sample.value.append(smp.value)
                else:
                    sample.value.append(0)

    for val in id_generator.string_table:
        profile.string_table.append(val)  # type: ignore

    return profile


def serialize(profile: Profile) -> bytes:
    data = profile.SerializeToString()  # type: ignore
    return gzip.compress(data)
