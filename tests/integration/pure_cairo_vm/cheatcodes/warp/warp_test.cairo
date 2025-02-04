from starkware.cairo.common.math import assert_not_zero

func test_warp(){
    alloc_locals;
    local deployed_contract_address;

    %{
        ids.deployed_contract_address = deploy_contract("./src/main.cairo").ok.contract_address
        assert warp(ids.deployed_contract_address, 123).err_code == 0
    %}

    assert_not_zero(deployed_contract_address);

    local timestamp;
    %{
        ids.timestamp = call(ids.deployed_contract_address, "timestamp_getter").ok[0]
    %}

    assert timestamp = 123;
    return ();
}

func test_warp_with_invoke(){
    alloc_locals;
    local deployed_contract_address;

    %{
        ids.deployed_contract_address = deploy_contract("./src/main.cairo").ok.contract_address
        assert warp(ids.deployed_contract_address, 123).err_code == 0
    %}
    assert_not_zero(deployed_contract_address);

    // Set the timestamp to rolled value
    %{ assert invoke(ids.deployed_contract_address, "block_timestamp_setter").err_code == 0 %}

    // Retrieve stored value
    local stored_block_timestamp;
    %{ ids.stored_block_timestamp = call(ids.deployed_contract_address, "stored_block_timestamp_getter").ok[0] %}
    assert stored_block_timestamp = 123;
    return ();
}