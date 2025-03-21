#!/bin/bash                                                                                                         
#                                                                                                                   
#  shaper.sh                                                                                                        
#  ---------                                                                                                        
#  A utility script for traffic shaping using tc                                                                    
#                                                                                                                   
#  Usage                                                                                                            
#  -----                                                                                                            
#  shape.sh start - starts the shaper                                                                               
#  shape.sh stop - stops the shaper                                                                                 
#  shape.sh restart - restarts the shaper                                                                           
#  shape.sh show - shows the rules currently being shaped      

                                                                                                                                                                 
#  tc uses the following units when passed as a parameter.                                                          
#    kbps: Kilobytes per second                                                                                     
#    mbps: Megabytes per second                                                                                     
#    kbit: Kilobits per second                                                                                      
#    mbit: Megabits per second                                                                                      
#    bps: Bytes per second                                                                                          
#  Amounts of data can be specified in:                                                                             
#    kb or k: Kilobytes                                                                                             
#    mb or m: Megabytes                                                                                             
#    mbit: Megabits                                                                                                 
#    kbit: Kilobits                                                                                                 
#                                                                                                                   
#  AUTHORS                                                                                                          
#  -------                                                                                                          
#  Aaron Blankstein                                                                                                 
#  Jeff Terrace                                                                                                     
#                                                                                                                   
#  Original script written by: Scott Seong                                                                          
#  Taken from URL: http://www.topwebhosts.org/tools/traffic-control.php                                             
#                                                                                                                   
                                                                                                                    
# Name of the traffic control command.                                                                              
TC=/sbin/tc                                                                                                         
# Rate to throttle to                                                                                               
RATE=$2                                                                                                             
# Peak rate to allow                                                                                                
PEAKRATE=$3                                                                                                         
# Interface to shape                                                                                                
IF=$4                                                                                                               
# Average to delay packets by                                                                                       
LATENCY=$5                                                                                                          
#Packetloss                                                                                                         
PACKET_LOSS=$6                                                                                                      
# Jitter value for packet delay                                                                                     
# Packets will be delayed by $LATENCY +/- $JITTER                                                                   
JITTER=1ms                                                                                                          
LIMIT=$7                                                                                                            
start() {                                                                                                           
            $TC qdisc add dev $IF root handle 1:0 tbf rate $RATE burst 5kb latency 5ms peakrate $PEAKRATE mtu 2000  
            $TC qdisc add dev $IF parent 1:1 handle 10: netem loss $PACKET_LOSS% delay $LATENCY $JITTER limit $LIMIT
        }                                                                                                           
                                                                                                                    
stop() {                                                                                                            
            $TC qdisc del dev $IF root                                                                              
                $TC qdisc del dev $IF parent 1:1                                                                    
        } 

restart() {                                                                                                         
            stop                                                                                                    
                sleep 1                                                                                             
                    start                                                                                           
            }                                                                                                       
                                                                                                                    
    show() {                                                                                                        
                $TC -s qdisc ls dev $IF                                                                             
        }                                                                                                           
                                                                                                                    
case "$1" in                                                                                                        
                                                                                                                    
        start)                                                                                                      
                                                                                                                    
                echo -n "Starting bandwidth shaping: "                                                              
                start                                                                                               
                echo "done"                                                                                         
                ;;                                                                                                  
                                                                                                                    
        stop)                                                                                                       
                                                                                                                    
                echo -n "Stopping bandwidth shaping: "                                                              
                stop                                                                                                
                echo "done"                                                                                         
                ;;                                                                                                  
                                                                                                                    
        restart)                                                                                                    
                                                                                                                    
                echo -n "Restarting bandwidth shaping: "                                                            
                restart                                                                                             
                echo "done"                                                                                         
                ;;                                                                                                  
                                                                                                                    
        show)                                                                                                       
                                                                                                                    
                echo "Bandwidth shaping status for $IF:"                                                            
                show                                                                                                
                echo ""                                                                                             
                ;;                                                                                                  
                                                                                                                    
        *)                                                                                                          
                                                                                                                    
                pwd=$(pwd)                                                                                          
                echo "Usage: shaper.sh {start|stop|restart|show}"                                                   
                ;;                                                                                                  
                                                                                                                    
        esac                                                                                                        
        exit 0                                                                                                      
~                 
