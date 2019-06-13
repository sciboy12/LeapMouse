from __future__ import division
import math, ConfigParser, ctypes, os.path
import platform
import math
import sys
import os
sys.path.append(os.getcwd())
import Leap
dir_path = os.path.dirname(os.path.realpath(__file__))
#from . file import Leap
from numpy import interp
from pynput import mouse
from pynput.mouse import Button, Controller

errorcode = 0

# Compensate for display scaling
system = platform.system()
if system == 'Windows':
    print('Windows')
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

elif system == 'Linux':
    print('Linux')
    from Xlib import display
    display=display.Display()
    scr=display.screen().root
    res=scr.get_geometry()
    warp_pointer=scr.warp_pointer
    screen_width=res.width
    screen_height=res.height
    sync=display.sync
# Get screen resolution

config = ConfigParser.RawConfigParser()

# Check for presence of config.ini
if not os.path.isfile("config.ini"):
    config = ConfigParser.SafeConfigParser()
    config.add_section('mode')
    config.set('mode', 'modeSetting', '0')
    
    config.add_section('mode_0')
    config.set('mode_0', 'screen_width', '270')
    config.set('mode_0', 'offset', '5')
    
    config.add_section('mode_1')
    config.set('mode_1', 'screen_width', '264')
    config.set('mode_1', 'offset', '10')
    # Create config.ini with above settings
    with open('config.ini', 'wb') as configfile:
        config.write(configfile)
    print "Config file created"

config.read('config.ini')
print "Config file loaded"
# ---Config---
# Area to map to the screen, measured in mm
# Height(NOT display height) is determined automatically based on display ratio
# lower number = smaller active area = higher sensitivity
mode = config.getint('mode', 'modeSetting')
screen_mm_0 = config.getint('mode_0', 'screen_width')
screen_mm_1 = config.getint('mode_1', 'screen_width')
offset_0 = config.getint('mode_0', 'offset')
offset_1 = config.getint('mode_1', 'offset')
screen_mm_2 = 215

# How many mm to offset the active area above the Leap
offset_mini = 5
offset_full = 10
offset_5inch = 8

# Notes
'''
TODO:
Fix error handling regarding mode 1
Further improve error handlng regarding corrupt config files
Update Readme.txt

https://docs.python.org/2.7/library/configparser.html#examples
0 is mini, 1 is full
'''
'''
# Ensure mode is valid
if not mode == 0 or mode == 1:
    errorcode = 1
else:
    errorcode = 0
    
# Print error if it isn't valid
if errorcode == 1:
    print "===ERROR==="
    print
    print "Error code:",errorcode
    print "See Readme.txt for more info."
    print
    input("Press Enter to exit...")
    controller.remove_listener(listener)
    exit()
'''
# Height calculation algorithm(Duplicated once for each mode)


def plat_windows():
    # X axis mapping
    interp_x = interp(Point.x - 20,[0 - screen_mm_final * 0.5,screen_mm_final * 0.5],[0,screen_width_final])
    # Y axis mapping
    interp_y = screen_height_final - interp(Point.y - offset_final,[0,sensitivity_y],[0,screen_height_final])
    # Position the cursor
    
if mode == 0:
    sensitivity_y = (screen_height/screen_width)*screen_mm_0
    screen_mm_final = screen_mm_0
    screen_width_final = screen_width
    screen_height_final = screen_height
    offset_final = offset_0
    print "Display resolution is",screen_width,"x",screen_height,"pixels."
    print "Active area width is",screen_mm_0,"mm"
    print "Y offset is",offset_0,"mm"
    
elif mode == 1:
    sensitivity_y = (screen_height/screen_width)*screen_mm_1
    screen_mm_final = screen_mm_1
    screen_width_final = screen_width
    screen_height_final = screen_height
    offset_final = offset_1
    print "Display resolution is",screen_width,"x",screen_height,"pixels."
    print "Active area width is",screen_mm_1,"mm"
    print "Y offset is",offset_1,"mm"
    
    '''
    elif mode == "5inch":
    sensitivity_y = (screen_height_5inch/screen_width_5inch)*screen_mm_5inch
    screen_mm_final = screen_mm_5inch
    screen_width_final = screen_width_5inch
    screen_height_final = screen_height_5inch
    offset_final = offset_5inch
    print "Current Display resolution is",screen_width_5inch,"x",screen_height_5inch,"pixels."
    print "Current sensitivity is",screen_mm_5inch,"mm"
    print "Current Y offset is",offset_5inch,"mm"
    print ""
    '''

else:
    print "Invalid mapping - Please ensure line 11 in LeapMouse.py is set to one of the following strings."
    print "---------------------------------------------------------------------------"
    print "\"full\" - maps the Leap to match your screen size."
    print "\"mini\" - maps the Leap to a width twice to the width of the sensor(2*80mm)."
    print "Press any key to continue."
    #controller.remove_listener(listener)
    #keyboard.sleep()
    exit()

class SampleListener(Leap.Listener):
    
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        
    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        #mouse = Controller()        
        pointable = frame.pointables.frontmost
        # Check for visible fingers
        if pointable.is_valid:
            #iBox = frame.interaction_box
            leapPoint = pointable.tip_position
            #normalizedPoint = iBox.normalize_point(leapPoint, False)
            Point = leapPoint
            

            # Main code
            # X axis mapping
            #interp_x = interp(Point.x - 20,[0 - screen_mm_final * 0.5,screen_mm_final * 0.5],[0,screen_width_final])
            # Y axis mapping
            #interp_y = screen_height_final - interp(Point.y - offset_final,[0,sensitivity_y],[0,screen_height_final])
            # Position the cursor
            #mouse.position = (interp_x,interp_y)
            if system == 'Windows':
                mouse.position = (int(interp_x = interp(Point.x - 20,[0 - screen_mm_final * 0.5,screen_mm_final * 0.5],[0,screen_width_final])), int(interp(y_new,[y_min,y_max],[0,height])))

            elif system == 'Linux':
                warp_pointer(int(interp(Point.x,[0 - screen_mm_final * 0.5,screen_mm_final * 0.5],[0,screen_width_final])),\
                             int(interp(Point.y - offset_final,[0,sensitivity_y],[screen_height_final,0])))
                sync()
            '''
            if (Point.z < 0):
                
                mouse.press(Button.left)
            else:
                mouse.release(Button.left)
            '''
            
    '''
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
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
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)



if __name__ == "__main__":
    main()
