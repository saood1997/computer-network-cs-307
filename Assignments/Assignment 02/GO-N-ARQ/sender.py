import socket                
import time
import sys

def sendData(frames):
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    PORT = 3000
   
    dest = (socket.gethostname(), PORT)   # ip and port
    try:         
        sockt.bind((socket.gethostname(), PORT))         
    except(socket.error ):
        print("\n Socket Binding Error\n")
        exit()
    sockt.listen(5)  

    try:
        c,addr = sockt.accept()
        print("Client Conneted at Port : "+str(addr[1])+"\n")
    except Exception as e:
        sockt.close()
        sys.exit(0)
    f = 0
    totalFrames = len(frames)
    sockt.settimeout(0.05)
    global mainFrame
    Sw,Sn,Sf = 3,0,0
    ackNumber = 0
    mainFrame[1][:] = frames[0:Sw]
    next1 = Sw
    while True:
              
        try:     
            c.send(bytes(mainFrame[1][0]+'|'+str(ackNumber),"utf-8"))
            mainFrame[0].append(mainFrame[1].pop(0))
            print("\nSending Frame :{}".format(str(ackNumber)),mainFrame)
            Sn += 1
            time.sleep(.5)         
            
            startingTime = time.time()
            stopTime = 0
            ack = c.recv(20).decode('utf-8')
            ackNumber = int(ack[-1])    
            if 'Timeout' in ack:
                print("Timeout:")
                continue
            if 'end' in ack:
                mainFrame[0].pop(0)
                print("Received ACK :"+str(ackNumber)," ",ack)

                break
            if "noACK" in ack:       # ack not received
                print("\n No Acknoledgement\n")
                time.sleep(5)
            if(ackNumber>=Sf and ackNumber<=Sn):
                if  "ACK" in ack:
                    print("Received ACK :"+str(ackNumber),ack)
                    while(Sf<=ackNumber):
                        mainFrame[0].pop(0)
                        if (next1 < totalFrames):
                            mainFrame[1].append(frames[next1])
                            next1+=1
                        Sf += 1
                    ackNumber+=1
            stopTime = time.time()
            timeout = stopTime - startingTime
            # print("Timeout: ",timeout)
            
        except socket.timeout:
            c.send(bytes(mainFrame[1][0]+'|'+str(ackNumber),"utf-8"))
        except Exception as e:
            print(str(e))
            sockt.close()
            exit(0)
        except KeyboardInterrupt as e:
            print("Socket Closed\n")
            exit(0)
        except ConnectionResetError as e:
            print("Connection Closed\n")
            sockt.close()
            exit(0)
mainFrame = [[],[]]     # [sent & ack  ,  Sent & not ack]
frameSize = 1

def makeFrames(data):
    frames = []
    if len(data) > frameSize:
        for i in range(0,len(data),frameSize):
            frame = data[i:i+frameSize]
            frames.append(frame)
    else:
        frames.append(data)
    frames.append('}^{')
    return frames

def mainAlgorithm():
    data = "Data Send!"
    frames = makeFrames(data)
    sendData(frames)  
    print("Connection Closed")
   
def main():
    mainAlgorithm()
main()
