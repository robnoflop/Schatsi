import os

a = open("SCHATSI_included.txt", "w")
for path, subdirs, files in os.walk(r'C:\\Users\\dokha\\OneDrive\\Projects\\Literature Research\\SCHATSI\\Topic Modeling'):
   for filename in files:
     f = os.path.join(path, filename)
     a.write(str(f) + os.linesep) 
