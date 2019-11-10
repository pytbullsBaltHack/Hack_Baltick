import configparser

# help:
#   configparser: https://docs.python.org/3/library/configparser.html

class AppConfig(object):
    filename = ""
    cache = 0
    
    facedet = {}

    # The class "constructor" - It's actually an initializer 
    def __init__(self):
        self.filename = ""
        self.cache = 0
        self.facedet = {}


def getConfig():
    configfn = 'config/config.ini'
    config = configparser.ConfigParser()
    config.read(configfn)
   
    c = AppConfig()
    
    if(config.has_section('facedet')): 
        c.facedet = {}
        c.facedet['cfg'] = config['facedet']['cfg']
        c.facedet['weights'] = config['facedet']['weights']
        c.facedet['img_size'] = int(config['facedet']['img_size'])
        c.facedet['conf_thres'] = float(config['facedet']['conf_thres'])
        c.facedet['nms_thres'] = float(config['facedet']['nms_thres'])
        c.facedet['device'] = config['facedet']['device']
        c.facedet['classes_names'] = config['facedet']['classes_names']

    else:
        print('Invalid config: {0} \n',format(configfn))
        return False
    
    if(config.has_section('test')): 
        c.filename = config['test']['filename'];
        c.cache = int(config['test']['cache']);
        
    else:
        print('Invalid config: {0} \n',format(configfn))
        return False
        
    return c
     