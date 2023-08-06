import os
import sys
import socket
import numpy
import time
import subprocess
from nptdms import TdmsFile
import matplotlib.pyplot as plt
import datetime
from robot.libraries.BuiltIn import BuiltIn

CONFIG_PATH = 'N:/AutomatedLabTest/LabTest-P600/ConfigFiles'
sys.path.append(os.path.join(os.path.abspath(__file__ + "/../../../../../../"),"robotframework",'pylibs'))
sys.path.append(os.path.join(os.path.abspath(__file__ + "/../../../../../../"),"robotframework",'robotlibs'))


def show_figure(tdms_file_path, x_name, y_name):
    base_path = os.path.dirname(tdms_file_path)

    tdms_file = TdmsFile(tdms_file_path)
    for group in tdms_file.groups():
        grp1_data = tdms_file.object('Channel_Data').as_dataframe()

    column_name = list(grp1_data.columns)    # read out column name in 

    if x_name not in column_name:
       raise Exception("the element is not in the list")

    if y_name not in column_name:
       raise Exception("the element is not in the list")

    x_axis_value = list(tdms_file.channel_data('Channel_Data', x_name))
    if x_name in ['MotorCurrentSensorPhaseV','MotorCurrentSensorPhaseU','MotorCurrentSensorPhaseW']:
        x_axis_value = list(map(lambda x: x*1000, x_axis_value))
    elif x_name =='TorqueTransducerOut':
        x_axis_value= list(map(lambda x:x*4,x_axis_value))
    else:
        pass

    y_axis_value = list(tdms_file.channel_data('Channel_Data', y_name))
    if y_name in ['MotorCurrentSensorPhaseV', 'MotorCurrentSensorPhaseU', 'MotorCurrentSensorPhaseW']:
        y_axis_value= list(map(lambda y: y * 1000, y_axis_value))
    elif y_name == 'TorqueTransducerOut':
        y_axis_value = list(map(lambda y: y * 4,y_axis_value))
    else:
        pass

    fig = plt.figure(figsize=(12, 6))  # set figure size
    plt.rcParams['agg.path.chunksize'] = 50000

    current_time = datetime.datetime.now()  # get current time

    time = datetime.datetime.strftime(current_time, '%Y_%m_%d__%H_%M_%S')  # change the time format

    fig_title = x_name + "__" + y_name + " Curves_" + time  # combine figure title name

    plt.plot(x_axis_value, y_axis_value, 'g', label=y_name)
    plt.legend()  # display figure legend
    plt.xlabel(x_name)  # set x axis label name
    plt.ylabel(y_name)  # set y axis label name



    plt.title(fig_title)  # set figure title
    plt.grid(True)  # display grid
    fig_name = fig_title + '.png'  # set figure name
    pic_path = os.path.join(base_path, fig_name)  # combine figure path and figure name
    plt.savefig(pic_path)  # save figure to expected path
    if os.path.exists(tdms_file_path):
        os.remove(tdms_file_path)
    return pic_path


class TCP_Server():
    '''
    call high speed sampling exe 'HSS_TCP.exe'

    the exe set up TCP connection and get measured data continously
    '''
    def __init__(self, target_exe='HSS_TCP.exe', data_path='C:\\Autotest\\HS_Data'):
        self.target_exe = target_exe
        self.tcp_process = None
        self.data_path = data_path

    def start_tcp_sever(self, channels):
        '''
        start the tcp server exe, that reads the measured data stream continuously

        channels: high speed sampling channel name list
        '''
        #current_path = os.getcwd()
        current_path = os.path.abspath(__file__)
        cmd_str = os.path.join(current_path, './../', self.target_exe)
        #print(cmd_str)
        
        for s in channels:
            cmd_str = cmd_str + ' ' + s
        
        self.tcp_process = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, encoding='utf-8')

    def get_result_png(self):
        '''
        get the result png path

        if no valid path return, None variable will be returned
        '''

        result_path = self._get_result_from_hs_exe()

        if result_path.strip() != '':
            return result_path
        else:
            return None

    def _get_result_from_hs_exe(self):
        '''
        wait for hs exe finished and get returned value

        if no value returned, an empty string will be returned
        '''
        if self.tcp_process is not None:
            while True:
                if self.tcp_process.poll() is not None:
                    try:
                        out, err = self.tcp_process.communicate(timeout=10)
                    except TimeoutError:
                        self.tcp_process.kill()
                        out, err = self.tcp_process.communicate()
                    finally:
                        #print('out: {}\nerr: {}'.format(out,err))
                        return out
        else:
            return ''


