import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


class FourDigitDisplay:
    def __init__(self, list_input, list_output):
        self.unique_patterns = [Display(value) for value in list_input]
        self.output = [Display(value) for value in list_output]


class Display:
    def __init__(self, activated):
        self.activated = [segment for segment in activated]
        self.value = -1

    def __add__(self, other):
        return Display((self - other).activated + other.activated)

    def __sub__(self, other):
        return Display([segment for segment in self.activated if segment not in other.activated])

    def __eq__(self, other):

        a = all([seg in other.activated for seg in self.activated])
        b = all([seg in self.activated for seg in other.activated])
        return a and b


def instantiate_display(scans):
    displays = []
    for line in scans:
        list_input = line.split(" | ")[0].split()
        list_output = line.split(" | ")[1].split()
        displays.append(FourDigitDisplay(list_input, list_output))

    return displays


def get_output(four_didgit_displays):
    count = 0
    for big_display in four_didgit_displays:

        digit = []
        for output in big_display.output:
            value = [display for display in big_display.unique_patterns if display == output][0].value
            digit.append(value)

        number = sum([digit[-(index+1)] * 10**index for index in range(4)])
        count+=number
    return count


def resolve(four_digit_diplays):
    for big_diplay in four_digit_diplays:

        all_paterns = [None, None, None, None, None, None, None, None, None, None]

        # on set les patterne primaire
        for display in big_diplay.unique_patterns:

            if len(display.activated) == 2:
                display.value = 1
                all_paterns[1] = display

            elif len(display.activated) == 4:
                display.value = 4
                all_paterns[4] = display

            elif len(display.activated) == 3:
                display.value = 7
                all_paterns[7] = display

            elif len(display.activated) == 7:
                display.value = 8
                all_paterns[8] = display


        bot_and_left_bot = all_paterns[8] - (all_paterns[4] + all_paterns[7])
        #on set les patterne a 6 segemtn
        for display in big_diplay.unique_patterns:
            if len(display.activated) == 6:
                if not ((all_paterns[1] + bot_and_left_bot) - display).activated:
                    display.value = 0
                    all_paterns[0] = display

                elif not (all_paterns[1] - display).activated:
                    display.value = 9
                    all_paterns[9] = display

                else:
                    display.value = 6
                    all_paterns[6] = display


        # on fait le reste
        up_right = all_paterns[8] - all_paterns[6]
        for display in big_diplay.unique_patterns:
            if len(display.activated) == 5:
                if not ((all_paterns[1]) - display).activated:
                    display.value = 3
                    all_paterns[3] = display

                elif not (up_right - display).activated:
                    display.value = 2
                    all_paterns[2] = display

                else:
                    display.value = 5
                    all_paterns[5] = display


        big_diplay.unique_patterns = all_paterns


if __name__ == "__main__":
    four_digit_displays = instantiate_display(scans)
    resolve(four_digit_displays)
    outputs = get_output(four_digit_displays)
    print(outputs)
