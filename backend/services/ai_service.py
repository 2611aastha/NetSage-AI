import os
from backend.models.schemas import AiDiagnosisResponse

class AiEngineService:
    def __init__(self):
        self.mock_mode = os.getenv("MOCK_AI_MODE", "true").lower() == "true"

    def diagnose_case(self, symptom: str, topology_note: str, show_outputs: str) -> AiDiagnosisResponse:
        output_lower = show_outputs.lower()
        if "administratively down" in output_lower:
            return AiDiagnosisResponse(
                root_cause="Interface Fa0/1 state is set to administrative shutdown.",
                confidence=95,
                confidence_level="high",
                evidence=["Interface Fa0/1 is administratively down, line protocol is down"],
                next_command="show ip interface brief",
                fix_steps=["configure terminal", "interface fa0/1", "no shutdown", "end"],
                osi_layer="Layer 1 / Layer 2",
                concept="Interface State",
                alternative_hypotheses=["Physical Layer link interruption on switch port Fa0/1"],
                human_review_required=True
            )
        elif "access vlan 20" in output_lower:
            return AiDiagnosisResponse(
                root_cause="Switchport assigned to incorrect Access VLAN 20 instead of targeted VLAN 10.",
                confidence=91,
                confidence_level="high",
                evidence=["Switchport access vlan 20 configured on interface Fa0/6"],
                next_command="show interfaces fa0/6 switchport",
                fix_steps=["configure terminal", "interface fa0/6", "switchport access vlan 10", "end"],
                osi_layer="Layer 2",
                concept="VLAN / Trunking",
                alternative_hypotheses=["Trunk tagging mismatch on uplink interface"],
                human_review_required=True
            )
        elif "gateway of last resort is not set" in output_lower:
            return AiDiagnosisResponse(
                root_cause="Missing static default route on core gateway router R1.",
                confidence=88,
                confidence_level="high",
                evidence=["Gateway of last resort is not set in active routing table"],
                next_command="show ip route",
                fix_steps=["configure terminal", "ip route 0.0.0.0 0.0.0.0 10.0.0.1", "end"],
                osi_layer="Layer 3",
                concept="Static Routing",
                alternative_hypotheses=["Dynamic routing adjacency loss"],
                human_review_required=True
            )
        else:
            return AiDiagnosisResponse(
                root_cause="Subnet address resolution issue or invalid gateway subinterface binding.",
                confidence=78,
                confidence_level="medium",
                evidence=["Show command output confirms incomplete ARP mapping."],
                next_command="show running-config interface fa0/0",
                fix_steps=["Verify subinterface IP assignment and subnet bitmask configuration."],
                osi_layer="Layer 3",
                concept="Addressing",
                alternative_hypotheses=["Local host firewall dropping inbound ICMP echo packets"],
                human_review_required=True
            )