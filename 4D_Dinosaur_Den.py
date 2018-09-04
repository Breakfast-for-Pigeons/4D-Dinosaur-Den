#!/usr/bin/python3
'''
4D Dinosaur Den

Description:
This program controls the motors of 3 toy dinosaurs and 1 flying
reptile. A button is pressed to make them move.

This program is also an example of adding color to text displayed to the
screen.

Author: Paul Ryan

This program was written on a Raspberry Pi using the Geany IDE.
'''
########################################################################
#                         Import Modules                               #
########################################################################

import os
import logging
import random
from time import sleep
from gpiozero import Motor, Button, OutputDevice
import pygame

########################################################################
#                          Variables                                   #
########################################################################

#  T. rex variables
t_rex_motor = Motor(20, 16, True)               # forward, backward, pwm
t_rex_motor_enable = OutputDevice(21)
white_button = Button(12)

# Triceratops variables
triceratops_motor = Motor(19, 13, True)         # forward, backward, pwm
triceratops_motor_enable = OutputDevice(6)
green_button = Button(26)

# Brachiosaurus variables
brachiosaurus_motor = Motor(23, 18, True)       # forward, backward, pwm
brachiosaurus_motor_enable = OutputDevice(24)
blue_button = Button(25)

# Pteranodon variables
pteranodon_motor = Motor(2, 3, True)            # forward, backward, pwm
pteranodon_motor_enable = OutputDevice(4)
yellow_button = Button(17)

# Other variables
red_button = Button(9)

########################################################################
#                           Initialize                                 #
########################################################################

pygame.mixer.init()

