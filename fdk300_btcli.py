import subprocess


class FDK300:
    def __init__(self):
        self.cmd = '''
        { printf 'scan on\n\n'
          printf 'connect C6:05:04:07:4D:54\n\n'
          printf 'menu gatt\n\n'
          printf 'select-attribute /org/bluez/hci0/dev_C6_05_04_07_4D_54/service0020/char0023\n\n'
          printf 'read\n\n'
          printf '\n\n'
          sleep 3
         
        } | bluetoothctl
        
        '''
    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        result={'temperature' : 0}
        for i in range(50):
            res = proc.stdout.readline()
            data = res.decode('ascii').strip()
            if data.find('fe 6a 72 5a') != -1:
                data = data.split(" ")[26:34]
                _temp = ''.join(data[4:6])
                temperateure = int(_temp,16)/100
                if temperateure < 50:
                    result['temperature']=temperateure
                    return result

        return result


if __name__ == '__main__':
    fdk300 = FDK300()
    while 1:
        data = fdk300.get_sensor_data()
        print(data)

