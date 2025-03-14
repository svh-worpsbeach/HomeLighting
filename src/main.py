# Assisted by watsonx Code Assistant 
import sys
import logging.handlers
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter("[{asctime:s}] [{name:25s}] {levelname:8s} | {message:s}", style='{'))
logging.getLogger().addHandler(ch)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from Lighting import Lighting
from Show import Show

lighting = None
show = None

def set_and_check_config():
    global lighting
    global show

    lightingFileName = None
    showFileName = None

    argc = len(sys.argv)
    
    if argc < 2:
        print("Usage: python main.py [-c <configuration file>]")
        sys.exit(1)

    for i in range (1, argc):

        parameter = sys.argv[i]

        if (parameter == "-c") | (parameter == "--configfile"):
            # do something
            lightingFileName = sys.argv[i+1]
            logger.debug (f"Configfile {lightingFileName}")
            pass

        if (parameter == "-s") | (parameter == "--showfile"):
            # do something
            showFileName = sys.argv[i+1]
            logger.debug (f"Showfile {showFileName}")
            pass

    if (lightingFileName is None):
        logger.debug(f"Not all parameters set from command line: {sys.argv}")
        print("Invalid parameter")
        sys.exit(1)
    else:  
        if showFileName is None:
            logger.debug(f"Starting without show configuration")
            show = Show(None)
        else:
            show = Show(showFileName)

        lighting = Lighting(lightingFileName, show)



def main():

    set_and_check_config()
    
    if lighting is not None:
        if show is not None:
            lighting.action()

if __name__ == "__main__":
    main()
