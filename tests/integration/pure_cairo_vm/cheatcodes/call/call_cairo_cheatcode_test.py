from pathlib import Path

import pytest

from tests.integration.conftest import (
    CreateProtostarProjectFixture,
    assert_cairo_test_cases,
)
from tests.integration._conftest import ProtostarFixture
from tests.integration.pure_cairo_vm.conftest import (
    CONTRACTS_PATH,
)

TEST_PATH = Path(__file__).parent


@pytest.fixture(name="protostar")
def protostar_fixture(create_protostar_project: CreateProtostarProjectFixture):
    with create_protostar_project() as protostar:
        yield protostar


async def test_call_pipeline(protostar: ProtostarFixture):
    protostar.create_contracts(
        {
            "basic": CONTRACTS_PATH / "basic_contract.cairo",
            "proxy": CONTRACTS_PATH / "proxy_for_basic_contract.cairo",
        }
    )
    testing_summary = await protostar.run_test_runner(
        TEST_PATH / "call_test.cairo",
        cairo_test_runner=True,
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[
            "test_call_simple",
            "test_call_not_mutating_state",
            "test_call_named_args",
            "test_call_with_proxy_simple",
            "test_call_with_proxy_named_args_success",
            "test_call_unknown_fail",
        ],
        expected_broken_test_cases_names=[
            "test_call_named_args_invalid_fail",
            "test_call_with_proxy_named_args_fail",
        ],
    )
