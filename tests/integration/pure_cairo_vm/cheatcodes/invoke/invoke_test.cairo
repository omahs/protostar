from starkware.cairo.common.math import assert_not_zero

func test_invoke_without_transformation() {
    alloc_locals;
    local deployed_contract_address;

    %{ ids.deployed_contract_address = deploy_contract("./src/basic.cairo").ok.contract_address %}
    assert_not_zero(deployed_contract_address);

    local balance;
    %{ ids.balance = call(ids.deployed_contract_address, "get_balance").ok[0] %}
    assert balance = 100;

    local new_balance;
    %{ assert invoke(ids.deployed_contract_address, "increase_balance", {"amount": 123}).err_code == 0 %}
    %{ ids.new_balance = call(ids.deployed_contract_address, "get_balance").ok[0] %}
    assert new_balance = 223;

    %{ assert invoke(ids.deployed_contract_address, "increase_balance", [123]).err_code == 0 %}
    return ();
}

func test_panicking() {
    alloc_locals;
    local error_code;
    %{
        contract_address = deploy_contract("./src/panic.cairo").ok.contract_address
        result = invoke(contract_address, "panic")
        ids.error_code = result.err_code
    %}
    assert error_code = 'PANIC_DESCRIPTION';
    return ();
}

func test_invoke_with_transformation() {
    alloc_locals;
    local deployed_contract_address;

    %{ ids.deployed_contract_address = deploy_contract("./src/basic.cairo").ok.contract_address %}
    assert_not_zero(deployed_contract_address);

    local balance;
    %{ ids.balance = call(ids.deployed_contract_address, "get_balance").ok[0] %}
    assert balance = 100;

    local new_balance;
    %{ invoke(ids.deployed_contract_address, "increase_balance", {"amount": 123}) %}
    %{ ids.new_balance = call(ids.deployed_contract_address, "get_balance").ok[0] %}
    assert new_balance = 223;

    return ();
}

func test_invoke_with_proxy() {
    alloc_locals;
    local deployed_contract_address;

    %{ ids.deployed_contract_address = deploy_contract("./src/basic.cairo").ok.contract_address %}
    assert_not_zero(deployed_contract_address);

    local deployed_proxy_address;
    %{ ids.deployed_proxy_address = deploy_contract("./src/proxy.cairo").ok.contract_address %}
    assert_not_zero(deployed_proxy_address);

    %{ invoke(ids.deployed_proxy_address, "set_target", [ids.deployed_contract_address]).ok %}

    local balance;
    %{ ids.balance = call(ids.deployed_proxy_address, "get_balance").ok[0] %}
    assert balance = 100;

    local new_balance;
    %{ invoke(ids.deployed_proxy_address, "increase_twice", {"amount": 123}).ok %}
    %{ ids.new_balance = call(ids.deployed_proxy_address, "get_balance").ok[0] %}
    assert new_balance = 346;

    return ();
}
