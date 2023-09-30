import paramiko

# Define the router information
router_info = [
    {"hostname": "Router1", "ip": "10.10.10.1", "username": "cisco", "password": "cisco"},
    {"hostname": "Router2", "ip": "10.10.10.2", "username": "cisco", "password": "cisco"},
    {"hostname": "Router3", "ip": "10.10.10.3", "username": "cisco", "password": "cisco"},
]

# Define the ping command
ping_command = "ping 8.8.8.8"

# Loop through the routers and test ping
for router in router_info:
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the router
        ssh_client.connect(
            router["ip"],
            username=router["username"],
            password=router["password"],
            timeout=10,
        )

        # Execute the ping command
        stdin, stdout, stderr = ssh_client.exec_command(ping_command)

        # Print the results
        print(f"Router: {router['hostname']} ({router['ip']})")
        print(stdout.read().decode("utf-8"))

        # Close the SSH connection
        ssh_client.close()

    except paramiko.AuthenticationException as auth_error:
        print(f"Authentication failed for {router['hostname']}: {auth_error}")
    except paramiko.SSHException as ssh_error:
        print(f"SSH connection failed for {router['hostname']}: {ssh_error}")
    except Exception as e:
        print(f"An error occurred for {router['hostname']}: {e}")
