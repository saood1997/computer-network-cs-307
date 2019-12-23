import socket                
import time, sys
def sending_Frames(frames):
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          

    PORT = 9001
    try:         
        sockt.bind((socket.gethostname(), PORT))         
    except(socket.error ):
        print("Port binding error\n")
        exit()
    sockt.listen(5)      
    for i in frames:
        c, addr = sockt.accept()      
        c.send(bytes(i,"utf-8")) 
        c.close()


frameSize = 5


def Frames(data):
    frames = []
    if len(data) > frameSize:
        for i in range(0,len(data),frameSize):
            frame = data[i:i+frameSize]
            frames.append(frame)
    else:
        frames.append(data)
    frames.append('')
    return frames

def Simplest_Protocol():
    
    data = "Data Send"   # data to be sent
    frames = Frames(data)
    print("Sending Frames....")
    sending_Frames(frames)  # sending frames to reciever
    
    
    print("Connection Closed!")
   

Simplest_Protocol()
