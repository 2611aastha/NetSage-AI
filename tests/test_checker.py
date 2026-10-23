import pytest
from rule_checker.checker import DeterministicRuleChecker

@pytest.fixture
def checker():
    return DeterministicRuleChecker()

def test_interface_down(checker):
    res = checker.check_interface_down("FastEthernet0/1 is administratively down")
    assert res.status == "FAIL"

def test_missing_route(checker):
    res = checker.check_missing_route("show ip route\nGateway of last resort is not set")
    assert res.status == "FAIL"