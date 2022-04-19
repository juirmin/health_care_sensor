import yaml
from yaml.loader import SafeLoader

def modeset():
    with open('/media/pi/HEALTH/set.yml') as f:
        data = yaml.load(f, Loader=SafeLoader)
    return(data.get('mode'))

if __name__ == '__main__':
    print(modeset())
