import os

path="/home/dell/Desktop/speedtest_diagnostics/src/tool"
capacity_list = [200,300,400,500]
fixed_cap=500000
pkt_loss_list=[1,2,3,4,5,6,7,8,9,10]
fixed_latency=3000
iface = "br-lan"
latency_list=[10,20,30,40,50,60,70,80,90,100]

tools = ["ndt","ookla"]

data_dir_list = ["LAT=10","LAT=20","LAT=30","LAT=40","LAT=50","LAT=60","LAT=70","LAT=80","LAT=90","LAT=100"]
data_dir= "data2"
NUM_REP=5
for tool in tools:
	for i in range(0,10):
		for k in range(0, NUM_REP):
			k = "start"
			cmd = f"ssh root@192.168.1.1 'ash /root/shaper_dpa.sh {k} {fixed_cap}kbit {fixed_cap+2}kbit {iface} {fixed_latency}ms {pkt_loss_list[0]}'"
			print(cmd)
			os.system(cmd)
			bottleneck_cmd = f"{path}/tslp-bottleneck-finder -d {tool}_exp3/{data_dir_list[i]} -w 50 -t {tool}"
			print("Running bottleneck finder tool")
			os.system(bottleneck_cmd)
			k = "stop"
			cmd = f"ssh root@192.168.1.1 'ash /root/shaper_dpa.sh {k} {fixed_cap}kbit {fixed_cap+2}kbit {iface} {fixed_latency} {pkt_loss_list[0]}'"
			os.system(cmd)


    ## logic to log the metadata 
