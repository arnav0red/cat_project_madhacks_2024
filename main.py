class VirtualDevice:
    def __init__(self, input: str):
        input = input.split(" ")
        if input[0] != "001":
            raise Exception("Couldn't find start of connection")
        elif input[-1] != "100":
            raise Exception("Couldn't find end of connection")
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

    def __repr__(self):
        return f"""ACK: {self.ACK}, STS: {self.STS}, listALL: {self.listALL}, listSTS: {self.listSTS}, LVL: {self.LVL}, END: {self.END},"""

    def response(self):
        if not self.ACK:
            raise Exception("Couldn't find start of connection")
        elif not self.END:
            raise Exception("Couldn't find end of connection")
        message = "001 "
        for i in self.listSTS:
            message += "110 111 "
            if int(i) == 1:
                message += "101 "
        if self.LVL:
            message += "100110 "
        message += "100"
        return message

    def __repr__(self):
        return f"""ACK: {self.ACK}, FLT: {self.FLT}, listFLT: {self.listFLT}, OKY: {self.OKY}, LVL: {self.LVL}, fuelLVL: {self.fuelLVL}, END: {self.END},"""


exampleSessionRecord = "001 010 000 010 000001 010 000011 011 100"
# exampleSensorRespose = "001 110 111 101 110 111 011 100110 100"
with open("Session.txt","r") as file:
    for i in file.readlines():
        print(VirtualDevice(i).response())
