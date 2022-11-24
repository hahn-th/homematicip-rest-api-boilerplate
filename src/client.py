#!/usr/bin/env python3
import homematicip
from HomematicipHandler import HomematicipHandler

# read the config file which is created by the hmip_generate_auth_token.py script
config = homematicip.find_and_load_config_file()
    
def main():
    if config is None:
        print("COULD NOT DETECT CONFIG FILE")
        return

    print("Initialize handler")
    hmHandler = HomematicipHandler(config)
    print("Connect to HomematicIP Cloud")
    hmHandler.connect()

    input('Press enter to continue: ')
    hmHandler.disconnect()

if __name__ == "__main__":
    main()