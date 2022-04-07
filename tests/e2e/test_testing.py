import shutil
from black import Path
import pytest

@pytest.fixture(name="test_file")
def complex_protostar():
    fixtures_path = Path() / "tests" /"e2e" / "fixtures"


@pytest.mark.usefixtures("init")
def test_basic_contract(protostar):
    result = protostar(["test", "tests"])
    assert "1 passed" in result


@pytest.mark.usefixtures("init")
def test_complex(protostar, copy_fixture):
    copy_fixture("basic_with_constructor.cairo", "./src") 
    copy_fixture("proxy_contract.cairo", "./src") 
    copy_fixture("test_proxy.cairo", "./tests") 

    result = protostar(["test", "tests"])
    assert "1 passed" in result
    
    
    
    
    
    
    
    