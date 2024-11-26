import matplotlib.pyplot as plt

# Bandwidth Data
phonepe_bandwidth = [
    (100, 4.222),
    (200, 2.377),
    (400, 2.080),
    (600, 2.457),
    (800, 2.212),
    (1000, 1.522)
]

mobikwik_bandwidth = [
    (100, 20.623),
    (200, 10.244),
    (300, 6.270),
    (400, 4.370),
    (500, 4.158),
    (600, 4.108),
    (800, 3.813),
    (1000, 3.281)
]

# Latency Data
phonepe_latency = [
    (10, 1.330),
    (100, 1.711),
    (500, 1.920),
    (1000, 2.888),
    (1500, 5.210),
    (2000, 9.550),
    (3000, 11.223),
    (4000, 14.294)
]

mobikwik_latency = [
    (10, 3.500),
    (50, 3.997),
    (100, 3.864),
    (150, 4.607),
    (200, 4.395),
    (300, 4.228),
    (500, 4.597),
    (750, 7.066),
    (1000, 7.504),
    (1500, 7.460),
    (2000, 7.500),
    (3000, 9.240),
    (4000, 11.360)
]

# Create a figure with two subplots
plt.figure(figsize=(12, 5))

# Bandwidth subplot (Bandwidth on x-axis)
plt.subplot(1, 2, 1)
plt.plot([x[1] for x in phonepe_bandwidth], [x[0] for x in phonepe_bandwidth], 'o-', label='PhonePe')
plt.plot([x[1] for x in mobikwik_bandwidth], [x[0] for x in mobikwik_bandwidth], 's-', label='Mobikwik')
plt.title('Transaction Time vs Bandwidth')
plt.ylabel('Transaction Time (ms)')
plt.xlabel('Bandwidth (Mbps)')
plt.legend()
plt.grid(True)

# Latency subplot (Latency on x-axis)
plt.subplot(1, 2, 2)
plt.plot([x[1] for x in phonepe_latency], [x[0] for x in phonepe_latency], 'o-', label='PhonePe')
plt.plot([x[1] for x in mobikwik_latency], [x[0] for x in mobikwik_latency], 's-', label='Mobikwik')
plt.title('Transaction Time vs Latency')
plt.ylabel('Transaction Time (ms)')
plt.xlabel('Latency (ms)')
plt.xscale('log')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Print out some basic statistics
print("PhonePe Bandwidth Stats:")
print(f"Min Bandwidth: {min(x[1] for x in phonepe_bandwidth):.3f} Mbps")
print(f"Max Bandwidth: {max(x[1] for x in phonepe_bandwidth):.3f} Mbps")

print("\nMobikwik Bandwidth Stats:")
print(f"Min Bandwidth: {min(x[1] for x in mobikwik_bandwidth):.3f} Mbps")
print(f"Max Bandwidth: {max(x[1] for x in mobikwik_bandwidth):.3f} Mbps")

print("\nPhonePe Latency Stats:")
print(f"Min Latency: {min(x[1] for x in phonepe_latency):.3f} ms")
print(f"Max Latency: {max(x[1] for x in phonepe_latency):.3f} ms")

print("\nMobikwik Latency Stats:")
print(f"Min Latency: {min(x[1] for x in mobikwik_latency):.3f} ms")
print(f"Max Latency: {max(x[1] for x in mobikwik_latency):.3f} ms")
