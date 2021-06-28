import os

a = open("/data/output/SCHATSI_included.txt", "w")
for path, subdirs, files in os.walk(r'/data/input'):
    for filename in files:
        f = os.path.join(path, filename)
        a.write(str(f) + os.linesep)
