import subprocess


class MTKA1:
    def __init__(self):
        self.find_data = False
        self.cmd = '''
        { printf 'scan on\n\n'
          printf '\n\n'
          sleep 30
          printf 'quit'
         
        } | bluetoothctl
        
        '''

    def get_sensor_data(self):
        proc = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        convert = 0
        for i in range(50):
            res = proc.stdout.readline()
            data = res.decode('ascii').strip()
            data_index = data.find(
                'Device 6D:97:40:33:34:D0 ManufacturerData Value:')
                        
            if self.find_data == True:
                raw_data = data.split(' ')
                raw_weight = ''.join(raw_data[-10:-8])
                weight = int(raw_weight, 16)/10
                self.find_data = False
                return {'weight':weight}
            
            if data_index != -1:
                self.find_data = True
        return {'weight': 0}


if __name__ == '__main__':
    scale = MTKA1()
    while 1:
        data = scale.get_sensor_data()
        print(data)
