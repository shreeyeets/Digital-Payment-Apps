def analyze_pcap(file_path):
    sni_list = []
    sni_timestamp_list = []
    packet_count = 0
    ip_count = 0
    tcp_count = 0
    possible_tls_count = 0
    tls_handshake_count = 0
    client_hello_count = 0

    with open(file_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        for timestamp, buf in pcap:
            packet_count += 1
            try:
                ip = dpkt.ip.IP(buf)
                ip_count += 1
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    tcp_count += 1
                    if tcp.sport == 443 or tcp.dport == 443:
                        possible_tls_count += 1
                        if len(tcp.data) > 0:
                            record_type, record_data, error = parse_tls_record(tcp.data)
                            if error:
                                if packet_count <= 5:
                                    print(f"Error parsing TLS record in packet {packet_count}: {error}")
                                continue
                            
                            if record_type == 22:  # Handshake
                                tls_handshake_count += 1
                                handshake_type, handshake_data, error = parse_tls_handshake(record_data)
                                if error:
                                    if packet_count <= 5:
                                        print(f"Error parsing TLS handshake in packet {packet_count}: {error}")
                                    continue
                                
                                if handshake_type == 1:  # ClientHello
                                    client_hello_count += 1
                                    extensions_data, error = parse_client_hello(handshake_data)
                                    if error:
                                        if packet_count <= 5:
                                            print(f"Error parsing ClientHello in packet {packet_count}: {error}")
                                        continue
                                    
                                    sni, extensions_seen = parse_tls_extension(extensions_data)
                                    if sni:
                                        sni_timestamp_list.append((sni, datetime.datetime.fromtimestamp(timestamp)))
                                    elif packet_count <= 5:
                                        print(f"ClientHello found in packet {packet_count}, but no SNI extracted")
                                        print(f"Extensions seen: {extensions_seen}")
                                        print(f"Extensions data length: {len(extensions_data)}")
                                        print(f"First 50 bytes of extensions data: {extensions_data[:50].hex()}")
                                elif packet_count <= 5:
                                    print(f"Non-ClientHello handshake type {handshake_type} found in packet {packet_count}")
            except Exception as e:
                if packet_count <= 5:
                    print(f"Error processing packet {packet_count}: {str(e)}")
                    print(f"Packet data starts with: {buf[:50].hex()}")

    # Sort SNI list by timestamp
    sni_timestamp_list.sort(key=lambda x: x[1])
    
    # Separate sorted SNI and timestamps
    sorted_sni_list = [sni for sni, _ in sni_timestamp_list]
    sorted_timestamps = [timestamp for _, timestamp in sni_timestamp_list]

    print(f"Total packets processed: {packet_count}")
    print(f"IP packets found: {ip_count}")
    print(f"TCP packets found: {tcp_count}")
    print(f"Possible TLS packets (port 443): {possible_tls_count}")
    print(f"TLS Handshakes found: {tls_handshake_count}")
    print(f"ClientHello messages found: {client_hello_count}")
    print(f"SNIs extracted: {len(sorted_sni_list)}")
    return sorted_sni_list, sorted_timestamps
