from homematicip.home import Home
from homematicip.base.enums import EventType

class HomematicipHandler:

    def __init__(self, config) -> None:
        """Initialize HomematicIP Cloud connection."""
        self._config = config
        self._home = Home()

    def connect(self) -> None:
        self._home = Home()
        self._home.set_auth_token(self._config.auth_token)
        self._home.init(self._config.access_point)

        self._home.get_current_state()
        self._home.onEvent += self.homematicip_eventHandler
        self._home.enable_events()

    def disconnect(self) -> None:
        self._home.disable_events()


    def homematicip_eventHandler(self, eventList):
        """ This function handles all changes. Here you can filter for devices and store the changes """
        print("homematicip_eventHandler called")
        for event in eventList:
            # Process events
            type = event['eventType']
            obj = event['data']

            if type == EventType.GROUP_CHANGED:
                print("Group {0} changed".format(obj.id))
            elif type == EventType.DEVICE_CHANGED:
                print("Device {0} changed".format(obj.id))
            else:
                print("Process eventType {0}".format(type))