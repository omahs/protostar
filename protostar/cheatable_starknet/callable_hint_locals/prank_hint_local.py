from typing import Callable

from protostar.cheatable_starknet.controllers import ContractsController
from protostar.starknet import Address
from protostar.cheatable_starknet.callable_hint_locals.callable_hint_local import (
    CallableHintLocal,
)


class PrankHintLocal(CallableHintLocal):
    def __init__(self, contracts_controller: ContractsController):
        self._contracts_controller = contracts_controller

    @property
    def name(self) -> str:
        return "prank"

    def _build(self) -> Callable:
        return self.prank

    def prank(self, caller_address: int, target_address: int):
        valid_target_address = Address.from_user_input(target_address)
        self._contracts_controller.prank(
            caller_address=Address.from_user_input(caller_address),
            target_address=valid_target_address,
        )
        return lambda: self._contracts_controller.cancel_prank(
            target_address=valid_target_address
        )
