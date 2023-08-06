#import os
import sys
import time
import logging
import json
from importlib.resources import files
import UDP

'''
try:
    from utility.getdata import config
except Exception as e:
    DIRPATH = os.path.join(os.path.abspath(__file__ + "/../../../../../"),"robotframework",'pylibs')
    sys.path.append(DIRPATH)
    from utility.getdata import config
'''
'''
try:
    from .crio_hs import crio_hs
except Exception as e:
    print(e)
    from crio_hs import crio_hs
'''

import time

CONFIG_STRING_ERROR = 100
CONFIG_ROUTE_ERROR  = 101

boolValue={'true':True,'false':False,'True':True,'False':False, True:True, False:False}

logger = logging.getLogger(__name__)

def loadJson(path):
    with open(path,'r') as f:
        f_dict = json.load(f)
        return f_dict

class crio():
    def __init__(self):
        self.UDP = UDP.UDP()
        jsonpath = files('config').joinpath('iniconfig.cfg')
        #self.iniData = iniData(manualImport,manualPath).iniDataDic
        self.iniData = loadJson(jsonpath)
        self.funcCode = {'SDO','SDI','AOV','TMR','AOC','ENC'}
        #self.chs = crio_hs() #high speed sampling instance

    def _serial_common(self,config_string='',value = None):
        '''
        Function:    handle the crio DIO/AIO/PIO command

        param config_string: 
        | The key name for terminal info in the inifile data dist |
        param value: 
        | The value to be set, this can be BOOL/Double/Uint |
        return: 
        | DIO/AIO/PIO value and time stamp |
        '''        
        config_string = config_string.lower()
        if( not((config_string) in self.iniData.keys())):
            return CONFIG_STRING_ERROR
        
        config_string = config_string.lower()
        send_terminalInfo = self.iniData[config_string]                      # get terminal config info, example 'cRIO\BENCH\SDO 7 0'
        confstr = send_terminalInfo.split('\\')                                         # convert config info to ['cRIO','BENCH','SDO 7 0']
        send_addr = (self.iniData['riohost_'+ confstr[1].lower()], 47257)    # get current bench ip addr
        send_function = confstr[2].split(' ')[0]                                        # example SDO/SDI

        if(send_function in self.funcCode):
            send_channel = int(confstr[2].split(' ')[2])
            send_device = int(confstr[2].split(' ')[1])

        print(config_string, send_addr, send_function, send_channel, send_device, value)
        return self.UDP.send(send_addr, send_function, send_channel, send_device, value, timeout=False)
        time.sleep(0.05)

    def configure_route(self,config_string='',connect = True):
        '''
        function: handle the crio DIO/AIO/PIO route
        
        param config_string: 
        | The key name for terminal info in the inifile data dist |
        param connect: 
        | if True, the connect value will be read from the inifile(+/connect  -/disconnect) |
        | if False, all termianl will be disconnect |
        return:
        | DIO/AIO/PIO value and time stamp |
        '''
        config_string = config_string.lower()
        if(config_string not in self.iniData.keys()):
            return CONFIG_STRING_ERROR

        if( config_string in self.iniData.keys() and         
            self.iniData[config_string][0:4] == 'cRIO'):         # check if the config_string is a crio string or a subConfigString for crio
            return self._serial_common(config_string, connect)

        route = self.iniData[config_string]      # get config route info, example 'T32_Encoder_Relay- OptionB_Relay1- OptionB_Relay2-'
        routeList = route.split(' ')
        for switch in routeList:
            if(connect == True):
                if(switch[-1] == '+'):
                    value = True
                elif(switch[-1] == '-'):
                    value = False
            else:
                value = False
            self._serial_common(switch[:-1].lower(), value)
            
    def digital_output(self,terminalName,value=False):
        '''
        Function:    output digital signal from crio

        Example:  set terminal 18 digital output to True
        | digital_output | 't18digitalinput' | True |     
        '''
        return self._serial_common(terminalName, boolValue[value])

    def digital_input(self,terminalName):
        '''
        Function:    read digital signal from drive

        Example:  get terminal 18 digital input from drive
        | ${parameter_value}= | digital_input | 't18digitaloutputput' |    
        '''
        return self._serial_common(terminalName)

    def current_input(self, terminalName):
        '''
        Function:    read current signal from drive

        Example:  get terminal 18 current input from drive
        | ${parameter_value}= | current_input | 't18currentoutput' |    
        '''
        return self._serial_common(terminalName)

    def current_output(self, terminalName,value=0.0):
        '''
        Function:    output current signal to drive

        Example:  output terminal 18 current to drive with 9mA
        | current_output | 't18currentinput' | 0.009 |   
        '''
        return self._serial_common(terminalName,value)

    def analog_output(self, terminalName, value=0.0):
        '''
        Function:    output analog signal to drive

        Example:  output terminal 18 to drive with 4v
        | analog_output | 't18analoginput' | 4 |   
        '''
        return self._serial_common(terminalName, value)

    def analog_input(self, terminalName):
        '''
        Function:    read analog signal from drive

        Example:  get terminal 18 analog input from drive
        | ${parameter_value}= | analog_input | 't18analogoutput' |    
        '''
        return self._serial_common(terminalName)

    def pulse_input(self, terminalName):
        '''
        Function:    get pulse input signal from drive

        Example:  get terminal 18 pulse input from drive
        | ${parameter_value}= | pulse_input | 't18pulseoutput' |    
        '''
        return self._serial_common(terminalName)

    def pulse_output(self, terminalName, value=0):
        '''
        Function:    output pulse signal to drive

        Example:  output terminal 18 pulse to drive with 3000
        | pulse_output | 't18analoginput' | 3000 |           '''

        return self._serial_common(terminalName, value)

    def encoder(self, configstring=''):  
        '''
        Function:    get the motor speed from the encoder, return the speedRPM

        '''     
        value, time_stamp = self._serial_common(configstring)
        speedRPM = value[0]<<24|value[1]<<16|value[2]<<8|value[3]
        return speedRPM,time_stamp

    # def load_signal(self,T27Value,T32Value,T33Value,T29Value=''):
    #     '''
    #     Function:    output control signal to load drive
    #     | T32Value:loaddrivestart | T33Value:loaddrivestartreverse | T27Value:loaddrivecoastinverse | 
    
    #     '''        
    #     self.digital_output('loaddrivestart',boolValue[T32Value])
    #     self.digital_output('loaddrivestartreverse',boolValue[T33Value])
    #     self.digital_output('loaddrivecoastinverse',boolValue[T27Value])        

    # def load_setup_mode(self,bit0,bit1):
    #     '''
    #     Function:    set load drive mode
    #     | bit0=1 | Toque closed loop | bit0=0 Speed closed loop | 
    
    #     '''
    #     self.digital_output('loaddrivesetupbit0',boolValue[bit0])
    #     self.digital_output('loaddrivesetupbit1',boolValue[bit1])

    # def load_reference(self,ref=0.0,control_source='current'):
    #     '''
    #     Function:    set load drive reference

    #     Example: set load drive reference to 10%
    #     | load_drive_reference | 10 |  
    
    #     '''
    #     if(control_source == 'voltage'):
    #         return self.analog_output('loaddrivevoltagereference',ref/10)           # 10V = 100% 
    #     elif(control_source == 'current'):
    #         return self.current_output('loaddrivecurrentreference',ref*0.02/100)    # current/50 = 100%


