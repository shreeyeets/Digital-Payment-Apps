import dpkt
import socket
from dpkt.compat import compat_ord
import datetime
import matplotlib.pyplot as plt

def parse_tls_record(data):
    if len(data) < 5:
        return None, None, "TLS record too short"
    
    record_type = data[0]
    version = int.from_bytes(data[1:3], 'big')
    length = int.from_bytes(data[3:5], 'big')
    
    if len(data) < length + 5:
        return None, None, f"TLS record incomplete. Expected {length + 5} bytes, got {len(data)}"
    
    record_data = data[5:5+length]
    return record_type, record_data, None

def parse_tls_handshake(data):
    if len(data) < 4:
        return None, None, "Handshake message too short"
    
    handshake_type = data[0]
    length = int.from_bytes(data[1:4], 'big')
    
    if len(data) < length + 4:
        return None, None, f"Handshake message incomplete. Expected {length + 4} bytes, got {len(data)}"
    
    handshake_data = data[4:4+length]
    return handshake_type, handshake_data, None

def parse_client_hello(data):
    if len(data) < 34:
        return None, "ClientHello too short"
    
    client_version = int.from_bytes(data[:2], 'big')
    random = data[2:34]
    session_id_length = data[34]
    
    offset = 35 + session_id_length
    if len(data) < offset + 2:
        return None, "ClientHello incomplete: can't read cipher suites length"
    
    cipher_suites_length = int.from_bytes(data[offset:offset+2], 'big')
    offset += 2 + cipher_suites_length
    
    if len(data) < offset + 1:
        return None, "ClientHello incomplete: can't read compression methods length"
    
    compression_methods_length = data[offset]
    offset += 1 + compression_methods_length
    
    if len(data) < offset + 2:
        return None, "ClientHello incomplete: can't read extensions length"
    
    extensions_length = int.from_bytes(data[offset:offset+2], 'big')
    offset += 2
    
    if len(data) < offset + extensions_length:
        return None, "ClientHello incomplete: extensions data incomplete"
    
    extensions_data = data[offset:offset+extensions_length]
    return extensions_data, None

def parse_tls_extension(data):
    sni = None
    extensions_seen = []
    while data:
        if len(data) < 4:
            break
        ext_type = int.from_bytes(data[:2], 'big')
        ext_len = int.from_bytes(data[2:4], 'big')
        extensions_seen.append(ext_type)
        
        if ext_type == 0 and len(data) >= ext_len + 4:  # Server Name Indication
            sni_data = data[4:4+ext_len]
            if len(sni_data) > 2:
                sni_list_len = int.from_bytes(sni_data[:2], 'big')
                if len(sni_data) >= sni_list_len + 2:
                    name_data = sni_data[2:2+sni_list_len]
                    if name_data and name_data[0] == 0:  # host_name
                        name_len = int.from_bytes(name_data[1:3], 'big')
                        if len(name_data) >= name_len + 3:
                            sni = name_data[3:3+name_len].decode('utf-8', errors='ignore')
        
        data = data[4+ext_len:]
    
    return sni, extensions_seen

def analyze_pcap(file_path):
    sni_list = []
    timestamps = []
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
                                        sni_list.append(sni)
                                        timestamps.append(datetime.datetime.fromtimestamp(timestamp))
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

    print(f"Total packets processed: {packet_count}")
    print(f"IP packets found: {ip_count}")
    print(f"TCP packets found: {tcp_count}")
    print(f"Possible TLS packets (port 443): {possible_tls_count}")
    print(f"TLS Handshakes found: {tls_handshake_count}")
    print(f"ClientHello messages found: {client_hello_count}")
    print(f"SNIs extracted: {len(sni_list)}")
    return sni_list, timestamps

def plot_transactions(timestamps):
    if not timestamps:
        print("No timestamps to plot. The graph will be empty.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, range(len(timestamps)), marker='o')
    plt.xlabel('Time')
    plt.ylabel('Transaction Count')
    plt.title('TLS Transactions Over Time')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main(pcap_file):
    sni_list, timestamps = analyze_pcap(pcap_file)
    
    print("\nSNI found:")
    for sni in set(sni_list):
        print(f"- {sni}")
    
    print(f"\nTotal TLS transactions: {len(timestamps)}")
    plot_transactions(timestamps)

if __name__ == "__main__":
    pcap_file = "path/to/your/pcap/file.pcap"
    main(pcap_file)
