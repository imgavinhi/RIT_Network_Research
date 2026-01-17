def packet_choice(predictions):
    """
    Analyzes the CNN predictions for RTSP time series.
    Each prediction represents a sequence (conversation) of 26 packets. 
    """
    stream_states = [] 

    # Counters for the conversation-level classifications 
    success_counter = 0     # Class 1: 2xx codes
    client_error_counter = 0 # Class 2: 4xx codes
    server_error_counter = 0 # Class 3: 5xx codes
    background_counter = 0   # Class 0: Non-RTSP traffic
    
    total_conversations = len(predictions)

    for i in predictions:
        if i == 1:
            state = "SUCCESSFUL STREAMING"
            success_counter += 1
        elif i == 2:
            state = "CLIENT ERROR (4xx)"
            client_error_counter += 1
        elif i == 3:
            state = "SERVER ERROR (5xx)"
            server_error_counter += 1
        else:
            state = "BACKGROUND/OTHER"
            background_counter += 1
        
        stream_states.append(state)

    # Calculate overall stream health
    # A single error sequence might indicate a streaming failure between nodes 
    print("\n" + "="*30)
    print(" RTSP STREAM ANALYSIS REPORT ")
    print("="*30)
    print(f"Total Conversations Analyzed: {total_conversations}")
    print(f" (Each conversation = 26 packets) ")
    print("-"*30)
    print(f"Successful Segments:  {success_counter}")
    print(f"Client-Side Errors:   {client_error_counter}")
    print(f"Server-Side Errors:   {server_error_counter}")
    print(f"Background Traffic:   {background_counter}")
    print("-"*30)

    # Logic to determine final stream status
    if client_error_counter > 0 or server_error_counter > 0:
        print("FINAL STATUS: STREAM FAILED")
        if client_error_counter > 0:
            print("REASON: Unauthorized (401) or other Client-side error detected.")
    elif success_counter > 0:
        print("FINAL STATUS: STREAM SUCCESSFUL")
    else:
        print("FINAL STATUS: NO RTSP STREAM DETECTED")
    print("="*30 + "\n")

    return stream_states