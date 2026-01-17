import numpy as np

def packet_choice(predictions, host_data=None):
    """
    Analyzes CNN predictions for RTSP conversations.
    Each prediction represents a sequence of 12 packets between two nodes.
    """
    stream_states = [] 

    # Counters for conversation-level classifications
    success_ctr = 0      # Class 1: 2xx codes
    client_err_ctr = 0   # Class 2: 4xx codes
    server_err_ctr = 0   # Class 3: 5xx codes
    background_ctr = 0   # Class 0: Non-RTSP traffic
    
    total_convs = len(predictions)

    print("\n" + "="*60)
    print(f"{'RTSP STREAM SESSION REPORT':^60}")
    print("="*60)
    print(f"{'Source IP':<20} | {'Destination IP':<20} | {'Status'}")
    print("-" * 60)

    for idx, pred in enumerate(predictions):
        # Determine the human-readable state
        if pred == 1:
            state = "SUCCESS (2xx)"
            success_ctr += 1
        elif pred == 2:
            state = "CLIENT ERR (4xx)"
            client_err_ctr += 1
        elif pred == 3:
            state = "SERVER ERR (5xx)"
            server_err_ctr += 1
        else:
            state = "BACKGROUND"
            background_ctr += 1
        
        # Retrieve host info if available
        src_ip, dst_ip = ("Unknown", "Unknown")
        if host_data is not None and idx < len(host_data):
            src_ip, dst_ip = host_data[idx]

        # Print RTSP-related conversations
        if pred > 0:
            print(f"{src_ip:<20} | {dst_ip:<20} | {state}")
        
        stream_states.append(state)

    print("-" * 60)
    # The total number of conversations is based on the 12-packet group logic
    print(f"Total Conversations: {total_convs} (12 packets each)")
    print(f"Successful: {success_ctr} | Client Errors: {client_err_ctr} | Server Errors: {server_err_ctr}")
    print("-" * 60)

    # Final Stream Health Conclusion based on status code patterns
    if client_err_ctr > 0 or server_err_ctr > 0:
        print("OVERALL RESULT: STREAMING FAILURE DETECTED")
        if client_err_ctr > 0:
            print("Note: Check for 401 Unauthorized or 404 Not Found errors.")
    elif success_ctr > 0:
        print("OVERALL RESULT: STREAMING SUCCESSFUL")
    else:
        print("OVERALL RESULT: NO RTSP TRAFFIC FOUND")
    print("="*60 + "\n")

    return stream_states