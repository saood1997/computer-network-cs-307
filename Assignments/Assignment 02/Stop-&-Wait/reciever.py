import socket      
 
sockt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     

PORT = 2203

dest = (socket.gethostname(), PORT)   # ip & port
try:      
    sockt.connect((socket.gethostname(), PORT))
except socket.error:
    print('Conection Refused\n') 
    exit(0)

frameSize = 5
mainData = ''
ACK = 1

def receiver():
    data = ""
    try:
        global ACK,mainData
        data = sockt.recv(frameSize).decode('UTF-8')
      
        if data == '}^{':
            send_ack = 'ACK Received' 
            sockt.send(bytes(send_ack,'UTF-8'))
            return False
        
        send_ack = "ACK Received!"+" of frame "+ str(ACK)
        sockt.send(bytes(send_ack,'UTF-8'))
        ACK  += 1

    except Exception as e:
        print("exception Raised!!!")
        sockt.close()
        exit(0)
    except KeyboardInterrupt as e:
        print("Connection Closed")
        sockt.close()
        exit(0)
    print(data)
    mainData += data
    return True


def main():    
    print("\nFRAMES : ",end='')
    while True:
        if not (receiver()):break
    sockt.close()
    print("\nComplete Data: '"+mainData)
main()