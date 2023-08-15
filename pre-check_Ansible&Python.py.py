Basic Python&Ansible scripts for pre-checks #Mirand Osmani

import subprocess

def check_reachability(router_ip):
    result = subprocess.run(["ping", "-c", "4", router_ip], stdout=subprocess.PIPE)
    return result.returncode == 0

def check_service_status(service_name):
    result = subprocess.run(["systemctl", "is-active", service_name], stdout=subprocess.PIPE)
    return result.stdout.decode().strip() == "active"

router_ip = "ROUTER_IP_ADDRESS"

if not check_reachability(router_ip):
    print("Router is not reachable.")
    exit(1)

if not check_service_status("telnet"):
    print("Telnet service is not active on the router.")
    exit(1)

def check_bgp_status():
    result = subprocess.run(["show", "ip", "bgp", "summary"], stdout=subprocess.PIPE)
    bgp_output = result.stdout.decode()
    return "BGP state is Active" in bgp_output

def check_ospf_status():
    result = subprocess.run(["show", "ip", "ospf", "neighbor"], stdout=subprocess.PIPE)
    ospf_output = result.stdout.decode()
    return "FULL/DROTHER" in ospf_output

def check_alarms():
    result = subprocess.run(["show", "alarms"], stdout=subprocess.PIPE)
    alarms_output = result.stdout.decode()
    return "Critical" not in alarms_output


if not check_bgp_status():
    print("BGP is not in Active state. Please check which one is not forming BGP properly and make a note!")
    exit(1)

if not check_ospf_status():
    print("OSPF neighbors are not in FULL state.")
    exit(1)

if not check_alarms():
    print("Critical alarms are present on the router.")
    exit(1)

print("Pre-upgrade checks passed.")

-----------------------------------------------------------------------------------------------------------------
Ansible script

#first creating an invetory with appropriate ip addresses of remote hosts(Routers, Switches, Firewalls, Load Balancers etc)
#example:
[routers]
router1 ansible_host=ROUTER1_IP
router2 ansible_host=ROUTER2_IP
# Add more routers as needed

#than create a playbook to execute the pre-upgrade checks
---
- name: Perform Pre-upgrade Checks
  hosts: routers    #this refer to the name of you invetory. 
  tasks:
    - name: Copy pre_upgrade_checks.py to routers
      copy:
        src: pre_upgrade_checks.py
        dest: /tmp/pre_upgrade_checks.py
        mode: 0755

    - name: Execute pre_upgrade_checks.py
      command: python3 /tmp/pre_upgrade_checks.py

    Executing Ansible playbook: ansible-playbook -i inventory.ini pre_upgrade_playbook.yml -u your_ssh_username -k 


