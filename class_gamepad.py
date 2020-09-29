import pygame


class Gamepad:
    """Class to create object for single Joystick

    Automatically initializes during initialisation. User can initialize or un-initialize it via subs 'init' and 'quit'
    Multiple instances of Gamepad must work with single instance of JoystickEvents class.
    Usage:
    1. Create 1 JoystickEvents object and as many Gamepad objects as you need
        je = JoystickEvents()
        j1 = Gamepad(0)
        j2 = Gamepad(1)
    2. Add to mainloop:
         if j1.is_new_events(je):
            event = j1.get_event(je)

    """

    def __init__(self, gamepad_id):
        """ Connect Gamepad to physical device if available

        Initialize Joystick module
        and check if device(id) is present
        :param gamepad_id: system id of joystick

        """

        self.exist = False
        self.axe_count = 0
        self.button_count = 0
        self.id = gamepad_id
        self.is_events = False

        if not pygame.joystick.get_init():
            pygame.joystick.init()

        gamepad_count = pygame.joystick.get_count()

        if gamepad_count < 1:  # gamepad not connected
            print('gamepad not connected')
        elif type(gamepad_id) != int:  # id is not 'int' class
            print('id must be int')
        elif gamepad_id < 0 or gamepad_count <= gamepad_id:  # id out of range
            print('wrong id', gamepad_id)
        else:
            print('gamepad', gamepad_id, 'found')
            self.exist = True

        if self.exist:
            self.Gamepad = pygame.joystick.Joystick(gamepad_id)
            self.init()
            self.button_count = self.Gamepad.get_numbuttons()
            self.axe_count = self.Gamepad.get_numaxes()

    def init(self):
        """Initialize current instance if present"""

        if self.exist:
            self.Gamepad.init()
        else:
            print('this gamepad not exists')

    def quit(self):
        """Un-initialize current instance if present"""

        if self.exist:
            self.Gamepad.quit()
        else:
            print('this gamepad not exists')

    def get_button_count(self):
        """Returns number of buttons of current device

        :return integer

        """

        return self.button_count

    def get_axe_count(self):
        """Returns number of axes of current device

        :return integer

        """
        return self.axe_count

    def get_event(self, joystick_events_instance):
        """Return event for current device, and delete it from event_list

        Event is a dict:
            for button [type, button number]
                type:  10 - button down
                       11 - button up
            for axe [type, axis, value]
                type:  7 - axis move
                value: float from -1 to 1 (0 - center)

        :returns list

        """

        if len(joystick_events_instance.event_list[self.id]) > 0:
            return joystick_events_instance.event_list[self.id].pop()

    def is_new_events(self, joystick_events_instance):
        """Update events

         and put to event list if present

        :returns True if new events found, else returns False

        """

        joystick_events_instance.append_events_to_event_list()

        if len(joystick_events_instance.event_list[self.id]) > 0:
            return True
        else:
            return False


class JoystickEvents:
    """Class for joystick events

    You should use only one instance of this class

    """

    def __init__(self):
        pygame.init()
        self.event_list = [[], []]

    def append_events_to_event_list(self):
        """Check joystick events and put to self.event_list

        Also clean current API event list.
        Ignoring and delete all other events (mouse, keyboard, midi)

        """

        if pygame.event.peek():
            for event in pygame.event.get():
                if event.type == 10:  # JOYBUTTONDOWN
                    append_element = {'type': event.type, 'button': event.button}
                    self.event_list[event.joy].append(append_element)
                elif event.type == 11:  # JOYBUTTONUP
                    append_element = {'type': event.type, 'button': event.button}
                    self.event_list[event.joy].append(append_element)
                elif event.type == 7:  # JOYAXISMOTION
                    append_element = {'type': event.type, 'axis': event.axis, 'value': event.value}
                    self.event_list[event.joy].append(append_element)

    def get_joy_event_list(self, joy):
        """Move all events for custom joystick to list in return

        :returns list

        """

        joy_event_list = []
        index = 0
        for event in self.event_list[joy]:
            joy_event_list.append(event)
            self.event_list[joy].pop(index)
            index += 1
        return joy_event_list


if __name__ == '__main__':

    ev = JoystickEvents()
    j0 = Gamepad(0)
    j1 = Gamepad(1)

    a = True
    timer = pygame.time.Clock()

    while a:
        timer.tick(100)

        if j0.is_new_events(ev):
            a = j0.get_event(ev)  # a - dictionary

            if a['type'] == 10:
                print('Gamepad 0: ', a['type'], a['button'])
            if a['type'] == 11:
                print('Gamepad 0: ', a['type'], a['button'])
            if a['type'] == 7:
                print('Gamepad 0: ', a['type'], a['axis'], a['value'])

        if j1.is_new_events(ev):
            print('Gamepad 1: ', j1.get_event(ev))
