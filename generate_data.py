import csv
import json
import os

os.makedirs("data", exist_ok=True)

# 1. Populate 32 cases into cases.csv
cases = [
    {
        "case_id": "NS-001",
        "symptom": "PC-01 cannot obtain IP address from DHCP pool.",
        "topology_note": "PC-01 on Switch SW1 Port Fa0/2; Router R1 running DHCP service.",
        "show_outputs": "SW1# show interfaces fa0/2 switchport\nAccess Mode VLAN: 10\nR1# show ip dhcp binding\n(No bindings active)",
        "expected_fault": "DHCP Relay helper address missing on VLAN 10 interface",
        "osi_layer": "Layer 3",
        "concept": "DHCP",
        "severity": "High"
    },
    {
        "case_id": "NS-002",
        "symptom": "Sales-PC ping to WebServer fails continuously.",
        "topology_note": "Sales-PC connected to Fa0/6 on SW1.",
        "show_outputs": "SW1# show interfaces fa0/6 switchport\nName: Fa0/6\nAccess Mode VLAN: 20 (Marketing)",
        "expected_fault": "Access VLAN mismatch on endpoint switchport",
        "osi_layer": "Layer 2",
        "concept": "VLAN / Trunking",
        "severity": "High"
    },
    {
        "case_id": "NS-003",
        "symptom": "Branch router cannot reach external gateway subnets.",
        "topology_note": "Branch-R1 connected to ISP-Edge via Gi0/0.",
        "show_outputs": "Branch-R1# show ip route\nGateway of last resort is not set",
        "expected_fault": "Missing default route to ISP next-hop",
        "osi_layer": "Layer 3",
        "concept": "Static Routing",
        "severity": "Critical"
    }
]

for i in range(4, 33):
    cases.append({
        "case_id": f"NS-0{i:02d}",
        "symptom": f"Host NS-HOST-{i} unreachable across local boundary.",
        "topology_note": f"Topology segment {i} linked to SW-Core.",
        "show_outputs": f"SW-Core# show running-config interface fa0/{i}\nFastEthernet0/{i} is administratively down, line protocol is down" if i % 4 == 0 else f"SW-Core# show ip route\nGateway of last resort is not set",
        "expected_fault": "Interface administratively disabled" if i % 4 == 0 else "Missing default route entry",
        "osi_layer": f"Layer {(i % 3) + 2}",
        "concept": ["VLAN / Trunking", "DHCP", "Static Routing", "ACL", "NAT", "DNS"][i % 6],
        "severity": ["Critical", "High", "Medium", "Low"][i % 4]
    })

with open("data/cases.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cases[0].keys())
    writer.writeheader()
    writer.writerows(cases)

# 2. Responsible AI Log
ai_log = """case_id,initial_ai_diagnosis,ai_confidence,reviewer_correction,actual_fault,evidence_proved_wrong,error_reason,lesson_learned
NS-014,DNS host resolution timeout failure,85,ACL explicit deny rule order blocking traffic,ACL rule sequence 10 dropped UDP 53 before permit rule,AI evaluated host symptom instead of parsing access-list rule priority order,Rule checker parser must precede LLM prompts for access list sequence verification.
NS-019,Static route missing to 10.20.30.0/24 subnet,88,Duplicate IP conflict on gateway subinterface,ARP log table showed duplicate address conflict on 10.20.30.1,AI missed secondary log output embedded in show commands,Structured log analysis should run deterministically prior to prompt generation.
NS-022,DHCP server pool exhaustion,91,Switchport assigned to wrong Access VLAN 20,Switchport Fa0/6 mode access vlan 20 instead of 10,AI relied on host DHCP timeout log without correlating switchport state,Contextual topology cross-checking is mandatory for Layer 2 diagnostics.
NS-027,Trunk encapsulation dot1q protocol mismatch,82,Native VLAN mismatch causing untagged frame drop,Native VLAN 1 on SW1 vs Native VLAN 99 on SW2,AI misattributed framing errors to link protocol settings,Explicit native VLAN matching logic required in rule checker layer.
NS-031,WLC security key authentication error,79,Default gateway route missing on AP subinterface,Gateway of last resort not set on WLC management subinterface,AI over-attributed failure to wireless domain rather than basic IP reachability,Verify Layer 3 reachability baseline before analyzing Layer 7 protocol states."""

with open("data/responsible_ai_log.csv", "w", encoding="utf-8") as f:
    f.write(ai_log)

# 3. Initial Empty Review Log
with open("data/review_log.json", "w", encoding="utf-8") as f:
    json.dump([], f)

print("Data structures initialized successfully.")