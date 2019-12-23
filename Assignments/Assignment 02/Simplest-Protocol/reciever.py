import socket                
import time
frameSize = 5
mainData = ''
def Receiver():
    sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
    PORT = 9001       
    sockt.connect((socket.gethostname(), PORT)) 
    data = sockt.recv(frameSize) 
    data = data.decode("UTF-8")
    print(data)
    
    if data is '':
        sockt.close() 
        return False
    
    global mainData
    mainData += data
    sockt.close()  
    return True

def main():    
   # print("\n\nFRAMES: ",end='')
    while True:
        if not (Receiver()):break
        time.sleep(0.3)

    print("\nData: '"+mainData+"'\n")

main()
