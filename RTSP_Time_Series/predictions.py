import numpy as np

def packet_choice(predictions, host_data=None):
    """
    Analyzes CNN predictions for RTSP conversations.
    Prioritizes error detection over success for stream health reporting.
    """
    stream_states = [] 

    # Initialize all counters to 0
    success_ctr = 0      # Class 1: 2xx codes
    client_err_ctr = 0   # Class 2: 4xx codes (e.g., 401 Unauthorized)
    server_err_ctr = 0   # Class 3: 5xx codes
    data_trans_ctr = 0   # Class 4: Data Streaming
    background_ctr = 0   # Class 0: Non-RTSP traffic
    
    total_convs = len(predictions)

    print("\n" + "="*60)
    print(f"{'RTSP STREAM SESSION REPORT':^60}")
    print("="*60)
    print(f"{'Source IP':<20} | {'Destination IP':<20} | {'Status'}")
    print("-" * 60)

    for idx, pred in enumerate(predictions):
        # Determine human-readable state
        if pred == 1:
            state = "SUCCESS (200 OK)"
            success_ctr += 1
        elif pred == 2:
            state = "CLIENT ERR (401)"
            client_err_ctr += 1
        elif pred == 3:
            state = "SERVER ERR (5xx)"
            server_err_ctr += 1
        elif pred == 4:
            state = "DATA STREAMING"
            data_trans_ctr += 1
        else:
            state = "BACKGROUND"
            background_ctr += 1
        
        # Retrieve host info
        src_ip, dst_ip = ("Unknown", "Unknown")
        if host_data is not None and idx < len(host_data):
            src_ip, dst_ip = host_data[idx]

        # Log every RTSP-related conversation segment
        if pred > 0:
            print(f"{src_ip:<20} | {dst_ip:<20} | {state}")
        
        stream_states.append(state)

    print("-" * 60)
    print(f"Total Conversations: {total_convs} (12 packets each)")
    print(f"Success/Data: {success_ctr + data_trans_ctr} | Client Errors: {client_err_ctr} | Server Errors: {server_err_ctr}")
    print("-" * 60)

    # --- CRITICAL: STRICT ERROR-FIRST LOGIC ---
    # We check for errors first. If any exist, the stream is a failure.
    if client_err_ctr > 0 or server_err_ctr > 0:
        print("OVERALL RESULT: STREAMING FAILURE DETECTED")
        if client_err_ctr > 0:
            print("Note: Multiple 401 Unauthorized codes found. Authentication is failing.")
    elif success_ctr > 0 or data_trans_ctr > 0:
        # Only report success if there were zero error segments detected
        print("OVERALL RESULT: STREAMING SUCCESSFUL")
    else:
        print("OVERALL RESULT: NO RTSP TRAFFIC FOUND")
    print("="*60 + "\n")

    return stream_states