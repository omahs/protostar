func test_expect_event_by_name() {
    %{
        contract_address = deploy_contract("emitter").ok.contract_address
        expect_events({"from_address": contract_address, "name": "EVENT_NAME"})
        assert invoke(contract_address, "emit", [42]).err_code == 0
    %}
    return ();
}

func test_expect_event_by_name_and_data() {
    %{
        contract_address = deploy_contract("emitter").ok.contract_address
        expect_events({"from_address": contract_address, "name": "EVENT_NAME", "data": [42]})
        invoke(contract_address, "emit", [42])
    %}
    return ();
}

func test_fail_on_data_mismatch() {
    %{
        contract_address = deploy_contract("emitter").ok.contract_address
        expect_events({"from_address": contract_address , "name": "EVENT_NAME", "data": [21]})
        invoke(contract_address, "emit", [42])
    %}
    return ();
}

func test_fail_when_no_events_were_emitted() {
    %{ expect_events({"from_address": 123, "name": "EVENT_NAME"}) %}
    return ();
}

func test_expect_events_in_declared_order() {
    %{
        contract_address = deploy_contract("emitter").ok.contract_address
        expect_events(
            {"from_address": contract_address, "name": "EVENT_NAME", "data": [21]},
            {"from_address": contract_address, "name": "EVENT_NAME", "data": [37]},
        )
        invoke(contract_address, "emit", [21])
        invoke(contract_address, "emit", [37])
    %}
    return ();
}

func test_fail_message_about_first_not_found_event() {
    %{
        contract_address = deploy_contract("emitter").ok.contract_address
        expect_events(
            {"from_address": contract_address, "name": "EVENT_NAME", "data": [37]},
            {"from_address": contract_address, "name": "EVENT_NAME", "data": [21]},
        )
        invoke(contract_address, "emit", [21])
        invoke(contract_address, "emit", [37])
    %}
    return ();
}

func test_allow_checking_for_events_in_any_order() {
    %{
        contract_address = deploy_contract("emitter").ok.contract_address
        expect_events({"from_address": contract_address, "name": "EVENT_NAME"})
        expect_events({"from_address": contract_address, "name": "EVENT_NAME_2"})
        invoke(contract_address, "emit", [21])
        invoke(contract_address, "emit_2", [37])
    %}
    return ();
}
