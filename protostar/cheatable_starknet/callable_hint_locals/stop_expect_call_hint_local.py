from typing import Callable

from starknet_py.utils.data_transformer.data_transformer import CairoData

from protostar.cheatable_starknet.controllers.expect_call_controller import (
    ExpectCallController,
    CallData,
)
from protostar.cheatable_starknet.callable_hint_locals.callable_hint_local import (
    CallableHintLocal,
)

from protostar.starknet import RawAddress


class StopExpectCallHintLocal(CallableHintLocal):
    def __init__(self, controller: ExpectCallController):
        self._controller = controller

    @property
    def name(self) -> str:
        return "stop_expect_call"

    def _build(self) -> Callable:
        return self.stop_expect_call

    def stop_expect_call(self, address: RawAddress, fn_name: str, calldata: CairoData):
        self._controller.remove_expected_call(
            expected_call=CallData(address=address, fn_name=fn_name, calldata=calldata)
        )
