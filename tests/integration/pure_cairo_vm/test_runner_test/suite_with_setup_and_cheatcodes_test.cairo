func __setup__(){
    %{ context.contract_address = deploy_contract("./src/main.cairo").ok.contract_address %}
    return ();
}

func test_setup_with_deployment(){
    alloc_locals;
    local initial_balance;

    %{ ids.initial_balance = call(context.contract_address, "get_balance").ok[0] %}
    assert initial_balance = 100;

    local increased_balance;
    %{
        assert invoke(context.contract_address, "increase_balance", [100]).err_code == 0
        ids.increased_balance = call(context.contract_address, "get_balance").ok[0]

    %}
    assert increased_balance = 200;

    return ();
}

// Depends on test_setup_with_deployment, which modifies the state
func test_suites_with_setups_dont_leak_state(){
    alloc_locals;
    local initial_balance;

    %{
        ids.initial_balance = call(context.contract_address, "get_balance").ok[0]
    %}
    assert initial_balance = 100;

    return ();
}