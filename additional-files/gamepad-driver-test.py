#Test file for using gamepad driver in games
import time
import keyboard
import pydirectinput as pdi
import vgamepad as vg

gamepad = vg.VDS4Gamepad() #use vg.VX360Gamepad() if games can not recognize dualshock

time.sleep(5) # Have enough time to switch to the game
count = 0
test_mode = True # Turn the wheel full left-right-left  /  Set it false to drive with "wasd"

while True:
    mjoy = 0
    
    if test_mode:
        if count % 2 == 0:
            mjoy = -1
        else:
            mjoy = 1
        time.sleep(1)
        count += 1

    if keyboard.is_pressed("a"):
        mjoy = -1
    elif keyboard.is_pressed("d"):
        mjoy = 1

    if keyboard.is_pressed("w"):
        gamepad.right_trigger_float(1)
        gamepad.left_trigger_float(0)
    elif keyboard.is_pressed("s"):
        gamepad.left_trigger_float(1)
        gamepad.right_trigger_float(0)
    else:
        gamepad.left_trigger_float(0)
        gamepad.right_trigger_float(0)

    gamepad.left_joystick_float(mjoy, 0)
    gamepad.update()

    if keyboard.is_pressed("esc"):
        break
