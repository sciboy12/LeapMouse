import configparser, os.path
import platform
import sys
import os
#sys.path.append(os.getcwd())
import Leap
dir_path = os.path.dirname(os.path.realpath(__file__))
#from . file import Leap
from numpy import interp
#from pynput import mouse
#from pynput.mouse import Button, Controller

# Compensate for display scaling
system = platform.system()
print(system)
if system == 'Windows':
    import ctypes
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

elif system == 'Linux':
    from Xlib import display
    display=display.Display()
    scr=display.screen().root
    res=scr.get_geometry()
    warp_pointer=scr.warp_pointer
    screen_width=res.width
    screen_height=res.height
    sync=display.sync

# Check for presence of config.ini
config = configparser.RawConfigParser()
if not os.path.isfile("config.ini"):
    config = configparser.ConfigParser()

    config.add_section('main')
    config.set('main', 'screen_width_mm', '300')
    config.set('main', 'y_offset', '0')
    config.set('main', 'disp_angle', '0')

    # Write to config.ini with above settings
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Config file created")

config.read('config.ini')
# ---Config---
# Area to map to the screen, measured in mm
# Height(NOT display height) is determined automatically based on display ratio
# lower number == smaller active area == higher sensitivity
screen_width_mm = config.getint('main', 'screen_width_mm')
y_offset = config.getint('main', 'y_offset')
disp_angle = config.getint('main', 'disp_angle')
print("Config file loaded")
y_scale = interp(disp_angle,[0,90],[1,0])

# Height calculation algorithm
y_sensitivity = (screen_height/screen_width)*screen_width_mm
print("Display resolution is",screen_width,"x",screen_height,"pixels.")
print("Active area width is",screen_width_mm,"mm")
print("Y offset is",y_offset,"mm")
print("Y scale is",y_scale,"(" + str(disp_angle) + "° offset)")

class SampleListener(Leap.Listener):

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        #mouse = Controller()
        pointable = frame.pointables.frontmost
        # Check for visible fingers
        if pointable.is_valid:
            leapPoint = pointable.tip_position
            Point = leapPoint
            # Position the cursor
            if system == 'Windows':
                #mouse.position = (int(interp_x = interp(Point.x - 20,[0 - screen_mm_final * 0.5,screen_mm_final * 0.5],[0,screen_width_final])), int(interp(y_new,[y_min,y_max],[0,height])))
                mouse.position = (int(interp(Point.x,[0 - screen_width_mm * 0.5,screen_width_mm * 0.5],[0,screen_width])),\
                                  int(interp(Point.y - y_offset,[0,y_sensitivity * y_scale],[screen_height,0])))

            elif system == 'Linux':
                warp_pointer(int(interp(Point.x,[0 - screen_width_mm * 0.5,screen_width_mm * 0.5],[0,screen_width])),\
                             int(interp(Point.y - y_offset,[0,y_sensitivity * y_scale],[screen_height,0])))
                sync()
            '''
            if (Point.z < 0):

                mouse.press(Button.left)
            else:
                mouse.release(Button.left)
            '''

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Allow processing frames without window focus
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
