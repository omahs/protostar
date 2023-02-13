func test_expect_call_success() {
  %{
    addr = deploy_contract("./src/basic.cairo").ok.contract_address
    expect_call(addr, "get_balance", [])
    call(addr, "get_balance").ok
  %}

  return ();
}

func test_expect_call_with_stop() {
  %{
    addr = deploy_contract("./src/basic.cairo").ok.contract_address
    expect_call(addr, "get_balance", [])
    call(addr, "get_balance")
    stop_expect_call(addr, "get_balance", [])
  %}

  return ();
}
