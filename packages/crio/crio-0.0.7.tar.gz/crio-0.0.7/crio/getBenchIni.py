import os,json
from Loadini import iniData
from crio import *
def benchname():
    ConfigFilePath = 'N:/AutomatedLabTest/LabTest-P600/ConfigFiles'
    benchname = {}       
    for filefolder in os.listdir(ConfigFilePath):
        benchname[filefolder]=filefolder[9:].replace(' ','').replace('(','').replace(')','')
    a = os.path.abspath(os.curdir)
    with open(a+'/config.json','w') as file_obj:
        json.dumps(benchname,file_obj,indent=1)
    print('Process done. File update in' + a)
def accquireCFG(benchname,storepath):
    if(benchname == 'Manual'):
        print('Manual bench, currently config file is not needed.') 
        return   
    ConfigFilePath = 'N:/AutomatedLabTest/LabTest-P600/ConfigFiles'
    ConfigFilePath += '/'+benchname
    a = iniData(True,ConfigFilePath)
    f = os.path.abspath(os.curdir)
    with open(storepath +'/iniconfig.cfg','w') as file_obj:
        json.dump(a.iniDataDic,file_obj,indent=1)
    print('Process done. File update in ' + 'iniconfig.cfg')
    pass

if __name__=="__main__":
    accquireCFG("pc0232141 (CNHY11)","./config")