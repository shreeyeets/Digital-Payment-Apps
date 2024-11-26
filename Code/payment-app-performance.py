import matplotlib.pyplot as plt

# Bandwidth Data (Bandwidth in kbps, Transaction Time in seconds)
phonepe_bandwidth = [
    (100, 4.222),
    (200, 2.377),
    (400, 2.080),
    (600, 2.457),
    (800, 2.212),
    (1000, 1.522)
]

mobikwik_bandwidth = [
    (100, 20.623),  # Highest time for lowest bandwidth
    (200, 10.244),
    (300, 6.270),
    (400, 4.370),
    (500, 4.158),
    (600, 4.108),
    (800, 3.813),
    (1000, 3.281)
]

# Latency Data (Latency in ms, Transaction Time in seconds)
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

# Bandwidth subplot
plt.subplot(1, 2, 1)
plt.plot([x[0] for x in phonepe_bandwidth], [x[1] for x in phonepe_bandwidth], 'o-', label='PhonePe')
plt.plot([x[0] for x in mobikwik_bandwidth], [x[1] for x in mobikwik_bandwidth], 's-', label='Mobikwik')
plt.title('Transaction Time vs Bandwidth')
plt.xlabel('Bandwidth (kbps)')
plt.ylabel('Transaction Time (seconds)')
plt.legend()
plt.grid(True)

# Latency subplot
plt.subplot(1, 2, 2)
plt.plot([x[0] for x in phonepe_latency], [x[1] for x in phonepe_latency], 'o-', label='PhonePe')
plt.plot([x[0] for x in mobikwik_latency], [x[1] for x in mobikwik_latency], 's-', label='Mobikwik')
plt.title('Transaction Time vs Latency')
plt.xlabel('Latency (ms)')
plt.ylabel('Transaction Time (seconds)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Print detailed statistics
print("Bandwidth Performance:")
print("\nPhonePe:")
for bw, time in phonepe_bandwidth:
    print(f"Bandwidth {bw} kbps: {time:.3f} seconds")

print("\nMobikwik:")
for bw, time in mobikwik_bandwidth:
    print(f"Bandwidth {bw} kbps: {time:.3f} seconds")

print("\nLatency Performance:")
print("\nPhonePe:")
for lat, time in phonepe_latency:
    print(f"Latency {lat} ms: {time:.3f} seconds")

print("\nMobikwik:")
for lat, time in mobikwik_latency:
    print(f"Latency {lat} ms: {time:.3f} seconds")
