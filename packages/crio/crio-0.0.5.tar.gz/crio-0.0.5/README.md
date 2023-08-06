## How to install 
pip install crio

## How to use:

from crio import crio

a = crio()

### Examples:
 
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



