import re
from typing import List
from rule_checker.models import CheckResult

class DeterministicRuleChecker:
    def __init__(self):
        pass

    def run_all_checks(self, show_outputs: str, topology_note: str = "") -> List[CheckResult]:
        results = [
            self.check_interface_down(show_outputs),
            self.check_duplicate_ip(show_outputs),
            self.check_gateway_mismatch(show_outputs),
            self.check_missing_route(show_outputs),
            self.check_subnet_mask(show_outputs)
        ]
        return [r for r in results if r is not None]

    def check_interface_down(self, show_output: str) -> CheckResult:
        if "administratively down" in show_output.lower():
            matches = re.findall(r"(\S+)\s+is administratively down", show_output, re.IGNORECASE)
            intf = matches[0] if matches else "Interface"
            return CheckResult(
                check_name="interface_admin_down",
                status="FAIL",
                severity="critical",
                evidence=f"{intf} status: administratively down",
                explanation=f"Target interface {intf} has been shut down manually.",
                recommended_action=f"Execute 'no shutdown' on interface {intf}."
            )
        return CheckResult(
            check_name="interface_admin_down",
            status="PASS",
            severity="low",
            evidence="No administratively down interfaces detected.",
            explanation="Interface operational states validated."
        )

    def check_duplicate_ip(self, show_output: str) -> CheckResult:
        if "duplicate ip" in show_output.lower() or "conflict detected" in show_output.lower():
            return CheckResult(
                check_name="duplicate_ip",
                status="FAIL",
                severity="critical",
                evidence="IP conflict notification detected in system logs.",
                explanation="Address conflict present on local broadcast domain.",
                recommended_action="Reassign static address or reset local DHCP lease state."
            )
        return CheckResult(
            check_name="duplicate_ip",
            status="PASS",
            severity="low",
            evidence="No duplicate IP logs detected.",
            explanation="IP address uniqueness verified."
        )

    def check_gateway_mismatch(self, show_output: str) -> CheckResult:
        if "default-gateway" in show_output.lower():
            gw_match = re.search(r"ip default-gateway\s+(\d+\.\d+\.\d+\.\d+)", show_output, re.IGNORECASE)
            ip_match = re.search(r"ip address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)", show_output, re.IGNORECASE)
            if gw_match and ip_match:
                gw = gw_match.group(1)
                ip = ip_match.group(1)
                if gw.split('.')[:3] != ip.split('.')[:3]:
                    return CheckResult(
                        check_name="gateway_mismatch",
                        status="FAIL",
                        severity="high",
                        evidence=f"Host IP: {ip}, Default Gateway: {gw}",
                        explanation="Configured gateway belongs to an improper network prefix.",
                        recommended_action="Adjust default-gateway parameter to local subnet router interface IP."
                    )
        return CheckResult(
            check_name="gateway_mismatch",
            status="PASS",
            severity="low",
            evidence="Default gateway prefix aligns with local host configuration.",
            explanation="Gateway routing check passed."
        )

    def check_missing_route(self, show_output: str) -> CheckResult:
        if "show ip route" in show_output.lower() and "gateway of last resort is not set" in show_output.lower():
            return CheckResult(
                check_name="missing_default_route",
                status="FAIL",
                severity="high",
                evidence="Gateway of last resort is not set in routing table.",
                explanation="Router lacks default routing policy for non-local traffic.",
                recommended_action="Define static route via 'ip route 0.0.0.0 0.0.0.0 <next-hop>'."
            )
        return CheckResult(
            check_name="missing_default_route",
            status="PASS",
            severity="low",
            evidence="Default gateway or active routes exist.",
            explanation="Routing table rules verified."
        )

    def check_subnet_mask(self, show_output: str) -> CheckResult:
        if "255.255.255.255" in show_output:
            return CheckResult(
                check_name="invalid_subnet_mask",
                status="FAIL",
                severity="medium",
                evidence="Host mask /32 (255.255.255.255) assigned to active LAN interface.",
                explanation="Host cannot form ARP bindings with local subnets.",
                recommended_action="Reconfigure mask to standard network prefix."
            )
        return CheckResult(
            check_name="invalid_subnet_mask",
            status="PASS",
            severity="low",
            evidence="Subnet mask values conform to standard network ranges.",
            explanation="Subnet checks passed."
        )