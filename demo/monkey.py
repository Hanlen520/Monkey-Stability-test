import os
import os.path
import time
import glob

# delete script
path = "E:\\monkey_test\\"
for file in glob.glob(os.path.join(path, '*.cmd')):
    os.remove(file)

os.system("cls")  # os.system("cls") clear screen
rt = os.popen('adb devices').readlines()  # os.popen()get return
n = len(rt) - 2
print("connect：" + str(n))
aw = input("monkey yes or no: ")

if aw == 'yes':
    print
    "monkey ready...."
    count = input("input monkey test count: ")
    testmodel = input("1 2: ")
    ds = range(n)
    for i in range(n):
        nPos = rt[i + 1].index("\t")
        ds[i] = rt[i + 1][:nPos]
        dev = ds[i]
        promodel = os.popen(
            "adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.model="').readlines()  # phone type
        # modelname = ('').join(promodel)  #
        modelname = promodel[0]  #
        model = modelname[17:].strip('\r\n')
        proname = os.popen(
            "adb -s " + dev + ' shell cat /system/build.prop | find "ro.product.brand="').readlines()
        roname = proname[0]
        name = roname[17:].strip('\r\n')
        packagename = os.popen(
            "adb -s " + dev + ' shell pm list packages | find "xxx"').readlines()
        package = packagename[0]
        pk = package[8:].strip('\r\n')
        if pk == 'com.xxx':
            filedir = os.path.exists("E:\\monkey_test\\")
            if filedir:
                print
                "File Exist!"
            else:
                os.mkdir("E:\\monkey_test\\")
            devicedir = os.path.exists("E:\\monkey_test\\" + name + '-' + model + '-' + dev)
            if devicedir:
                print
                "File Exist!"
            else:
                os.mkdir("E:\\monkey_test\\" + name + '-' + model + '-' + dev)
            wl = open("E:\\monkey_test\\" + name + '-' + model + '-' + ds[i] + '-logcat' + '.cmd', 'w')
            # wl.write('adb -s ' + dev + ' logcat -v time ACRA:E ANRManager:E System.err:W *:S')
            wl.write('adb -s ' + dev + ' logcat -v time *:W')
            wl.write('> E:\\monkey_test\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\logcat_%random%.txt\n')
            wl.close()
            wd = open("E:\\monkey_test\\" + name + '-' + model + '-' + ds[i] + '-device' + '.cmd', 'w')
            wd.write(
                'adb -s ' + dev + ' shell monkey -p com.carsland.asd --monitor-native-crashes --ignore-crashes --pct-syskeys 5 --pct-touch 55 --pct-appswitch 20 --pct-anyevent 20 --throttle 200 -s %random% -v ' + count)  # 选择设备执行monkey
            wd.write('> E:\\monkey_test\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\monkey_%random%.txt\n')
            wd.write('@echo ok~')
            wd.close()
        wd = open("E:\\monkey_test\\" + name + '-' + model + '-' + ds[i] + '-device' + '.cmd', 'w')
        wd.write(':loop')
        wd.write('\nset /a num+=1')
        wd.write('\nif "%num%"=="4" goto end')
        wd.write(
            '\nadb -s ' + dev + ' shell monkey -p com.carsland.asd --monitor-native-crashes --ignore-crashes --pct-syskeys 5 --pct-touch 55 --pct-appswitch 20 --pct-anyevent 20 --throttle 200 -s %random% -v ' + count)  # 选择设备执行monkey
        wd.write('> E:\\monkey_test\\' + '"' + name + '-' + model + '-' + dev + '"' + '\\monkey_%random%.txt\n')
        wd.write('@echo ok~')
        wd.write('\nadb -s ' + dev + ' shell am force-stop ' + pk)
        wd.write('\n@ping -n 15 127.1 >nul')
        wd.write('\ngoto loop')
        wd.write('\n:end')
        wd.close()
    else:
        print("confirm" + name + '-' + model + "not install com.xxx~")

# cmd path='E:\\monkey_test\\'
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)) == True:
        if file.find('.cmd') > 0:
            os.system('start ' + os.path.join(path, '"' + file + '"'))
            time.sleep(1)
        elif aw == 'no':
            print('please cofirm adb')
    else:
        print(" illegal yes or no！")