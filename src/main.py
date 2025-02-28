# Assisted by watsonx Code Assistant 
import sys
import logging.handlers

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter("[{asctime:s}] [{name:25s}] {levelname:8s} | {message:s}", style='{'))
logging.getLogger().addHandler(ch)
logging.getLogger().setLevel(logging.DEBUG)

from Lighting import Lighting

lighting = None

def setAndCheckConfig():
    argc = len(sys.argv)
    
    if argc < 2:
        print("Usage: python main.py [-c <configuration file>]")
        sys.exit(1)

    for i in range (1, argc):

        parameter = sys.argv[i]

        if (parameter == "-c") | (parameter == "--configfile"):
            # do something
            fileName = sys.argv[i+1]
            print (fileName)
            global lighting
            lighting = Lighting(fileName)
            pass

    if (lighting is None):
        logging.debug(f"Not all parameters set from command line: {sys.argv}")
        print("Invalid parameter")
        sys.exit(1)

def main():

    setAndCheckConfig()

    if lighting is not None:
        lighting.action()

if __name__ == "__main__":
    main()
