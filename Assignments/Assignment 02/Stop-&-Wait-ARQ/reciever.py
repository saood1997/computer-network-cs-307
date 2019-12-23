import socket      
import time, sys   

sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     

PORT = 3165  

dest = (socket.gethostname(), PORT)   # ip and port
try:      
    sockt.connect((socket.gethostname(), PORT))
except socket.error:
    print("Conection Refused!!!\n") 
    exit(0)


frameSize = 5
mainData = ''
ACK = 1

def Receiver():
    sockt.settimeout(0.5)

    try:
        global ACK,mainData
        data = socket.recv(frameSize).decode('UTF-8')
        if data == '}^{':
            send_ack = "ack received!"+" of end frame. " 
            sockt.send(bytes(send_ack,'UTF-8'))
            return False
        print(data)
        mainData += data
        send_ack = "ACK Received! "+ str(ACK)
        sockt.send(bytes(send_ack,'UTF-8'))
        ACK += 1
    except socket.timeout:
        send_ack = "Timeout!!!"
        sockt.send(bytes(send_ack,'UTF-8'))
    except Exception as e:
        print(str(e))
        sockt.close()
        exit(0)
    except KeyboardInterrupt as e:
        print("connection closed")
        sockt.close()
        exit(0)
    
    return True

def main():
    while True:
        if not (Receiver()):break

    sockt.close()
    
    print("\Main Data: '"+mainData+"'\n")