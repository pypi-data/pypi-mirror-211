from pynput.keyboard import Key, Controller
from time import sleep

keyboard = Controller()

def press_and_release(key):
    """
    Presses a given key and releases it if it is currently pressed.
    
    :param key: A string representing the key to be pressed and released.
    
    :return: None.
    """
    keyboard.press(key)
    if (keyboard.pressed(key)):
        keyboard.release(key)

        
def run_command(command):
    """
    Runs a given command.
    
    :param command: A string representing the command to be run.
    
    :return: None.
    """
    keyboard.type(command)
    press_and_release(Key.enter)


def main():
    """
    Executes a terminal command to print 'Hello World' by simulating the Windows key + R keyboard shortcut to open the Run dialog. Then, it runs the command prompt (cmd) and executes the 'echo Hello World' command.

    Args:
        None.

    Returns:
        None.
    """
    press_and_release(Key.cmd_r)

    run_command('cmd')
    run_command('echo Hello World')
    
    
if __name__ == '__main__':
    main()