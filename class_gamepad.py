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
            for event in pygame.event.get():
                if event.type == 10 and event.joy == self.id:  #JOYBUTTONDOWN
                    # print('button ', event.button)
                    # print('joy ', event.joy)
                    event_return = [True, event.type, event.button]
                    return event_return
                elif event.type == 11 and event.joy == self.id:  #JOYBUTTONUP
                    # print('button ', event.button)
                    # print('joy ', event.joy)
                    event_return = [True, event.type, event.button]
                    return event_return
                elif event.type == 7 and event.joy == self.id:  #JOYAXISMOTION
                    # print('axis ', event.axis)
                    # print('joy ', event.joy)
                    # print('joy ', event.value)
                    event_return = [True, event.type, event.axis, event.value]
                    return event_return
                else:
                    event_return = [False]
                    return event_return

j = Gamepad(1)
j.init()
pygame.init()

a = True
timer = pygame.time.Clock()
while a:
    timer.tick(100)
    if pygame.event.peek():
        a = j.get_event()
        if a[0]:
            print(a)


