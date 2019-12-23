import socket                
def Sending_Frames(frames):
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    PORT = 2203 # port number
   
    dest = (socket.gethostname(), PORT)  # host ip and port
    try:         
        sockt.bind((socket.gethostname(), PORT))  # binding port
    except(socket.error ):
        print("Port Binding Error\n")
        exit()
    sockt.listen(5)  
    try:
        c,addr = sockt.accept()
    except Exception as e:
        print(str(e))
        sockt.close()
        exit(0)

    frame = 0
    totalFrames = len(frames)
 
    while(frame<totalFrames):
        try:     
            c.send(bytes(frames[frame],"UTF-8"))
            ACK = c.recv(40).decode('UTF-8')
            
            if  "received!" in ACK:
                print(str(ACK))
                frame+=1
        
        except Exception as e:
            print("Exception Raised\n")
            sockt.close()
            exit(0)
        except KeyboardInterrupt as e:
            print("Server Closed\n")
            exit(0)
        except ConnectionResetError as e:
            print("Connection Closed\n")
            sockt.close()
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

def main_Algorithm():    
    data = "Data Send!"
    frames = Frames(data)
    Sending_Frames(frames)  

                
    
    print("Connection Closed")  # closing connection
   
if __name__ == "__main__":
    main_Algorithm()
