import configparser

# help:
#   configparser: https://docs.python.org/3/library/configparser.html

class AppConfig(object):
    filename = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self,filename):
        self.filename = filename


def getConfig():
    configfn = 'config/config.ini'
    config = configparser.ConfigParser()
    config.read(configfn)
    
    if(config.has_section('test')): 

        filename = config['test']['filename'];
        c = AppConfig(filename)
        return c
    else:
        print('Invalid config: {0} \n',format(configfn))
        return False