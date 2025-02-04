from dataclasses import dataclass

from starknet_py.net.signer import BaseSigner
from starknet_py.net import AccountClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.client_models import Call as SNCall
from starknet_py.net.client_errors import ClientError

from protostar.starknet import Address, TransactionHash, Selector, CairoData
from protostar.protostar_exception import ProtostarException
from protostar.starknet_gateway.core import PreparedInvokeTransaction
from protostar.starknet_gateway.multicall import (
    SignedMulticallTransaction,
    MulticallAccountManagerProtocol,
    UnsignedMulticallTransaction,
)

from .type import Fee
from .account_tx_version_detector import AccountTxVersionDetector
from .gateway_facade import GatewayFacade


@dataclass
class Account:
    address: Address
    signer: BaseSigner


class AccountManager(MulticallAccountManagerProtocol):
    def __init__(
        self,
        account: Account,
        gateway_url: str,
        client: GatewayFacade,
    ):
        self._account = account
        gateway_client = GatewayClient(gateway_url)
        self._account_tx_version_detector = AccountTxVersionDetector(gateway_client)
        self._client = client
        self._account_client = AccountClient(
            address=int(account.address),
            client=gateway_client,
            signer=account.signer,
            supported_tx_version=1,
        )

    def get_account_address(self):
        return Address(self._account_client.address)

    async def sign_multicall_transaction(
        self, unsigned_transaction: UnsignedMulticallTransaction
    ) -> SignedMulticallTransaction:
        await self._ensure_account_is_valid()
        try:
            tx = await self._account_client.sign_invoke_transaction(
                calls=[
                    SNCall(
                        to_addr=int(call.address),
                        selector=int(call.selector),
                        calldata=call.calldata,
                    )
                    for call in unsigned_transaction.calls
                ],
                max_fee=unsigned_transaction.max_fee
                if isinstance(unsigned_transaction.max_fee, int)
                else None,
                auto_estimate=unsigned_transaction.max_fee == "auto",
                version=1,
            )
            return SignedMulticallTransaction(
                contract_address=Address(tx.contract_address),
                calldata=tx.calldata,
                max_fee=tx.max_fee,
                nonce=tx.nonce,
                signature=tx.signature,
            )
        except ClientError as ex:
            raise SigningException(message=ex.message) from ex

    async def prepare_invoke_transaction(
        self,
        address: Address,
        selector: Selector,
        calldata: CairoData,
        max_fee: Fee,
    ) -> PreparedInvokeTransaction:
        await self._ensure_account_is_valid()
        try:
            signed_tx = await self._account_client.sign_invoke_transaction(
                calls=SNCall(
                    to_addr=int(address),
                    selector=int(selector),
                    calldata=calldata,
                ),
                max_fee=max_fee if isinstance(max_fee, int) else None,
                auto_estimate=max_fee == "auto",
                version=1,
            )
            return PreparedInvokeTransaction(
                account_address=Address(signed_tx.contract_address),
                account_execute_calldata=signed_tx.calldata,
                max_fee=signed_tx.max_fee,
                nonce=signed_tx.nonce,
                signature=signed_tx.signature,
            )
        except ClientError as ex:
            raise SigningException(message=ex.message) from ex

    async def _ensure_account_is_valid(self):
        actual_account_version = await self._account_tx_version_detector.detect(
            self._account.address
        )
        if actual_account_version != self._account_client.supported_tx_version:
            raise ProtostarException(
                f"Unsupported account version: {actual_account_version}"
            )

    async def execute(
        self, prepared_invoke_tx: PreparedInvokeTransaction
    ) -> TransactionHash:
        return await self._client.send_prepared_invoke_tx(prepared_invoke_tx)


class UnsupportedAccountVersionException(ProtostarException):
    def __init__(self, version: int):
        super().__init__(message=f"Unsupported account version: {version}")


class SigningException(ProtostarException):
    pass
