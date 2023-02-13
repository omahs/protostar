from dataclasses import dataclass
from typing import TYPE_CHECKING

from protostar.starknet import CairoData, RawAddress

if TYPE_CHECKING:
    from protostar.testing import Hook
    from protostar.cairo_testing import CairoTestExecutionState
    from protostar.cheatable_starknet.cheatables.cheatable_cached_state import (
        CheatableCachedState,
    )


@dataclass
class CallData:
    address: RawAddress
    fn_name: str
    calldata: CairoData


class ExpectCallController:
    def __init__(
        self,
        test_finish_hook: "Hook",
        test_execution_state: "CairoTestExecutionState",
        cheatable_state: "CheatableCachedState",
    ) -> None:
        self._test_execution_state = test_execution_state
        self._test_finish_hook = test_finish_hook
        self._cheatable_state = cheatable_state
        self._test_finish_hook.on(self.assert_no_expected_calls_left)

    def add_expected_call(self, expected_call: CallData):
        pass

    def remove_expected_call(self, expected_call: CallData):
        pass

    def assert_no_expected_calls_left(self):
        pass
