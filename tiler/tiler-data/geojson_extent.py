import subprocess
import sys

## Check all our variables are in order
if len(sys.argv) > 1:
    FILE_NAME = sys.argv[1]
else:
    raise  ValueError("FILE_NAME not defined")

process = subprocess.Popen('ogrinfo -ro -so -al {} | grep "Extent:"'.format(FILE_NAME), shell=True, stdout=subprocess.PIPE)
for line in iter(process.stdout.readline,''):
   extent = line.rstrip()

extent = extent.replace("Extent: ", "")
extent = extent.replace("(", "").replace(")", "").replace(" - ", ", ")
extent = "[" + extent + "]"
print extent

# stdout, stderr = process.communicate()
# print "Stout", stdout
# print "Sterr", stderr
# print "Exit code: ", process.wait()

