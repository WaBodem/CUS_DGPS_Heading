
import paho.mqtt.client as mqtt
import time
import math

msgcounter1 = 0
msgcounter2 = 0
SumRW1=0
SumHW1=0
SumRW2=0
SumHW2=0
gpstimersec=20
# The callback for when the client receives a CONNACK response from the server.
def on_connect(clientcompass, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker; subscribing\n")
        #aubscribe to topic /device/CS1_1/GGA and /device/CS1_2/GGA
        clientcompass.subscribe("/device/CS1_1/GK")
        clientcompass.subscribe("/device/CS1_2/GK")

    else:
        print("Connection failed!")
        
# The callback for when a PUBLISH message is received from the server.
def on_message(clientc, userdata, message):
    global msgcounter1, msgcounter2, SumRW1, SumHW1, SumRW2, SumHW2
    #print('Received',userdata , message.topic, message.payload )
    # send payload to the GNSS receiver over serial
    #print(message)
    if message.topic == "/device/CS1_1/GK":
        #split payload into list and print list
        payload = message.payload.decode("utf-8").strip().split(" ")
        #print(payload)
        if payload[4].split('=')[1] == "4" or payload[4].split('=')[1] == "5" and msgcounter1 <= 10:
            #split payload RW and SumRW
            SumRW1 += float(payload[2].split("=")[1])
            SumHW1 += float(payload[3].split("=")[1])
            msgcounter1 = msgcounter1 + 1

        
    if message.topic == "/device/CS1_2/GK":
        #split payload into list and print list
        payload = message.payload.decode("utf-8").strip().split(" ")
        #print(payload)
        if payload[4].split('=')[1] == "4" or  payload[4].split('=')[1] == "5" and msgcounter2 <= 10:
            #split payload RW and SumRW
            SumRW2 += float(payload[2].split("=")[1])
            SumHW2 += float(payload[3].split("=")[1])
            msgcounter2 = msgcounter2 + 1
        
    
def main():
    global msgcounter2, msgcounter1, SumRW1, SumHW1, SumRW2, SumHW2,gpstimersec
    #create clientcompass 
    clientcompass = mqtt.Client("compass")
    #connect to broker localhost
    clientcompass.connect(host= "192.168.178.60", port=1883)

     
    #set callback functions
    clientcompass.on_connect = on_connect
    clientcompass.on_message = on_message
    #clientcompass.loop_forever()
    clientcompass.loop_start()
    gpstimer=time.time()+gpstimersec
    #main loop
    while True:
        x=0
        y=0
        time.sleep(1)
        print(".", end='', flush=True)
        if msgcounter2 == 10 and msgcounter1 == 10:
            RW1=round(SumRW1/10,2)
            HW1= round(SumHW1/10,2)
            RW2=round(SumRW2/10,2)
            HW2=round(SumHW2/10,2)
            print("\nRW1 HW1: ", RW1,HW1)
            print("RW2 HW2: ", RW2, HW2)
            #create vector between points RW1,HW1 and RW2,HW2
            x=RW1-RW2
            y=HW1-HW2
            #calculate angle between vector and north
            angle=round(math.degrees(math.atan2(y,x)),2)
            CSRW=round((RW2+RW1)/2,2)
            CSHW=round((HW2+HW1)/2,2)
            #calculate length of vector between points RW1,HW1 and RW2,HW2
            basislänge=round(math.sqrt(x**2+y**2),2)
            print("Orientierung: ", round(180-angle,2), '°', 'Baseline:', int(basislänge*100), ' cm CS Standpunkt:', CSRW, CSHW)
            clientcompass.publish("/CS1/Orientierung", str(round(180-angle,2)))
            clientcompass.publish("/CS1/Baseline", str(int(basislänge*100)))
            clientcompass.publish("/CS1/GK", str(CSRW)+' '+ str(CSHW))
            msgcounter2=0
            msgcounter1=0
            RW1=0
            HW1=0
            RW2=0
            SumRW1=0
            SumHW1=0
            SumRW2=0
            SumHW2=0
            gpstimer=time.time()+gpstimersec
        if time.time() > gpstimer:
            print("GPS Timeout")
            gpstimer=time.time()+gpstimersec
            msgcounter2=0
            msgcounter1=0
            RW1=0
            HW1=0
            RW2=0
            SumRW1=0
            SumHW1=0
            SumRW2=0
            SumHW2=0




 
        
        
#call main function
if __name__ == '__main__':
    main()
 