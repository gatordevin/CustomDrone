import socket
import time
class SBUSUDP:
    def __init__(self, ip=None):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.newChannels = [1024] * 16
        self.oldChannels = []
        self.ip = ""
        if(ip == None):
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            splitted = IPAddr.split(".")
            ipSearch = ""
            for i in range(len(splitted) - 1):
                ipSearch += splitted[i] + "."
            for i in range(0, 101):
                ips = ipSearch + str(i)
                data = bytearray(4)
                data[0] = ord('H')
                data[1] = ord('A')
                data[2] = ord('N')
                data[3] = ord('D')
                self.client_socket.sendto(data, (ips, 6666))
                try:
                    self.client_socket.settimeout(0.01)
                    data = self.client_socket.recvfrom(256)
                    if (data != None):
                        self.ip = ips
                        break
                except:
                    None
        else:
            self.ip = ip
        print(self.ip)
        self.timeSent = time.time()



    def create_BEAT(self):
        data = bytearray(4)
        data[0] = ord('B')
        data[1] = ord('E')
        data[2] = ord('A')
        data[3] = ord('T')
        return (data)

    def findDevice(self):
        self.client_socket.sendto(self.create_BEAT(), (self.ip, 6666))

    def createPacket(self, channels):
        chan = []
        chan.append(ord('S'))
        chan.append(ord('B'))
        chan.append(ord('U'))
        chan.append(ord('S'))
        for i in channels:
            LSB = int(i) & 0xff
            MSB = (int(i) >> 8) & 0xff
            chan.append(LSB)
            chan.append(MSB)
        checksum1 = 0
        for byte in chan:
            checksum1 = checksum1 ^ byte
        checksum1 = checksum1 & 0xFE
        checksum2 = (~checksum1) & 0xFE
        chan.append(checksum2)
        chan.append(checksum1)
        # print(chan)
        return chan

    def sendUDP(self, channels):
        channels = bytearray(self.createPacket(channels))
        self.client_socket.sendto(channels, (self.ip, 6666))


