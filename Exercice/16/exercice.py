import os
import utils
from math import prod

scans = utils.read_file(os.getcwd() + "\\input.txt")
HexBinDict = {"0": [0, 0, 0, 0], "1": [0, 0, 0, 1],
              "2": [0, 0, 1, 0], "3": [0, 0, 1, 1],
              "4": [0, 1, 0, 0], "5": [0, 1, 0, 1],
              "6": [0, 1, 1, 0], "7": [0, 1, 1, 1],
              "8": [1, 0, 0, 0], "9": [1, 0, 0, 1],
              "A": [1, 0, 1, 0], "B": [1, 0, 1, 1],
              "C": [1, 1, 0, 0], "D": [1, 1, 0, 1],
              "E": [1, 1, 1, 0], "F": [1, 1, 1, 1]}


class Packet:
    def __init__(self, octets):
        self.packet_version = BinToDec(octets[:3])
        self.packet_type_ID = BinToDec(octets[3:6])

        if self.is_litteral_value():

            total_octet = []
            index = 6
            prefix = octets[index]
            while prefix == 1:
                total_octet += octets[index+1:index+5]
                index += 5
                prefix = octets[index]

            #pour le dernier package (celui qui commence par 0)
            total_octet += octets[index+1:index+5]
            self.value = BinToDec(total_octet)
            self.length = index+5

        else:
            self.length_type_ID = octets[6]
            self.sub_packets = []

            #type 15-bit (longeur total de tt les packets enfant)
            if self.length_type_ID == 0:
                length_of_total_sub_packets = BinToDec(octets[7:22])
                index = 22
                while length_of_total_sub_packets > 0:
                    sub_packet = Packet(octets[index:])
                    self.sub_packets.append(sub_packet)

                    index+=sub_packet.length
                    length_of_total_sub_packets -= sub_packet.length
                assert length_of_total_sub_packets == 0
                self.length = index

            #type 11-bit (nombre de packet enfant)
            else:
                number_sub_packets = BinToDec(octets[7:18])
                index = 18
                for i in range(number_sub_packets):
                    sub_packet = Packet(octets[index:])
                    self.sub_packets.append(sub_packet)
                    index += sub_packet.length
                self.length = index
            
            self.value = self.get_value()


    def is_litteral_value(self):
        return self.packet_type_ID == 4

    def sum_version_number(self):
        if self.is_litteral_value():
            return self.packet_version
        else:
            return self.packet_version + sum([sub.sum_version_number() for sub in self.sub_packets])

    def get_value(self):
        if self.packet_type_ID == 0:
            return sum([packet.value for packet in self.sub_packets])
        if self.packet_type_ID == 1:
            return prod([packet.value for packet in self.sub_packets])
        if self.packet_type_ID == 2:
            return min([packet.value for packet in self.sub_packets])
        if self.packet_type_ID == 3:
            return max([packet.value for packet in self.sub_packets])
        if self.packet_type_ID == 5:
            if self.sub_packets[0].value > self.sub_packets[1].value:
                return 1
            else:
                return 0
        if self.packet_type_ID == 6:
            if self.sub_packets[0].value < self.sub_packets[1].value:
                return 1
            else:
                return 0
        if self.packet_type_ID == 7:
            if self.sub_packets[0].value == self.sub_packets[1].value:
                return 1
            else:
                return 0



def BinToDec(octet):
    return sum([2 ** index for index in range(len(octet)) if octet[-(index + 1)] == 1])


def HexToBin(string):
    octet = []
    for char in string:
        octet += HexBinDict[char]
    return octet


if __name__ == "__main__":
    binary_input = HexToBin(scans[0])
    First_Layer_Packet = Packet(binary_input)
    print(First_Layer_Packet.value)
