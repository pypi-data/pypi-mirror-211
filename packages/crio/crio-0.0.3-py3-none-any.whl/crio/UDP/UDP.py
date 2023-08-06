import struct
import binascii
import socket
import sys

python_version = sys.version_info.major

class UDP:
    def __init__(self):
        self.send_times = 0

        self.telegram_array_send = []
        self.telegram_array_recv = []
        self.send_addr = ()
        self.recv_addr = ()

    def send(self, addr, function, channel, device, value=None, timeout=False):
        self.send_addr = addr   
        command = self.__handle_command(function, channel, device, value=value, timeout=timeout)     
        # self.__send_cmd()
        print(self.telegram_array_send)
        return

        try_times = 0
        while try_times < 5:    # Try send message 5 times, if there is still error, then raise error
            try:
                self.__response_error_check()
                break
            except Exception as e:
                raise Exception ("{}".format(e))

        value, time_stamp = self.__handle_response()
        return value, time_stamp    # Return value and time stamp

    def __handle_command(self, function, channel, device, value=None, timeout=None):
        '''
        #:
        Handle read/write command
        Deal the difference between read and write in this method
            when it's write, all parameter

        Parameter:
            function:
            channel:
            device:
            value:
            timeout:


        format will be as below:
            byte0:      Head must be 0x75 (DEC 117), a fixed number
            byte1:      Length of the data, 
                        contains function, device number, channel number, data and timeout
                        will be calculated internally
            byte2:      check sum, will be calculated internally
            byte3:      command executation time, should be an attribute of current class, every time run this function, the number plus 1
            byte4~11:   time stamp, will be always 0
            byte12~14:  three upper letters function. (for example: SDO), will be pass by a parameter input
            byte15:     channel number, will be pass by a parameter input
            byte16:     device number, will be pass by a parameter input
            byte17~?:   value, could be a boolean (1 byte) or a double float (8 bytes),
            byte_end:   timeout, will be pass by a parameter input, 1 for true, 0 for false
        '''

        self.telegram_array_send = [0x75]             # byte0
        data = []       # data_combine contain function ascii array, channel number, device number, value and timeout if exist
        
        # Combine function, channel number, device number, value and timeout to data array
        for i in function:      # Translate parameter "function" to ascii array
            d = ord(i)
            data.append(d)      # byte 12~14

        data.append(channel)    # byte 15
        data.append(device)     # byte 16

        if value != None:   # pack double type value to 8 bytes array
            if type(value) != bool:
                bs = struct.pack("d",value)
                if python_version == 3:
                    if(function == "TMR"):
                        value_b = [bs[7], bs[6], bs[5], bs[4], bs[3], bs[2], bs[1], bs[0],50]
                    else:
                        value_b = [bs[7],bs[6],bs[5],bs[4],bs[3],bs[2],bs[1],bs[0]]
                elif python_version == 2:
                    value_b = [ord(bs[7]),ord(bs[6]),ord(bs[5]),ord(bs[4]),ord(bs[3]),ord(bs[2]),ord(bs[1]),ord(bs[0])]
            else:   # Change value from boolean to array with only 1 element, 1 for True, 0 for False
                if value == True:
                    value_b = [1]
                else:
                    value_b = [0]
            data.extend(value_b)    # byte 17~?

        if timeout !=None:      # To a read command, there is no timeout, to a write command timeout could be True or False
            if timeout == True:
                data.append(1)
            elif timeout == False:
                data.append(0)      # byte_end

        check_sum = self.__check_sum(data)  # Calculate check sum of whole combined data

        data_lens = len(data)   # get lens of whole combined data

        self.telegram_array_send.append(data_lens)    # Byte 1
        self.telegram_array_send.append(check_sum)    # Byte 2
        self.telegram_array_send.append(self.send_times)  # Byte 3
        self.telegram_array_send.extend([0,0,0,0,0,0,0,0])    # Byte 4~11
        self.telegram_array_send.extend(data)     # Byte 12~end, combined data

    def __send_cmd(self):
        '''
        This is a internal function:
            To send a command and recieve response
            Every time read/write cRio, there must be a sendto and a recvfrom
            
            Error check should be done here. 
        '''
        try:
            udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   # Create a socket
            udp_socket.settimeout(3)
            udp_socket.bind(("", self.send_addr[1]))     # Bind local host ("" means local host) and port of current PC for recieving message
            if python_version == 2:     # Deal the differency of python 2 and python 3
                send_message = b''
                for data in self.telegram_array_send:
                    send_message = send_message + chr(data)
            elif python_version == 3:
                send_message = bytes(self.telegram_array_send)

            udp_socket.sendto(send_message, self.send_addr)     # Send message to cRio, with ip address and port of cRio, port is fixed, ip address is changable
            self.send_times = (self.send_times + 1)%256    # Count send times, every time send a message, counter plus 1, must always in 0~256
            recv_message, self.recv_addr = udp_socket.recvfrom(1024)  # Recieve message from local host and port, parameter is buffer size.
            self.telegram_array_recv = list(map(lambda x: (x), recv_message))     # Transform recv message (byte type) to byte array
            udp_socket.close()      # Close socket
        except Exception as e:
            udp_socket.close()      # Close socket
            raise Exception ("{}".format(e))
        

    def __handle_response(self):       
        time_stamp_bytes = self.telegram_array_recv[4:12]
        value_bytes = self.telegram_array_recv[12:]    
        
        ba = bytearray()    # Transform time stamp from byte array to float
        for h in time_stamp_bytes:
            ba.append(h)
        time_stamp = struct.unpack("!d",ba)[0]

        if len(value_bytes) == 0:
            value = None
        elif len(value_bytes) == 1:
            value = bool(value_bytes[0])
        elif len(value_bytes) == 8:  
            ba = bytearray()    # Transform time stamp from byte array to float
            for h in value_bytes:
                ba.append(h)
            value = struct.unpack("!d",ba)[0]

        elif len(value_bytes) == 16:            
            value = value_bytes
        
        return value, time_stamp

    def __response_error_check(self):
        data_recv = self.telegram_array_recv[12:]
        data_lens = len(data_recv)
        check_sum = self.__check_sum(data_recv)

        ''' TODO
            Evaluate which method is better to deal with error.
                raise Exception will block program
                it looks better to return the error code as an output

                if structure can only return one fail reason, do we need to return all errors?
        '''
        if self.recv_addr[0] != self.send_addr[0]:   # Check if this message is from cRio IP address
            raise Exception ("Recieve telegram IP address is wrong!")
        elif self.recv_addr[1] != self.send_addr[1]:   # Check if this message is from cRio specific port
            raise Exception ("Recieve telegram port is wrong!")
        elif self.telegram_array_recv[0] != 0x75:    # Check if telegram head equals 0x75
            raise Exception ("Telegram head is wrong!")
        elif self.telegram_array_recv[1] != data_lens:   # Check if data lens is correct
            raise Exception ("Data lens is wrong!")
        elif self.telegram_array_recv[2] != check_sum:   # Check if check sum is correct
            raise Exception ("Check sum is wrong!")
        elif self.telegram_array_recv[3] != self.telegram_array_send[3]:  # Check if send times equals
            raise Exception ("Send times wrong!")        

    def __check_sum(self, data):
        check_sum = sum(data)
        check_sum &= 0xFF         
        return check_sum