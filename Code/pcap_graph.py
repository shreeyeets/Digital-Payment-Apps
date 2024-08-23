import dpkt
import socket
import datetime
import matplotlib.pyplot as plt

def mac_addr(address):
    return ':'.join('%02x' % b for b in address)

def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def extract_tls_sni(pcap_file):
    tls_transactions = []

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        
        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            
            if not isinstance(eth.data, dpkt.ip.IP):
                continue
            
            ip = eth.data
            if isinstance(ip.data, dpkt.tcp.TCP):
                tcp = ip.data
                if tcp.dport == 443 or tcp.sport == 443:  # TLS traffic typically on port 443
                    try:
                        ssl = dpkt.ssl.TLSRecord(tcp.data)
                        if isinstance(ssl.data, dpkt.ssl.TLSHandshake):
                            handshake = ssl.data
                            if isinstance(handshake.data, dpkt.ssl.TLSClientHello):
                                client_hello = handshake.data
                                for ext_type, ext_data in client_hello.extensions:
                                    if ext_type == 0x00:  # SNI extension
                                        sni = ext_data[5:].decode()
                                        src_ip = inet_to_str(ip.src)
                                        dst_ip = inet_to_str(ip.dst)
                                        tls_transactions.append((timestamp, src_ip, dst_ip, sni))
                    except (dpkt.ssl.SSL3Exception, dpkt.dpkt.NeedData):
                        continue

    return tls_transactions

def plot_tls_transactions(tls_transactions):
    times = [datetime.datetime.utcfromtimestamp(ts) for ts, _, _, _ in tls_transactions]
    sni_hosts = [sni for _, _, _, sni in tls_transactions]

    plt.figure(figsize=(12, 6))
    plt.scatter(times, sni_hosts, c='blue', alpha=0.6, edgecolors='w', linewidth=0.5)
    plt.xlabel('Time')
    plt.ylabel('SNI Hosts')
    plt.title('TLS/SNI Transactions Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Enter pcap file datapath here
pcap_file = 'PCAPdroid_22_Aug_22_37_04.pcap'
tls_transactions = extract_tls_sni(pcap_file)

# Debugging: Print the extracted transactions
print("Extracted TLS/SNI Transactions:")
for transaction in tls_transactions:
    print(transaction)

plot_tls_transactions(tls_transactions)
