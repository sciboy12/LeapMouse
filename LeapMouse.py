import configparser, os.path
import platform
import sys
import os
import Leap
from numpy import interp
from math import atan2, degrees

def do_nothing():
    pass

# Compensate for display scaling
system = platform.system()
print(system)

if system == 'Windows':
    import ctypes
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    set_pos = ctypes.windll.user32.SetCursorPos
    sync = do_nothing

if system == 'Linux':
    from Xlib import display
    display=display.Display()
    scr=display.screen().root
    res=scr.get_geometry()
    screen_width=res.width
    screen_height=res.height
    sync=display.sync
    set_pos = scr.warp_pointer

# Check for presence of config.ini
config = configparser.RawConfigParser()
if not os.path.isfile("config.ini"):
    config = configparser.ConfigParser()

    config.add_section('main')
    config.set('main', 'enable_scaler', 'True')
    config.set('main', 'screen_width_mm', '300')
    config.set('main', 'y_offset', '0')
    #config.set('main', 'disp_angle', '0')

    # Write to config.ini with above settings
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("Config file created")

config.read('config.ini')

# Whether or not to compensate for an angle diffrence between the sensor and display
enable_scaler = config.getboolean('main', 'enable_scaler')

# Area to map to the screen, measured in mm
# screen_height_mm is determined automatically based on display ratio
screen_width_mm = config.getint('main', 'screen_width_mm')

# How far the active area will be offset upwards
y_offset = config.getint('main', 'y_offset')
print("Config file loaded")

# Height calculation algorithm
screen_height_mm = (screen_height/screen_width)*screen_width_mm

# Print current config/determined values
print("Display resolution is",screen_width,"x",screen_height,"pixels.")
print("Active area width is",screen_width_mm,"mm")
print("Active area height is",int(screen_height_mm),"mm")
print("Y axis offset is",y_offset,"mm")
if enable_scaler:
    enable_scaler_print = "ON"
else:
    enable_scaler_print = "OFF"
print("Y axis scaler is",enable_scaler_print)

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        pointable = frame.pointables.frontmost

        # Check for visible fingers
        if pointable.is_valid:
            leapPoint = pointable.tip_position
            Point = leapPoint

            # Calculate offset angle
            if enable_scaler:
                angle = degrees(atan2(Point.z - 15, Point.y)) + 15
                y_scale = interp(angle,[-120,0],[0,1])
            else:
                y_scale = 1

            # Position the cursor
            set_pos(int(interp(Point.x,[0 - screen_width_mm * 0.5,screen_width_mm * 0.5],[0,screen_width])),\
                    int(interp(Point.y - y_offset,[0,screen_height_mm * y_scale],[screen_height,0])))
            sync() # This does nothing on Windows

            #if system == 'Windows':
            #    #mouse.position = (int(interp_x = interp(Point.x - 20,[0 - screen_mm_final * 0.5,screen_mm_final * 0.5],[0,screen_width_final])), int(interp(y_new,[y_min,y_max],[0,height])))
            #    mouse.position = (int(interp(Point.x,[0 - screen_width_mm * 0.5,screen_width_mm * 0.5],[0,screen_width])),\
            #                      int(interp(Point.y - y_offset,[0,screen_height_mm * y_scale],[screen_height,0])))

            #elif system == 'Linux':
            #    warp_pointer(int(interp(Point.x,[0 - screen_width_mm * 0.5,screen_width_mm * 0.5],[0,screen_width])),\
            #                 int(interp(Point.y - y_offset,[0,screen_height_mm * y_scale],[screen_height,0])))
            #    sync()

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