#####################################################################################################
#---------------------------------New Keywords to fit commonbench-----------------------------------#
# To decouple the code, the following code only use "self.configure_route" and "self._serial_common"
# TODO: In future, maybe some functions above can be deleted, (Need to discuss)
#####################################################################################################

    def _load_mode(self, load_type):
        if load_type == 'speed':
            self._serial_common('loaddrivesetupbit0', False)
        elif load_type == 'torque':
            self._serial_common('loaddrivesetupbit0', True)
        else:
            raise Exception("Didn't support load type {}".format(load_type))

    def _load_control(self, function):
        if function == 'start':
            self._serial_common('loaddrivecoastinverse', True)
            self._serial_common('loaddrivestart', True)
            self._serial_common('loaddrivestartreverse', False)
        elif function == 'reverse':
            self._serial_common('loaddrivecoastinverse', True)
            self._serial_common('loaddrivestartreverse', True) 
            self._serial_common('loaddrivestart', False)
        elif function == 'stop':
            '''
            Maybe do not need a stop, coast can replace stop, need to discuss
            '''
            self._serial_common('loaddrivecoastinverse', True)
            self._serial_common('loaddrivestartreverse', False) 
            self._serial_common('loaddrivestart', False)            
        elif function == 'coast':
            self._serial_common('loaddrivecoastinverse', False)
            self._serial_common('loaddrivestartreverse', False) 
            self._serial_common('loaddrivestart', False)           
        else:
            raise Exception("Didn't support {}".format(function))
    
    def _load_ref(self, value):
        '''
        To simplify the load ref function, always use a current as reference source
        value input must be a percentage of reference
        '''
        self._serial_common('loaddrivecurrentreference', value*0.02/100)  # 10V = 100%

    def power(self, state):
        if state == 'on':
            self.configure_route("PowerOnDUT")
        elif state == 'off':
            self.configure_route("PowerOffDUT")
        elif state == 'cycle':
            self.configure_route("PowerOffDUT")
            time.sleep(12)
            self.configure_route("PowerOnDUT")
            time.sleep(5)

    def pick(self, device_type, device=0):
        '''
        This function is used to switch bench to the correct device.

        Parameters:
            device_type:    Choose which device need to be switched, only support drive and motor, other type will raise error.
            device:         Name of device. Device name must be in benchinfo.json file 
        '''
        if device_type == 'Drive':
            # drives = self.conf.support_drives()
            index = drives.index(device) + 1
            Drawer = "Drawer{}".format(str(index))
            self.configure_route(Drawer, True)
            logger.info("Switch to {}".format(Drawer))

        elif device_type == 'Motor':
            # motors = self.conf.support_motors()
            if device=='1K5AM':
                self.configure_route("InternalMotor", True)
            else:
                device = device.lower()
                key = "switchinmotor_{}".format(device)
                self.configure_route(key, True)
            
            logger.info("Switch to {} Motor".format(device))
            self.connect_motor()

        elif device_type == 'Load':
            if device == 'Simple Load':
                self.configure_route('LoadDriveMains', connect=True)    # Connect load drive
                self._load_mode('torque')
                self._load_control('coast')
                self._load_ref(0)
            else:
                logger.info("Crio only support simple load, do nothing here")

        else:
            raise Exception("Crio doesn't support pick {}".format(device_type))

    def connect_motor(self):
        self.configure_route("MotorPhaseU", True)
        self.configure_route("MotorPhaseV", True)
        self.configure_route("MotorPhaseW", True)

    def disconnect_motor(self):
        self.configure_route("MotorPhaseU", False)
        self.configure_route("MotorPhaseV", False)
        self.configure_route("MotorPhaseW", False)

    def start_load(self, load_type):
        self.load_type = load_type
        self._load_control('coast')
        time.sleep(0.2)
        self._load_mode(self.load_type)
        self._load_ref(0)
        self._load_control('start')

    def set_load_value(self, start_value, stop_value=0.0, ramp_time=0.0):
        value = float(start_value)
        value_end = float(stop_value)
        t_ramp = float(ramp_time)

        # Translate torque or speed to a percentage reference
        load_nom_torque = 16        # Norminal torque of crio bench, all bench are the same
        load_nom_speed = 2000       # Norminal speed of crio bench, all bench are the same
        if self.load_type == 'speed':
            value = round((value/load_nom_speed)*100, 2)
            value_end = round((value_end/load_nom_speed)*100, 2)
        elif self.load_type == 'torque':
            value = round((value/load_nom_torque)*100, 2)
            value_end = round((value_end/load_nom_torque)*100, 2)
        else:
            raise Exception("Didn't support load type {}".format(self.load_type))

        # the sub function is used to realize wait until time
        def wait_until_time(time_ms, time_step):
            """
            A wait function
            """
            time_stamp = int(round(time.time() * 1000))
            while (time_stamp - time_ms) < time_step:
                # wait 100ms each loop
                time.sleep(0.1)
                time_stamp = int(round(time.time() * 1000))

            millis = int(round(time.time() * 1000)) - time_ms

        if t_ramp > 0.0:    # Which means the load will follow a ramp
            time_step = 0.1
            steps = t_ramp / time_step
            load_step = (value_end - value) / steps
            load_value = value + load_step
            last_load_value = 0   

            for _ in range(0, int(steps)):
                time_ms = int(round(time.time() * 1000))
                abs_load_value = abs(load_value)    # crio didn't support negative value, so here use abs value

                if load_value < 0 and last_load_value >= 0:
                    self._load_control('reverse')
                elif load_value >= 0 and last_load_value < 0:
                    self._load_control('start')
                else:
                    pass

                self._load_ref(abs_load_value)
                last_load_value = load_value    # Use to verify if drive need to turn reverse
                load_value = round((load_value + load_step), 4)
                wait_until_time(time_ms, time_step * 1000)
                
        else:   # Which means the load will be added directlly
            abs_value = abs(value)
            if value < 0:
                self._load_control('reverse')
                self._load_ref(abs_value)
            else:
                self._load_control('start')
                self._load_ref(abs_value)

    def stop_load(self):
        self._load_control('coast')        # Coast load drive
        self._load_ref(0)          # Set load reference to 0
        self._load_mode('torque')       # Set load type to torque

    def set_digital_output(self, terminal, value, invert_value=None, **kwargs):
        value =True if value == "True" else False
        if invert_value == True:
            value = bool(1-value)
        return self._serial_common(terminal, boolValue[value])

    def get_digital_input(self, terminal):
        return self._serial_common(terminal)

    def set_analog_output(self, terminal, value, **kwargs):
        return self._serial_common(terminal, value)

    #----------------------keyworda merged from crio_hs----------------------#
    def start_capture(self,rate=1000, *signals ):
        self.chs.start_hs(*signals, rate)

    def stop_capture(self,csv_save=False,**kwargs):


        x_name = kwargs.get('x', None)
        y_name = kwargs.get('y', None)

        self.chs.stop_hs(csv_save,x_name,y_name)