class UDP_client():
    '''
    set up UDP connection to cRIO, send/receive messages to configure cRIO high speed
    sampling and close the connection
    '''
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.send_time = 0

    def msg_send_rev(self, data_array):
        '''
        send command to specified address:port by UDP socket

        1. open UDP socket
        2. send data_array
        3. get feedback
        4. close UDP socket
        '''

        pc_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        send_address = (self.ip_address, self.port)
        rev_address = ('', self.port)
        pc_udp_socket.bind(rev_address)

        pc_udp_socket.settimeout(25)
        self.send_time += 1
        pc_udp_socket.sendto(bytes(data_array), send_address)

        pc_udp_socket.settimeout(5)
        rev_data, rev_addr = pc_udp_socket.recvfrom(1024)
        rev_data_array = list(numpy.frombuffer(rev_data, dtype=numpy.uint8))
        #print('received data: {} \nreceive address: {}'.format(rev_data_array, rev_addr))

        pc_udp_socket.close()
        return (rev_data, rev_addr)

class crio_hs:
    def __init__(self):
        self.computer_name = str.lower(socket.gethostname())
        self.host_config_path = None
        self._kw_to_load = {'Misc.ini' : ['[Encoder]'],'TorqueTransducer.ini' : ['[Torque_Transducer]'], \
            'TestPanel.ini' : ['[TestPanel]', '[Torque_Transducer]'], \
            'InputOutput.ini' : ['[Relays]', '[DigitalInputs]', '[VoltageInputs]', '[CurrentInputs]']}
        for name in os.listdir(CONFIG_PATH):
            if name[:len(self.computer_name)] == self.computer_name:
                self.host_config_path = CONFIG_PATH + '/' + name
                break
        
        self.valid_channel = {}
        self.sampling_rate_hz = numpy.uint32(1000)
        self.UDP_port = 47257
        self.TCP_port = 47259
        self.RIOHOST_BENCH = None
        self.RIOHOST_SECOND = None
        self.HS_ChannelSetup = None
        self.HS_SamplingFreq = None
        self.HS_IP_Address = None

        if self.host_config_path is not None:
            with open(self.host_config_path+'/RIO.ini', 'r') as hs_info:
                for line in hs_info.readlines():
                    line = line[:line.find('#')]
                    if '=' in line:
                        key_word = line[:line.find('=')].strip()
                        if key_word == 'RIOHOST_BENCH':
                            self.RIOHOST_BENCH = line[(line.find('=')+1):].strip()
                        elif key_word == 'RIOHOST_SECOND':
                            self.RIOHOST_SECOND = line[(line.find('=')+1):].strip()
                        elif key_word == 'HS ChannelSetup':
                            self.HS_ChannelSetup = line[(line.find('=')+1):].strip()
                        elif key_word == 'HS SamplingFreq':
                            self.HS_SamplingFreq = line[(line.find('=')+1):].strip()
                            break
                        else:
                            continue

            if self.HS_ChannelSetup is not None:
                hs_crio = self.HS_ChannelSetup.split('\\')[1]
                if hs_crio == 'BENCH':
                    self.HS_IP_Address = self.RIOHOST_BENCH
                else:
                    self.HS_IP_Address = self.RIOHOST_SECOND
            
            self._get_valid_channel()
            self.udp_connection = UDP_client(self.HS_IP_Address, self.UDP_port)
            self.tcp_connection = TCP_Server()

    def start_hs(self, *args, rate=1000):
        '''
        start high speed sampling
        '''

        self._set_sampling_rate_hz(rate)
        channels = []
        for i in args:
            channels.append(str(i))

        hs_channels = self._sampling_chann_filter(channels)
        print('channels to sample {}'.format(hs_channels.keys()))
        stop_cmd_data = self._get_hs_stop_datagram()

        self.udp_connection.msg_send_rev(stop_cmd_data)

        if len(hs_channels) > 0:
            config_hs_cmd_data = self._get_hs_prepare_datagram(hs_channels)
            self.udp_connection.msg_send_rev(config_hs_cmd_data)
            time.sleep(0.5)
            start_cmd_data = self._get_hs_start_datagram()
            self.tcp_connection.start_tcp_sever(hs_channels.keys())
            time.sleep(1)
            self.udp_connection.msg_send_rev(start_cmd_data)

    def stop_hs(self,csv_save=False,x_name=None,y_name=None):
        '''
        stop high speed sampling
        '''
        stop_cmd_data = self._get_hs_stop_datagram()
        self.udp_connection.msg_send_rev(stop_cmd_data)
        time.sleep(1)
        result_path = None

        if str(csv_save).lower() == 'True' or csv_save:
            csv_save = True
        else:
            csv_save = False

        if self.tcp_connection.tcp_process is not None:

            result_path = self.tcp_connection.get_result_png()
            data_path = result_path.split(".")[0]+".tdms"

            self.tcp_connection.tcp_process = None


        print('the final waveform is: {}'.format(result_path))

        if result_path is not None:
            self._attach_image(result_path)

        if csv_save == True:
           if not os.path.exists(data_path):
                raise Exception("data path does not exist")

           pic_path = show_figure(data_path, x_name, y_name)

           if not os.path.exists(pic_path):
               raise Exception("merge picture path does not exist")
           self._attach_image(pic_path)
           print("the merged pic path is:{}".format(pic_path))


    def _set_sampling_rate_hz(self, sampling_rate):
        '''
        set value of sampling_rate_hz, that must be a uint32 value
        '''
        self.sampling_rate_hz = numpy.uint32(sampling_rate)

    def _get_valid_channel(self):
        '''
        get all supporting high speed sampling channels on current bench

        get information from config files:
        RIO.ini; Misc.ini; TestPanel.ini; InputOutput.ini
        all suported channels and channel information are stored in dict self.valid_channel
        '''
        self.valid_channel = {}
        if self.host_config_path is None:
            print('No configurarion file folder exists of current pc {}'.format(self.computer_name))
        elif (self.HS_ChannelSetup is None) or (self.HS_SamplingFreq is None):
            print('High speed sampling is NOT squpported on current bench {}'.format(self.computer_name))
        else:
            for f_name in self._kw_to_load.keys():
                f_path = self.host_config_path + '/' + f_name
                block_name = self._kw_to_load[f_name]
                if os.path.exists(f_path):
                    valid_part = False
                    with open(f_path, 'r') as channel_file:
                        for line in channel_file.readlines():
                            if valid_part is True:
                                line = line[:line.find('#')].strip()
                                if '=' in line:
                                    self.valid_channel[line[:line.find('=')].strip()] = line[(line.find('=')+1):].strip()
                                elif (line == '') or (line.strip() in block_name):
                                    continue 
                                else:
                                    valid_part = False
                            else:
                                if line.strip() in block_name:
                                    valid_part = True

    def _sampling_chann_filter(self, channel_list):
        '''
        select all supported channels in 'channel_list'
        '''

        filtered_channel = {}

        for chann in channel_list:

            if chann in self.valid_channel.keys():
                filtered_channel[chann] = self.valid_channel[chann]

        
        return filtered_channel

    def _get_hs_prepare_datagram(self, channel_list):
        '''
        construct the command that used to configure high speed sampling channels
        '''

        func = self.HS_ChannelSetup.split('\\')[-1]
        data_array = []

        for chann in channel_list:
            chann_info_list = self.valid_channel[chann].split(' ')
            if chann_info_list[0].split('\\')[-1] == 'ENC':
                data_array = data_array + list(numpy.frombuffer('ENCPOS  '.encode(), dtype=numpy.uint8))
            elif (chann_info_list[0].split('\\')[-1]).startswith('SD'):
                chann_str = 'SDI-0' + chann_info_list[1] + '0' + chann_info_list[2]
                data_array = data_array + list(numpy.frombuffer(chann_str.encode(), dtype = numpy.uint8))
            else:
                chann_str = 'AIC-0' + chann_info_list[1] + '0' + chann_info_list[2]
                data_array = data_array + list(numpy.frombuffer(chann_str.encode(), dtype = numpy.uint8))

        data_array = list(numpy.frombuffer(func.encode(), dtype=numpy.uint8)) + [0x00, 0x00, len(channel_list)] + data_array

        head = [0x75, len(data_array), numpy.uint8(sum(data_array)), numpy.uint8(self.udp_connection.send_time), \
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        
        return (head + data_array)

    def _get_hs_start_datagram(self):
        '''
        construct high speed sampling start command
        '''
        func = self.HS_SamplingFreq.split('\\')[-1]
        data_array = list(numpy.frombuffer(func.encode(), dtype=numpy.uint8)) + [0x00, 0x00]
        freq_u8_array = [numpy.uint8(self.sampling_rate_hz // 0x1000000), numpy.uint8(self.sampling_rate_hz // 0x10000), \
            numpy.uint8(self.sampling_rate_hz // 0x100), numpy.uint8(self.sampling_rate_hz % 0x100)]

        data_array = data_array + freq_u8_array
        head = [0x75, len(data_array), numpy.uint8(sum(data_array)), numpy.uint8(self.udp_connection.send_time), \
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        return (head + data_array)

    def _get_hs_stop_datagram(self):
        '''
        construct high speed sampling stop command
        '''
        func = self.HS_SamplingFreq.split('\\')[-1]
        data_array = list(numpy.frombuffer(func.encode(), dtype=numpy.uint8)) + [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        head = [0x75, len(data_array), numpy.uint8(sum(data_array)), numpy.uint8(self.udp_connection.send_time), \
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

        return (head + data_array)

    def _attach_image(self, filepath):
        BuiltIn().log(message="<img src='{}'/>".format(filepath), html=True)
   
if __name__ == "__main__":

    cRIO_hs = crio_hs()
#    print(os.path.join(os.path.abspath(__file__ + "/../../../../../"),"robotframework",'pylibs'))

    cRIO_hs.start_hs('EncoderConnectedDUT', 'MotorCurrentSensorPhaseV', 'T27DigitalInput')
    time.sleep(10)
    cRIO_hs.stop_hs()