logging.basicConfig(filename='Files/Dinosaur_Den.log', filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%m/%d/%y %I:%M:%S %p:')

########################################################################
#                          Functions                                   #
########################################################################


def main():
    '''
    This is the main function. It will wait until one of the buttons is
    pressed. There is one button for each of the dinosaurs. When
    pressed, it will activate the specified dinosaur. The red button
    will stop the program. Pressing Ctrl-C will also stop the program.
    '''
    try:
        logging.info("START")
        # STEP01: Check to see that the necessary files exist.
        file_check()
        # STEP02: Check to see if files are accessible.
        permission_check()
        # STEP03: Read the dinosaur_facts.txt file to populate the
        # dino_facts list.
        dino_facts = read_file("Files/dinosaur_facts.txt")
        # STEP04: Check to see if the dino_facts file is empty.
        empty_file_check(dino_facts)
        # STEP05: Acknowledge that prelimiary checks are complete.
        logging.info("Prelimiary checks are complete. Starting program...")
        # STEP06: Display program header.
        print_header()
        # STEP07: Prompt the user to press a button.
        prompt_user_for_input()
        # STEP08: Wait for the user to press a button, then run the
        # function associated with that button.
        while True:

            if white_button.is_pressed:
                # STEP08.A.1: Load the sound file
                roar, roar_length = get_roar()
                # STEP08.A.2: Print out a random dinosaur fun fact
                print_dinosaur_fact(dino_facts)
                # STEP08.A.3: Move the T. rex for the duration of the
                # sound file
                activate_dinosaur(t_rex_motor, t_rex_motor_enable, roar,
                                  roar_length)
                # STEP08.A.4: Prompt the user to press a button
                prompt_user_for_input()

            if green_button.is_pressed:
                # STEP08.B.1: Load the sound file
                grunt, grunt_length = get_grunt()
                # STEP08.B.2: Print out a random dinosaur fun fact
                print_dinosaur_fact(dino_facts)
                # STEP08.B.3: Move the Triceratops for the duration of
                # the sound file
                activate_dinosaur(triceratops_motor, triceratops_motor_enable,
                                  grunt, grunt_length)
                # STEP08.B.4: Prompt the user to press a button
                prompt_user_for_input()

            if blue_button.is_pressed:
                # STEP08.C.1: Load the sound file
                bellow, bellow_length = get_bellow()
                # STEP08.C.2: Print out a random dinosaur fun fact
                print_dinosaur_fact(dino_facts)
                # STEP08.C.3: Move the Brachiosaurus for the duration of
                # the sound file
                activate_dinosaur(brachiosaurus_motor,
                                  brachiosaurus_motor_enable, bellow,
                                  bellow_length)
                # STEP08.C.4: Prompt the user to press a button
                prompt_user_for_input()

            if yellow_button.is_pressed:
                # STEP08.D.1: Load the sound file
                squawk, squawk_length = get_squawk()
                # STEP08.D.2: Print out a random dinosaur fun fact
                print_dinosaur_fact(dino_facts)
                # STEP08.D.3: Move the Pteranodon for the duration of
                # the sound file
                activate_dinosaur(pteranodon_motor, pteranodon_motor_enable,
                                  squawk, squawk_length)
                # STEP08.D.4: Prompt the user to press a button
                prompt_user_for_input()

            if red_button.is_pressed:
                # STEP08.E.1: Stop the program
                stop_the_program()

    except KeyboardInterrupt:
        stop_the_program()


def file_check():
    '''
    The file_check function checks to see if the necessary files exist.
    If they all exist, the program will continue.
    If a file is missing, the program will print out a message to the
    screen and then exit.
    '''

    file_missing_flag = 0

    sounds = ['T_rex1.ogg', 'T_rex2.ogg', 'T_rex3.ogg', 'T_rex4.ogg',
              'T_rex5.ogg', 'T_rex6.ogg', 'T_rex7.ogg', 'T_rex8.ogg',
              'Triceratops1.ogg', 'Triceratops2.ogg', 'Triceratops3.ogg',
              'Triceratops4.ogg', 'Triceratops5.ogg', 'Triceratops6.ogg',
              'Triceratops7.ogg', 'Triceratops8.ogg', 'Brachiosaurus1.ogg',
              'Brachiosaurus2.ogg', 'Brachiosaurus3.ogg', 'Brachiosaurus4.ogg',
              'Brachiosaurus5.ogg', 'Brachiosaurus6.ogg', 'Brachiosaurus7.ogg',
              'Brachiosaurus8.ogg', 'Pteranodon1.ogg', 'Pteranodon2.ogg',
              'Pteranodon3.ogg', 'Pteranodon4.ogg']

    logging.info("FILE CHECK")
    # Check to see if dinosaur_facts.txt file exists
    if os.path.isfile('Files/dinosaur_facts.txt'):
        logging.info("dinosaur_facts.txt file was found!")
    else:
        logging.error("dinosaur_facts.txt file was not found! Make sure " +
                      "that the dinosaur_facts.txt file exists in the Files " +
                      "folder.")
        file_missing_flag = 1

    # Check to see if sound files exists
    for sound in sounds:
        if os.path.isfile('Sounds/' + sound):
            logging.info("{} file was found!".format(sound))
        else:
            logging.error("{} file was not found! Make sure ".format(sound) +
                          "that the {} file exists in the ".format(sound) +
                          "'Sounds' folder.")
            file_missing_flag = 1

    # If there are no missing files, return to the main function
    # Otherwise print out message and exit the program
    if file_missing_flag == 0:
        return
    else:
        print("\033[1;31;40m\nCould not run the program. Some files are " +
              "missing. Check the log in the 'Files' folder for more " +
              "information.\n")
        stop_the_program()


def permission_check():
    '''
    The permission_check function checks to see if the user has
    permission to read the necessary files. If so, the program will
    continue. If not, the program will print out a message to the screen
    and then exit.
    '''

    permission_flag = 0

    sounds = ['T_rex1.ogg', 'T_rex2.ogg', 'T_rex3.ogg', 'T_rex4.ogg',
              'T_rex5.ogg', 'T_rex6.ogg', 'T_rex7.ogg', 'T_rex8.ogg',
              'Triceratops1.ogg', 'Triceratops2.ogg', 'Triceratops3.ogg',
              'Triceratops4.ogg', 'Triceratops5.ogg', 'Triceratops6.ogg',
              'Triceratops7.ogg', 'Triceratops8.ogg', 'Brachiosaurus1.ogg',
              'Brachiosaurus2.ogg', 'Brachiosaurus3.ogg', 'Brachiosaurus4.ogg',
              'Brachiosaurus5.ogg', 'Brachiosaurus6.ogg', 'Brachiosaurus7.ogg',
              'Brachiosaurus8.ogg', 'Pteranodon1.ogg', 'Pteranodon2.ogg',
              'Pteranodon3.ogg', 'Pteranodon4.ogg']

    logging.info("PERMISSION CHECK")
    # Check to see if user has read access to dinosaur_facts.txt
    if os.access('Files/dinosaur_facts.txt', os.R_OK):
        logging.info("User has permission to read the dinosaur_facts.txt " +
                     "file.")
    else:
        logging.error("User does not have permission to read the " +
                      "dinosaur_facts.txt file.")
        permission_flag = 1

    # Check to see if user has read access to sound files
    for sound in sounds:
        if os.access('Sounds/' + sound, os.R_OK):
            logging.info("User has permission to read the " +
                         "{} file.".format(sound))
        else:
            logging.error("User does not have permission to read the " +
                          "{} file.".format(sound))
            permission_flag = 1

    if permission_flag == 0:
        return
    else:
        print("\033[1;31;40m\nCould not run the program. Check the log " +
              "in the 'Files' folder for more information.")
        stop_the_program()


def read_file(file_name):
    '''
    The read_file function has one parameter: file_name. In this
    program, the argument passed in will be the dinosaur_facts.txt file
    located in the 'Files' folder. Each line of the file will be an
    element in the dino_facts list. It will then return the dino_facts
    list to the main function. If the program is unable to populate the
    list, it will display an error message and then exit the program.
    '''

    logging.info("READING DINOSAUR_FACTS.TXT")
    try:
        with open(file_name, "r") as facts:     # open the file as read-only
            dino_facts = facts.readlines()
        logging.info("The dino_facts list was successfully populated.")
    except IOError:
        print("\033[1;31;40mErrors were encountered. Check the log in the " +
              "'Files' folder for more information.")
        logging.error("The dino_facts list could not be populated.")
        stop_the_program()

    return dino_facts


def empty_file_check(list_name):
    '''
    The empty_file_check function has one parameter: file_name. In this
    program, the argument passed in will be the dino_facts list. It will
    checks to see if the list is empty. If it is, the program will print
    a message to the screen. If it is not empty, the program will
    continue.
    '''

    logging.info("EMPTY FILE CHECK")
    if list_name == []:
        logging.error("The dinosaur.txt file is empty. The program won't " +
                      "work.")
        print("\033[1;31;40mErrors were encountered. Check the log in the " +
              "'Files' folder for more information.")
        stop_the_program()
    else:
        logging.info("The dinosaur.txt file is not empty.(This is good. We " +
                     "don't want an empty file.)")


def print_header():
    '''
    The print_header function will print out the program header to the
    screen.
    This is the only part of the program that doesn't adhere to
    PEP standards (exceeds recommended line length). I decided that
    "Readability Counts" and "Beautiful is better than ugly" from The
    Zen of Python should trump the PEP standards in this case. I had
    rewritten it to meet the PEP standard, but is was ugly and
    unreadable. This is much better. The program still compiles and runs
    OK.
    '''

    print("\n\033[1;37;40m")
    print("==================================================================================")
    print("   _  _   ____    ____  _                                    ____                 ")
    print("  | || | |  _ \  |  _ \(_)_ __   ___  ___  __ _ _   _ _ __  |  _ \  ___ _ __      ")
    print("  | || |_| | | | | | | | | '_ \ / _ \/ __|/ _` | | | | '__| | | | |/ _ \ '_ \     ")
    print("  |__   _| |_| | | |_| | | | | | (_) \__ \ (_| | |_| | |    | |_| |  __/ | | |    ")
    print("     |_| |____/  |____/|_|_| |_|\___/|___/\__,_|\__,_|_|    |____/ \___|_| |_|    ")
    print("                                                                                  ")
    print("==================================================================================")
    print("\n")


def prompt_user_for_input():
    '''
    The prompt_user_for_input function prompts a user to push a button.
    '''
    # First line - print all white text
    print("\033[1;37;40mPush the white button to activate the T. Rex.")
    # Second line
    print("\033[1;37;40mPush the " +                 # print white text
          "\033[1;32;40mgreen button " +             # print green text
          "\033[1;37;40mto activate the " +          # print white text
          "\033[1;32;40mTriceratops.")               # print green text
    # Third line
    print("\033[1;37;40mPush the " +                 # print white text
          "\033[1;34;40mblue button " +              # print blue text
          "\033[1;37;40mto activate the " +          # print white text
          "\033[1;34;40mBrachiosaurus.")             # print blue text
    # Fourth line
    print("\033[1;37;40mPush the " +                 # print white text
          "\033[1;33;40myellow button " +            # print yellow text
          "\033[1;37;40mto activate the " +          # print white text
          "\033[1;33;40mPteranodon.")                # print yellow text
    # Fifth line
    print("\033[1;37;40mPush the " +                 # print white text
          "\033[1;31;40mred button " +               # print red text
          "\033[1;37;40mor press Ctrl-C to " +       # print white text
          "\033[1;31;40mstop " +                     # print red text
          "\033[1;37;40mthe program.\n")             # print white text


def print_dinosaur_fact(dino_facts):
    '''
    The print_dinosaur_fact function takes the dino_facts list as its
    input. It will select a random fact and print it out.
    '''

    print("\033[1;34;40mDINOSAUR FUN FACT:")
    print(random.choice(dino_facts))


def get_roar():
    '''
    The get_roar function will randomly select one of the T. rex roar
    files and return it and its file length to the main function.
    '''

    # The key/value pair is sound file name : length of file in seconds
    roars = {'Sounds/T_rex1.ogg': 6.5, 'Sounds/T_rex2.ogg': 3,
             'Sounds/T_rex3.ogg': 4, 'Sounds/T_rex4.ogg': 5.5,
             'Sounds/T_rex5.ogg': 4, 'Sounds/T_rex6.ogg': 6,
             'Sounds/T_rex7.ogg': 4.5, 'Sounds/T_rex8.ogg': 4}

    return random.choice(list(roars.items()))


def get_grunt():
    '''
    The get_grunt function will randomly select one of the Triceratops
    grunt files and return it and its file length to the main function.
    '''

    # The key/value pair is sound file name : length of file in seconds
    grunts = {'Sounds/Triceratops1.ogg': 5, 'Sounds/Triceratops2.ogg': 4,
              'Sounds/Triceratops3.ogg': 4, 'Sounds/Triceratops4.ogg': 4,
              'Sounds/Triceratops5.ogg': 5, 'Sounds/Triceratops6.ogg': 3,
              'Sounds/Triceratops7.ogg': 2, 'Sounds/Triceratops8.ogg': 3}

    return random.choice(list(grunts.items()))


def get_bellow():
    '''
    The get_bellow function will randomly select one of the Brachiosaurus
    bellow files and return it and its file length to the main function.
    '''

    # The key/value pair is sound file name : length of file in seconds
    bellows = {'Sounds/Brachiosaurus1.ogg': 5, 'Sounds/Brachiosaurus2.ogg': 4,
               'Sounds/Brachiosaurus3.ogg': 4, 'Sounds/Brachiosaurus4.ogg': 4,
               'Sounds/Brachiosaurus5.ogg': 5, 'Sounds/Brachiosaurus6.ogg': 3,
               'Sounds/Brachiosaurus7.ogg': 2, 'Sounds/Brachiosaurus8.ogg': 3}

    return random.choice(list(bellows.items()))


def get_squawk():
    '''
    The get_squawk function will randomly select one of the Pteranodon
    squawk files and return it and its file length to the main function.
    '''

    # The key/value pair is sound file name : length of file in seconds
    squawks = {'Sounds/Pteranodon1.ogg': 6.5, 'Sounds/Pteranodon2.ogg': 6.5,
               'Sounds/Pteranodon3.ogg': 6, 'Sounds/Pteranodon4.ogg': 6}

    return random.choice(list(squawks.items()))


def activate_dinosaur(motor_name, motor_name_enable, sound, sound_length):
    '''
    The activate_dinosaur function will play the sound file and then
    activate the specified motor for the duration of the sound file.
    This function has 4 parameters: motor_name, motor_name_enable,
    sound (a sound file) and sound_length (the length of the sound file
    in seconds).
    The arguments passed in will vary depending on which button was
    pressed. For example, if the T. rex button was pressed, the
    arguments passed in will be t_rex_motor, t_rex_motor_enable, roar,
    and roar_length.
    '''

    motor = motor_name
    motor_enable = motor_name_enable

    try:
        motor.value = 0.6              # Controls the motor speed
    except ValueError:
        logging.error("A bad value was specified for the {}. ".format(motor) +
                      "The value should be between 0 and 1.")
        print("\033[1;31;40mAn error was encountered. Check the log in the " +
              "'Files' folder for more information.\n")
        stop_the_program()
    pygame.mixer.music.load(sound)     # Loads the sound file
    motor_enable.on()                  # Starts the motor
    pygame.mixer.music.play()          # Plays the sound file
    sleep(sound_length)                # Length of sound file in seconds
    motor_enable.off()                 # Stops the motor


def release_gpio_pins():
    '''
    The release_gpio_pins function realeases the gpio pins.
    '''

    t_rex_motor.close()
    t_rex_motor_enable.close()
    triceratops_motor.close()
    triceratops_motor_enable.close()
    brachiosaurus_motor.close()
    brachiosaurus_motor_enable.close()
    pteranodon_motor.close()
    pteranodon_motor_enable.close()
    white_button.close()
    green_button.close()
    blue_button.close()
    yellow_button.close()
    red_button.close()


def stop_the_program():
    '''
    The stop_the_program function will call the release_gpio_pins
    function, print a message to the screen, and then exit the program.
    '''

    release_gpio_pins()
    print("\033[1;37;40mExiting program.\n")
    logging.info("END")
    exit()


if __name__ == '__main__':
    main()
