#############################################################################################
#           File: config.py                                                                 #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 12/2/15 ? 25/2/15  ?  5/3/15  ?   7/3/15                           #
#############################################################################################

# reading configuration from file
import config # used for config.__dict__, you can't access it from the module itself
file = open("config.cfg")
text = file.read().split("\n")
file.close()
for line in text:
    if line[0] == "#": continue
    line = line.split(":")
    config.__dict__[line[0]] = eval(line[1])
    
