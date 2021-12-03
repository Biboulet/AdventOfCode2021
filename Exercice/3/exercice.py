import os
import utils

scans = utils.read_file(os.getcwd() + "\\input.txt")


def get_gamma_rate(scans):
    octet = []
    for index in range(len(scans[0]) - 1):
        one_count = 0
        for line in scans:
            if line[index] == "1":
                one_count += 1
        if one_count > len(scans)//2:
            octet.append(1)
        else:
            octet.append(0)

    return octet


def get_epsilon(gama_rate):
    opsilion = []
    for bit in gama_rate:
        if bit == 1:
            opsilion.append(0)
        else:
            opsilion.append(1)
    return opsilion


def convert_dec(binary):
    octet = []
    if str(isinstance(binary, str)):
        binary = binary.split("\n")[0]
        octet = list(map(int, binary))
    else:
        octet = binary

    a = sum([2 ** index for index in range(len(octet)) if octet[-(index+1)] == 1])
    return a


def Part1():
    gama_rate = get_gamma_rate(scans)
    epsilon = get_epsilon(gama_rate)
    power = convert_dec(gama_rate) * convert_dec(epsilon)
    print(power)


def get_rating(numberList, bitcriteraia, index=0):
    number_with_index_1 = []
    number_with_index_0 = []

    for number in numberList:
        if number[index] == "1":
            number_with_index_1.append(number)
        else:
            number_with_index_0.append(number)

    final_numbers = []
    if bitcriteraia == "most":
        if len(number_with_index_1) > len(number_with_index_0):
            final_numbers = number_with_index_1
        elif len(number_with_index_1) == len(number_with_index_0):
            final_numbers = number_with_index_1
        else:
            final_numbers = number_with_index_0
    else:
        if len(number_with_index_1) < len(number_with_index_0):
            final_numbers = number_with_index_1
        elif len(number_with_index_1) == len(number_with_index_0):
            final_numbers = number_with_index_0
        else:
            final_numbers = number_with_index_0
    if len(final_numbers) == 1:
        return final_numbers[0]
    return get_rating(final_numbers, bitcriteraia, index+1)


if __name__ == "__main__":
    oxygen = get_rating(scans, "most")
    co2 = get_rating(scans, "least")

    life_support = convert_dec(oxygen) * convert_dec(co2)
    print(life_support)

