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


@pytest.fixture(autouse=True, name="protostar")
def protostar_fixture(create_protostar_project: CreateProtostarProjectFixture):
    with create_protostar_project() as protostar:
        yield protostar


async def test_deploy_contract(protostar: ProtostarFixture):
    protostar.create_contracts(
        {
            "basic": CONTRACTS_PATH / "basic_contract.cairo",
            "basic_with_constructor": CONTRACTS_PATH / "basic_with_constructor.cairo",
        }
    )

    testing_summary = await protostar.run_test_runner(
        TEST_PATH / "deploy_contract_test.cairo",
        cairo_test_runner=True,
    )

    assert_cairo_test_cases(
        testing_summary,
        expected_passed_test_cases_names=[
            "test_deploying_contract",
            "test_deploying_contract_by_name",
            "test_deploying_contract_with_constructor",
        ],
    )
