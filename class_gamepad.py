import pygame

class Gamepad:

    def __init__(self, gamepad_id):

        self.exist = False
        self.axe_count = 0
        self.button_count = 0
        self.id = gamepad_id

        if not pygame.joystick.get_init():
            pygame.joystick.init()

        gamepad_count = pygame.joystick.get_count()

        if gamepad_count < 1: # gamepad not connected
            print('gamepad not connected')
        elif type(gamepad_id) != int: # id is not 'int' class
            print('id must be int')
        elif gamepad_id < 0 or gamepad_count <= gamepad_id: # id out of range
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
        if self.exist:
            self.Gamepad.init()
        else:
            print('this gamepad not exists')

    def quit(self):
        if self.exist:
            self.Gamepad.quit()
        else:
            print('this gamepad not exists')

    def get_button_count(self):
        return self.button_count

    def get_axe_count(self):
        return self.axe_count

    def get_event(self):
            id = self.id
            joy_event_list = JoystickEvents.get_joy_event_list(id) #FIXME:TypeError: get_joy_event_list() missing 1 required positional argument: 'joy'
            for event in joy_event_list:
                if event[1] == 10:  #JOYBUTTONDOWN
                    event_return = [True, event[1], event[2]]
                    return event_return
                elif event[1] == 11:  #JOYBUTTONUP
                    event_return = [True, event[1], event[2]]
                    return event_return
                elif event[1] == 7:  #JOYAXISMOTION
                    event_return = [True, event[1], event[2], event[3]]
                    return event_return
                else:
                    event_return = [False]
                    return event_return

class JoystickEvents:

    def __init__(self,):
        self.event_list = []

    def append_events_to_event_list(self):
        """Check joystick events and put to self.event_list

        also clean current API event list

        """

        for event in pygame.event.get():
            if event.type == 10:  #JOYBUTTONDOWN
                append_element = [event.joy, event.type, event.button]
                self.event_list.append(append_element)
            elif event.type == 11:  # JOYBUTTONUP
                append_element = [event.joy, event.type, event.button]
                self.event_list.append(append_element)
            elif event.type == 7:  # JOYAXISMOTION
                append_element = [event.joy, event.type, event.axis, event.value]
                self.event_list.append(append_element)

    def get_joy_event_list(self, joy):
        """Move all events for custom joystick to list in return

        """

        joy_event_list = []
        self.append_events_to_event_list()

        for index in range(len(self.event_list)):
            if self.event_list[index][0] == joy:  #if event of joystick(id)
                joy_event_list.append(self.event_list.pop(index))
        return joy_event_list


pygame.init()
#ev = JoystickEvents
j = Gamepad(1)
j.init()


a = True
timer = pygame.time.Clock()
while a:
    timer.tick(100)

    if pygame.event.peek():
        a = j.get_event()
        if a[0]:
            print(a)


