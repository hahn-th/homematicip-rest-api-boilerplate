#!/usr/bin/env python3
import asyncio
import datetime
import json
import homematicip
from homematicip.base.base_connection import HmipConnectionError
from homematicip.base.enums import EventType
from homematicip.aio.home import AsyncHome

# read the config file which is created by the hmip_generate_auth_token.py script
config = homematicip.find_and_load_config_file()

def on_update_handler(data, event_type, obj):
    print("{0:15} - {1}".format(event_type, str(obj)))
    # React on different event types
    # if event_type == EventType.CLIENT_CHANGED:
    #     pass
    # elif event_type == EventType.GROUP_CHANGED:
    #     pass

async def get_home(loop):
    home = AsyncHome(loop)
    home.set_auth_token(config.auth_token)
    await home.init(config.access_point)
    return home


async def wait_for_ws_incoming(home):
    """ register update handlers on devices and groups"""
    print("read current states")
    await home.get_current_state()
    for d in home.devices:
        d.on_update(on_update_handler)
    for d in home.groups:
        d.on_update(on_update_handler)

    home.on_update(on_update_handler)

    print("wait for new events")
    reader = await home.enable_events()
    await reader


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    home = None
    try:
        home = loop.run_until_complete(get_home(loop))
        loop.run_until_complete(wait_for_ws_incoming(home))
    except HmipConnectionError:
        print("Problem connecting")
    finally:
        # close websocket connection
        print("close websocket connection")
        loop.run_until_complete(home.disable_events())
