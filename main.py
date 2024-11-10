import pandas as pd
import matplotlib.pyplot as plt
from typing import List
import random


class VirtualDevice:
    def __init__(self, input: str):
        input = input.split(" ")
        # if input[0] != "001":
        #     raise Exception("Couldn't find start of connection")
        # elif input[-1] != "100":
        #     raise Exception("Couldn't find end of connection")
        self.ACK = False
        self.STS = False
        self.listALL = False
        self.listSTS = []
        self.LVL = False
        self.END = False
        i = 0
        while i < len(input):
            read = input[i]
            if read == "001":
                self.ACK = True
            elif read == "100":
                self.END = True
            elif read == "010":
                self.STS = True
                i += 1
                if input[i] == "000":
                    self.listALL = True
                else:
                    self.listSTS.append(input[i])
            elif read == "011":
                self.LVL = True
            i += 1
        self.responseCreator()

    def __repr__(self):
        return f"""ACK: {self.ACK}, STS: {self.STS}, listALL: {self.listALL}, listSTS: {self.listSTS}, LVL: {self.LVL}, END: {self.END},"""

    def responseCreator(self):
        # if not self.ACK:
        #     raise Exception("Couldn't find start of connection")
        # elif not self.END:
        #     raise Exception("Couldn't find end of connection")
        self.message = "001 "
        for i in self.listSTS:
            self.message += "110 111 "
            if int(i) == 1:
                self.message += "101 "
        if self.LVL:

            self.fuelLevelInt = int(random.randrange(0, 50))
            self.fuelLVL = "{0:b}".format(self.fuelLevelInt)
            self.fuelLVL += " "
            self.message += self.fuelLVL

        self.message += "100"

    def response(self):
        return self.message

    def __str__(self):
        return f"""ACK: {self.ACK}, STS: {self.STS}, listFLT: {self.listSTS}, LVL: {self.LVL}, END: {self.END},"""

    def returnFuelLevel(self):
        return self.fuelLevelInt


exampleSessionRecord = "001 010 000 010 000001 010 000011 011 100"
# exampleSensorRespose = "001 110 111 101 110 111 011 100110 100"
listDevices: List[VirtualDevice] = []
with open("Session.txt", "r") as file:
    for i in file.readlines():
        device = VirtualDevice(i)
        listDevices.append(device)
        print(device)
        print("Response: ", device.response())

s = pd.Series([i.returnFuelLevel() for i in listDevices])
fig, ax = plt.subplots()
s.plot.bar()
fig.savefig("fuelLevel.png")
