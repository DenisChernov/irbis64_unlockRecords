__author__ = 'demiin'
import socket
import datetime

counter = 1;
bases = ['OLDEK', 'RETRO', 'CKC', 'RDR']
SERVER = "192.168.9.249"
log = open("/tmp/unlock_irbis64_records", "w")
log.write(str(datetime.datetime.now()) + "\n")
### First step - connect   ####################
msg_connect = "\nA\nA\nA\n31771\n" + str(counter) + "\n" + "9f9@7Nuq\nirbisoft\n\n\n\n" + "irbisoft\n9f9@7Nuq"
msg_connect = str(len(msg_connect) - 1) + msg_connect
sock = socket.socket()
sock.connect((SERVER, 6666))
sock.send(msg_connect)
data = sock.recv(64000)
sock.close()
print("connected")
log.write("connected to: " + SERVER + "\n")

### Steps - get list blocked   ###########

for bd in range(0, len(bases)):
#for bd in range(0, 1):
    counter += 2
    msg_listBlocked = "\n0\nA\n0\n31771\n" + str(counter) + "\n" + "9f9@7Nuq\nirbisoft\n\n\n\n" + bases[bd]
    msg_listBlocked = str(len(msg_listBlocked) - 1) + msg_listBlocked
    sock = socket.socket()
    sock.connect((SERVER, 6666))
    sock.send(msg_listBlocked)

    data = ""
    buf = "1"
    while buf != "":
        buf = sock.recv(1024)
        if buf != "":
            data += buf

    sock.close()
    print("get blocked from: " + bases[bd])
    log.write("get blocked from: " + bases[bd] + "\n")

### Steps - unblock   ####################
    counter += 2
    msg_Unblock = "\nQ\nA\nQ\n31771\n" + str(counter) + "\n" + "irbisoft\n9f9@7Nuq\n\n\n\n" + bases[bd] + "\n"
    data = data.split("\n")
    #print(data[14])
    if data[14] != "":
        data = data[14].split('\x1E')
        if data[0] != '\r':
            print(bases[bd] + ": ")
            print(data)
            log.write("count blocked records: " + str(len(data)) + "\n")
            for i in range(0, len(data)):
                msg_Unblock += str(data[i])
                if i < (len(data) - 1):
                    msg_Unblock += "\x0A"

            msg_Unblock = str(len(msg_Unblock) - 1) + msg_Unblock
            sock = socket.socket()
            sock.connect((SERVER, 6666))
            sock.send(msg_Unblock)
            data = ""
            buf = "1"
            while buf != "":
                buf = sock.recv(1024)
                if buf != "":
                    data += buf
            sock.close()
        else:
            print(bases[bd] + " has no blocked records")
            log.write(bases[bd] + " has no blocked records" + "\n")

### Last step - disconnect   ################
msg_disconnect = "\nB\nA\nB\n31771\n" + str(counter) + "\n" + "9f9@7Nuq\nirbisoft\n\n\n\n" + "irbisoft\n9f9@7Nuq"
msg_disconnect = str(len(msg_disconnect) - 1) + msg_disconnect
sock = socket.socket()
sock.connect((SERVER, 6666))
sock.send(msg_disconnect)
data = sock.recv(64000)
sock.close()
print ("disconnect")
log.write("disconnect" + "\n")
log.close()