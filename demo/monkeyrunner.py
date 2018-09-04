#coding = utf-8
import os,time,sys
import logging

def monkey():
    '''monkeyrunner and log output'''
    #get devices number
    rt = os.popen("adb devices").readlines()
    n = len(rt) - 2
    print("Current connect device counts is:"+str(n))
    #dir no need ':'and ' '
    now = time.strftime("%Y-%m-%d")
    #creat log name
    newnow = time.strftime("%Y-%m-%d%H%M%S")
    #get current dir
    nowpath = os.getcwd()
    #create log dir
    path = nowpath+'/'+now
    #create log file
    newpath =path+'/'+newnow+'log.txt'
    #get the first connect device
    devicename = rt[1][:16]
    # print(devicename)
    if not os.path.exists(path):
        os.mkdir(path)
    elif n<1:
        #make sure the device is not null
        print("Pls check the device connect!")
    elif n==1:
        event = int(input("Please enter the event of times you need to perform:"))
        #-v level0 /-v -v leve1 /-v -v -v level2
        #full screen dynamic hidden status bar and virtual buttons
        os.system('adb -s %s shell settings put global policy_control immersive.full=*' %devicename)
        #monkeytest
        os.system('adb -s %s shell monkey -p com.carsland.asd --pct-motion 25 --pct-touch 40 --pct-nav 10 --pct-appswitch 10 --ignore-crashes --ignore-timeouts --throttle 300 -s 8888 -v -v -v %d >%s' %(devicename,event,newpath))
        # os.system('adb logcat>'+newpath)
        # exist full screen dynamic hidden status bar and virtual buttons
        os.system('adb -s %s shell settings put global policy_control null'%devicename)
        # force exist app
        os.system('adb -s %s shell am force-stop com.carsland.asd' %devicename)
    else:
        # print("Current connect device more than 1")
        event = int(input("Please enter the event of times you need to perform:"))
        print(rt,rt[1][:16])
        for i in range(n):
            #get devicename
            dev = rt[i + 1][:16]
            print('Current run monkeytest device seria is:'+dev)
            #full screen dynamic hidden status bar and virtual buttons
            os.system('adb -s %s shell settings put global policy_control immersive.full=*' %dev)
            #monkeytest
            os.system(
                'adb -s %s shell monkey -p com.carsland.asd --pct-motion 25 --pct-touch 40 --pct-nav 10 --pct-appswitch 10 --ignore-crashes --ignore-timeouts --throttle 300 -s 8888 -v -v -v %d >%s' % (
                dev,event, newpath))
            #exist full screen dynamic hidden status bar and virtual buttons
            os.system('adb -s %s shell settings put global policy_control null' % dev)
            #force exist app
            os.system('adb -s %s shell am force-stop com.carsland.asd' %dev)

counts=int(input("Please enter the number of times you need to perform:"))
#run monkeytest
for y in range(counts):
    print("Running for %d times"%(y+1))
    monkey()
