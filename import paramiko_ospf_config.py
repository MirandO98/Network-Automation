import paramiko

# Define router information
router1_ip = "10.10.10.2"
router2_ip = "10.10.10.3"
username = "cisco"
password = "cisco"

# Define OSPF configuration commands
ospf_config = [
    "router ospf 1",
    "network 0.0.0.0 0.0.0.0 area 1",
    "end",
    "write memory",
]

# Create SSH clients for the routers
router1 = paramiko.SSHClient()
router2 = paramiko.SSHClient()
router1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
router2.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to Router 1
    router1.connect(router1_ip, username=username, password=password)

    # Send OSPF configuration to Router 1
    router1_shell = router1.invoke_shell()
    for command in ospf_config:
        router1_shell.send(command + "\n")
    router1_shell.send("exit\n")
    router1_shell.close()

    # Connect to Router 2
    router2.connect(router2_ip, username=username, password=password)

    # Send OSPF configuration to Router 2
    router2_shell = router2.invoke_shell()
    for command in ospf_config:
        router2_shell.send(command + "\n")
    router2_shell.send("exit\n")
    router2_shell.close()

    print("OSPF configuration applied successfully.")

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close SSH connections
    router1.close()
    router2.close()