if __name__=="__main__":
    c=crio()

    #Bench 初始化的步骤，例如初始化Bench，将DUT切换到Drawer1,并上电。
    c.configure_route("ClearMotorShorts",True)
    c.configure_route("ResistorBrakeShorted",False)    
    c.configure_route("ResistorBrakeConnect",True)
    c.configure_route('InternalMotor',True)
    c.configure_route('MotorPhasesNormal',True)
    c.configure_route('MainsNetRoute',True)
    c.configure_route('LoadDriveMains', connect=True)
    c.configure_route('Drawer1',True)
    c.power('on')

    #Bench 配置连接电机类型的步骤，苏州Bench可用电机有1K5AM和1K8PM，对应1.5K AM电机和1.8k PM电机   
    c.pick('Motor', '1K5AM') 

    #Bench 连接电机U V W项的步骤
    c.connect_motor() 

    #Bench向Drive输出开关量
    c.set_digital_output('t18digitalInput', 0, invert_value=None)

    #Bench采集Drive所输出的开关量
    value = c.digital_input('t27digitaloutput')

    #Bench向Drive输出模拟量（电压）
    c.configure_route("t53voltageinputroute",True) #这步会先配置通路，确定电压通道与Drive相连（如需要输出电流，配置电流通道）
    c.analog_output("t53voltageinput",value=5.0)

    #Bench采集Drive输出的电压
    a = c.analog_input("t50voltageoutput")

