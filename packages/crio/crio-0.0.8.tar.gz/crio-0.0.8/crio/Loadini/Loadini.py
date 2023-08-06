
import configparser
import os
import socket
'''
class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
'''

class iniData():
    def get_inifile_path(self):
        ConfigFilePath = 'N:/AutomatedLabTest/LabTest-P600\ConfigFiles\\'

        # Get current pc number
        pcNum = socket.getfqdn(socket.gethostname())      #pcxxxxxxx.danfoss.net
        pcNum = pcNum[0:9]
        pcNum = pcNum.lower()
        # Get inifile folder name for current pc
        for filefolder in os.listdir(ConfigFilePath):
            if pcNum in filefolder:
                return (ConfigFilePath+filefolder)

    def reload_inifile_configuration(self, manualImport=False, manualPath = ""):
        iniDataArr = []                                              # To save the iniData as list
        configer = configparser.ConfigParser()                       # create a ini file obj
        fileList = ['Drawers.ini','HS.ini','InputOutput.ini','LoadDrive.ini','Misc.ini','MotorData.ini','RIO.ini','Sensor.ini','SwitchBoard.ini','TestPanel.ini']
        if(not manualImport):
            path = self.get_inifile_path()
        else:
            path = manualPath
        for file in os.listdir(path):            # get all inifile in this folder
            if (file in fileList):

                configer.read(path +'\\'+ file)       # load one inifile
                sections = configer.sections()                           # get all sections
                for section in sections:
                    iniDataArr = iniDataArr + configer.items(section)    # get all section value and save to Arr
        iniDataDic = dict(iniDataArr)                                # convert the section value to dictionary
        for keyWord in iniDataDic:
            iniDataDic[keyWord] = iniDataDic[keyWord].split(';')[0]  # delete the comments after ';'
            iniDataDic[keyWord] = iniDataDic[keyWord].split('#')[0]  # delete the comments after '#'
        return iniDataDic



    def __init__(self,manualImport=False, manualPath = ""):
        self.iniDataDic=self.reload_inifile_configuration(manualImport,manualPath)


if __name__ == "__main__":
    demoData = iniData()




# class iniData1():
#     init_flag = False    # To check if the inidata has been load before
#     iniDataDic = {}      # To save the inidata as dictionary
#
#     def get_inifile_path(self):
#         ConfigFilePath = '..\\..\\..\\testcases\Configs\\'
#
#         # Get current pc number
#         pcNum = socket.getfqdn(socket.gethostname())      #pcxxxxxxx.danfoss.net
#         pcNum = pcNum[0:9]
#
#         # Get inifile folder name for current pc
#         for filefolder in os.listdir(ConfigFilePath):
#             if pcNum in filefolder:
#                 return (ConfigFilePath+filefolder)
#
#
#     def reload_inifile_configuration(self):
#         iniDataArr = []   # To save the iniData as list
#         global iniDataDic
#
#         # create a ini file obj
#         configer = configparser.ConfigParser()
#
#         for file in os.listdir(self.get_inifile_path()):            # get all inifile in this folder
#             os.path.join(self.get_inifile_path(), file)
#             configer.read(self.get_inifile_path()+ '\\'+ file)       # load one inifile
#             sections = configer.sections()                           # get all sections
#             for section in sections:
#                 iniDataArr = iniDataArr + configer.items(section)    # get all section value and save to Arr
#         iniData.iniDataDic = dict(iniDataArr)                        # convert the section value to dictionary
#
#     def setx(self):
#         self.x = 5
#
#     def getx(self):
#         return self.x
#
#     def __init__(self):
#
#         self.x = 1
#         if iniData.init_flag:                                        # check if the inifile has been load before
#             return
#         self.reload_inifile_configuration()
#         iniData.init_flag = True



# p1=iniData()


# print (iniData.iniDataDic)
# print (iniData.iniDataDic.__len__())
# p2=iniData()
# print(p2.iniDataDic.__len__())

# print p2.iniDataDic



