import yaml
from yaml.loader import SafeLoader

def modeset(filepath):
    with open(filepath) as f:
        data = yaml.load(f, Loader=SafeLoader)
    return(data.get('mode'))

if __name__ == '__main__':
    print(modeset())
