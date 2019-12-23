import socket                
import time
import sys

def sending_Frames(frames):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    port = 3165
   
    dest = (socket.gethostname(), port)   # ip and port
    try:         
        s.bind((socket.gethostname(), port))    # port binding     
        
    except(socket.error ):
        print(" Port Binding Error\n")
        exit()
    s.listen(5)  

    try:
        c,addr = s.accept()
    except Exception as e:
        print("Exception Raised!!!")
        s.close()
        sys.exit(0)
    f = 0
    totalFrames = len(frames)
    s.settimeout(0.5)
    while(f<totalFrames):
        try:     
            c.send(bytes(frames[f],"UTF-8"))
            ack = c.recv(40).decode('UTF-8')
            if  "received!" in ack:
                print(str(ack))
                f+=1
            elif "Timeout" in ack:       # ack  not received
                print(str(ack)+" ack!")
                continue
            
        except socket.timeout:
            c.send(bytes(frames[f],"UTF-8"))
        
        except Exception as e:
            print("Exception Raised!")
            s.close()
            exit(0)
        except KeyboardInterrupt as e:
            print("Exception Raised!!")
            exit(0)
        except ConnectionResetError as e:
            print("Connection Closed!!\n")
            s.close()
            exit(0)

frameSize = 5

def Frames(data):
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
    frames = Frames(data)
    sending_Frames(frames)  

    print("Connection Closed!!!")
   

mainAlgorithm()
