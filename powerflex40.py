#!/usr/bin/python3

#powerflex40.py
#Copyright (C) 2017  Cygnus Technical Services Ltd.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.


import datetime
import minimalmodbus
import csv

commport = '/dev/ttyUSB0'
results = '{}-results.csv'.format(datetime.datetime.now().strftime("%Y%m%d"))

VFDs = [
('TC2-1',1),
('TC2-2',2),
('TC2-3',3),
('TC1-1',4),
('TC1-2',5),
('TC1-3',6),
('TC1-4',7),
('TC1-5',8),
('TC1-6',9),
('TC1-7',10),
('TC1-8',11),
('TC1-9',12),
('SB1-1',13),
('SB1-2',14),
('SB1-3',15),
('SB1-4',16),
('SB1-5',17),
('SB1-6',18),
('CB1-1',19),
('CB1-2',20),
('CB1-3',21),
('CB1-4',22),
('MU1-1',23),
('MU1-4',24),
('MTR-8',25)
]

class Powerflex40VFD(minimalmodbus.Instrument):
  def __init__(self, portname, slaveaddress):
    minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
    self.dRange = (1,29)
    self.pRange = (31,43)
    self.aRange = (51,167)
    self.skipparams = [
      57,
      60,
      63,
      148,
      149,
      158,
      159
      ]
    self.divideByTenParams = [
      33,34,
      39,40,
      56,
      59,
      62,
      67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,
      85,86,87,
      89,
      91,
      93,
      98,99,
      106,
      109,110,111,112,113,114,
      118,
      120,
      126,
      128,
      130,131,
      135,
      137,138,139,
      150,151,152,153,154,155,156,157,
      163,
      165]
    self.fourDigitHexParams = [
      102,
      140,141,142,143,144,145,146,147
      ]
    self.divideByHundredParams = [
      115,116,
      129,
      134,
      136,
      160,161
      ]
      
    self.mode = minimalmodbus.MODE_RTU
    
    self.serial.baudrate = 9600
    
    
  def getParam(self, paramNumber):
    if (
        ((not (self.dRange[0] <= paramNumber <= self.dRange[1])) and
        (not (self.pRange[0] <= paramNumber <= self.pRange[1])) and
        (not (self.aRange[0] <= paramNumber <= self.aRange[1])))
        or paramNumber in self.skipparams):
      raise ValueError("Parameter number is out of range: {}".format(paramNumber))
    
    modbusVal = self.read_register(paramNumber, 0)
    if paramNumber in self.divideByTenParams:
      val = modbusVal/10
    elif paramNumber in self.divideByHundredParams:
      val = modbusVal/100
    elif paramNumber in self.fourDigitHexParams:
      val = "{:04X}".format(modbusVal)
    else:
      val = modbusVal
    return val

  def getAllParameters(self):
    ret = list()
    
    # dRange:
    # Don't care about saving this range
    #for addr in range(self.dRange[0], self.dRange[1]+1):
    #  if addr in self.skipparams:
    #    continue
    #  ret.append(["d{:03d}".format(addr), self.getParam(addr)])
      
    # pRange:
    for addr in range(self.pRange[0], self.pRange[1]+1):
      if addr in self.skipparams:
        continue
      ret.append(["p{:03d}".format(addr), self.getParam(addr)])
      
    # aRange:
    for addr in range(self.aRange[0], self.aRange[1]+1):
      if addr in self.skipparams:
        continue
      ret.append(["a{:03d}".format(addr), self.getParam(addr)])
      
    return ret
  
if __name__ == "__main__":
    csvPrefix = datetime.datetime.now().strftime("%Y%m%d")
    with open(results, "w") as resultsFile:
      resultscsv = csv.writer(resultsFile)
      resultscsv.writerow(['VFD', 'Address', 'Result'])
      for vfddecl in VFDs:
        vfdname = vfddecl[0]
        addr = vfddecl[1]
        print("Polling {} ({})".format(vfdname, addr))
        vfd = Powerflex40VFD(commport, addr)
        #print(vfd)
        try:
          params = vfd.getAllParameters()
        except IOError:
          print("...Failed")
          resultscsv.writerow([vfdname, addr, 'Failed'])
          continue
        filename = csvPrefix+"-"+vfdname+"-parameters.csv"
        with open(filename, "w") as outfile:
          csvout = csv.writer(outfile)
          csvout.writerow(["VFD:",vfdname])
          nowish = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
          csvout.writerow(["Exported:", nowish])
          csvout.writerow(["Parameter", "Value"])
          for answer in params:
            csvout.writerow([answer[0],str(answer[1])])
        resultscsv.writerow([vfdname, addr, 'Success'])
      
