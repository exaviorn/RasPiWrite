#!/usr/bin/env python

#   ;d0KOd.  .oOK0x:  
#  0xlllcoxolkolllloX 
#  ;OccloddKNdxdocckc 
#   .dkddkWNNMOdoxd,  
#   .o:,x0....xd,ck'  
#   K:xOoloOOccloocW  
# .x;N:....xO....'K;k,
# O..Nc...:XNl...:X.,X
# .kkx0NXk'...dNNxldK'
#  'k...0o....,O...d: 
#   ;o;'oM0olkWc.;oc  
#     .cOx....dOl.    
#        .x00k.    

#//////////////////////// 
#* Raspberry Pi SD Writer 
#* Matt Jump
#* exaviorn.com
#////////////////////////
# Copyright Matthew Jump 2012
# The following code is licenced under the Gnu Public Licence, please see gpl.txt for reference
#  This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# VERSION 1.0 -MACOSX- (March 2012)
#	* For support, please go to raspi.exaviorn.com, or go to our github (https://github.com/exaviorn/RasPiWrite)
#	* The script currently only works for Macs, however it can be changed with very little alterations, 
#	  I will add in OS detection logic and the subsequent functions from there

import re, os, urllib2, time, sys, threading
from commands import *
from sys import exit
from random import choice


#Display Augs
boldStart = "\033[1m"
end = "\033[0;0m"
WARNING = '\033[0;31m' #0;31

def findDL(OS): 	#got first 8 of the EUROPEAN mirrors (sorry, will work on global stuff later!), one is selected at random and returned as a string
	debian = ['http://files.velocix.com/c1410/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	 			'http://raspberrypi.nibelheim.ch/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	  			'http://www.marianm.net/pi/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	 			'http://85.199.153.78/mirror/pub/linux/raspberrypi/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	 			'http://mirror.bytemark.co.uk/raspberrypi/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	 			'http://only4you.in/raspberrypi/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	 			'http://mirrors.starteffect.com/rpi/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip',
	 			'http://mirrors.melbourne.co.uk/sites/downloads.raspberrypi.org/images/debian/6/debian6-17-02-2012/debian6-17-02-2012.zip']

	arch = ['http://files.velocix.com/c1410/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://raspberrypi.arrabonus.hu/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://m1.raspberrypi.itechcon.it/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://raspberrypi.rloewe.net/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://91.203.212.159/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://131.220.23.128/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://rpi.stream-in-box.com/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip',
			'http://85.199.153.78/mirror/pub/linux/raspberrypi/images/archlinuxarm/archlinuxarm-01-03-2012/archlinuxarm-01-03-2012.zip']

	fedora = ['http://achtbaan.nikhef.nl/events/rpi/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://mirror.star.net.uk/raspberrypi/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://www.sqltuning.cz/raspberry/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://raspberrypi.peir.com/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://raspberrypi.mirror.triple-it.nl/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://ftp.ticklers.org/RaspberryPi/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://files.velocix.com/c1410/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz',
			'http://raspberrypi.reon.hu/images/fedora/14/r1-06-03-2012/raspberrypi-fedora-remix-14-r1.img.gz']
	if OS == 'arch': return choice(arch)
	if OS == 'debian': return choice(debian)
	if OS == 'fedora': return choice(fedora)


def download(url):		#http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python | Downloads the disk image for the user
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)
	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break
	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,
	f.close()

def cleanOutput(text, text2):	#cleans up the output from df -h
	#^(?=.*?\b/\b)(?=.*?\bdisk0)((?!Volume).)*$ <-- regex used
	filename = "Example_file_(extra_descriptor).ext"
	removeGarbage = re.compile(r'(?=devfs)([^>]*)(?=/dev/)')
	removeRootHDD = re.compile(r"(?=.*?\b/\b)(?=.*?\bdisk0)((?!Volume).)*")
	cleanOutput = re.sub(removeRootHDD, '', re.sub(removeGarbage, '', text2))
	return cleanOutput

def matchSD(input):	#grabs just the drive's name from the df -h command (macOSX so far)
	selectSD = r"(?=/)(.*?)\s"
	match =  re.search(selectSD, input)
	return match

def unmount(location):	#unmounts the drive so that it can be rewrittern
	print 'Unmounting the drive in preparation for writing...'
	output = getoutput('diskutil unmount ' + location)
	print output
	if 'Unmount failed for' in output:
		print WARNING + 'Error, the Following drive couldn\'t be unmounted, exiting...' + end
	exit() #<-- commented out for debugging purposes

class transferInBackground (threading.Thread): 	#Runs the dd command in a thread so that I can give a waiting... indicator

   def run ( self ):
	global SDsnip
	global path
	copyString = 'dd bs=1m if=%s of=%s' % (path,SDsnip)
	print copyString
	print getoutput(copyString)
	print 'done!'
     

def transfer(file,archiveType,obtain,SD,URL):	#unzips the disk image
	global path
	if archiveType == 'zip': 
		path =  file.replace(".zip", "") + '/' + file.replace(".zip", ".img")
		extractCMD = 'unzip ' + file
	if archiveType == 'gz': 
		path =  file.replace(".gz", "") #<-- verify
		extractCMD = 'gunzip ' + file

	if obtain == 'dl': obtainType = 'Downloaded by this client (reliable and safe)'
	if obtain == 'usr': obtainType = 'Obtained by user and passed in (potentially dangerous)'

	if (os.path.exists(path)):
		print 'archive already has been extracted, skipping unzipping...'
	else:
		download(URL)
		print 'Ok... Unzipping the disk , this may take a while...'
		print getoutput(extractCMD) #extract here!
	print path
	global SDsnip
	SDsnip =  SD.replace(' ', '')[:-2]
	print SDsnip
	print '\n\n###################################################################'
	print 'About to start the transfer procedure, here is your setup:'
	print """
> OS Choice: %s
> SD Card: %s
> Type: %s
	""" % (file.replace(".zip", ""), SDsnip, obtainType)
	print """
Remember that Matt Jump nor exaviorn.com can be to warranty for any destruction of data or hardware 
(excerpt from GNU GPL, which can be found in the script's source, as well as inside the script's folder):
-----------------------------------------------------------------
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
-----------------------------------------------------------------
	"""
	print '###################################################################\n'
	confirm = raw_input(boldStart + 'Please verify this information before hitting typing \'accept\', if this information isn\'t correct, please press ctrl + c (^C), or type \'exit\' to quit: ' + end)
	if confirm == 'accept':
   		thread1 = transferInBackground()
   		thread1.start()
		sys.stdout.write("Waiting")
   		sys.stdout.flush()
		while thread1.isAlive():
			time.sleep(3)
			sys.stdout.write(".")
   			sys.stdout.flush()
   		print 'Transfer Complete! Please remove the SD card'
   		print """###########################################
Relevent information:
> Debian - Login is pi/suse
> Arch - Login is root/root
> Fedora - Login is root/fedoraarm
###########################################
Thank You for using RasPiWrite, you are now free to eject your drive 
   		"""
	else:
		print 'ENDING WITHOUT COPYING ANY DATA ACROSS, SD CARD HAS BEEN UNMOUNTED'
		exit()

def getImage(SD): #gives the user a bunch of options to download an image, or select their own, it then passes the user on to the transfer function
	global boldStart
	global end
	userChoice = raw_input('Do you wish to Download a Raspberry Pi compatiable image (choose yes if you don\'t have one) (Y/n): ')
	if (userChoice == 'Y') or (userChoice == 'y'):
		print boldStart + """
> Debian \"Squeeze\" [OPTION 1]""" + end + """
Reference root filesystem from Gray and Dom, containing LXDE, Midori, development tools 
and example source code for multimedia functions.
		"""
		print boldStart + """
> Arch Linux [OPTION 2]""" + end + """
Arch Linux ARM is based on Arch Linux, which aims for simplicity and full control to the 
end user. Note that this distribution may not be suitable for beginners.
		"""
		print boldStart + """
> Fedora 14 [OPTION 3]""" + end + """
The Raspberry Pi recommended choice for beginners, features a full GUI and applications for 
productivity and programming
		"""
		osChoice = raw_input('Your Choice e.g: \'1\' : ')
		if osChoice == '1':
			URL = findDL('debian')
			print 'Downloading Debian from [%s]'% URL
			download(URL)
			transfer('debian6-17-02-2012.zip','zip','dl',SD,URL)
		if osChoice == '2':
			URL = findDL('arch')
			print 'Downloading Arch Linux from [%s]'% URL
			download(URL)
			transfer('archlinuxarm-01-03-2012.zip','zip','dl',SD,URL)
		if osChoice == '3':
			URL = findDL('fedora')
			print 'Downloading Fedora 14 from [%s]'% URL
			download(URL)
			transfer('raspberrypi-fedora-remix-14-r1.img.gz','gz','dl',SD, URL)

	if (userChoice == 'N') or (userChoice == 'n'):
		userLocate = raw_input('Please locate the disk image: ')
		if (os.path.exists(userLocate)):
			matchZip = re.match('^.*\.zip$',userLocate)
			matchGzip = re.match('^.*\.img.gz$',userLocate)
			if matchZip is not None:
				print 'Found Zip'
				findDL('debian')
				transfer(userLocate,'zip','usr',SD)

    		elif matchGzip is not None:
    			print 'found Gzip'
    			transfer(userLocate, 'zip', 'usr',SD)
    			
				
		else:
			print 'sorry, the file you have specified doesn\'t exist, please try again'
			print 'Press ctrl + c (^C) to quit'
			exit()

def driveTest(SD):
	if (SD == '/dev') or (SD == '/') or (SD == '/home') or (SD == '/net'):
		print WARNING + """ 
#############################################################
WARNING: THE FOLLOWING PREDICTED LOCATION MAY BE INCORRECT!
	No reliable SD Card location could be found
#############################################################
""" + end
		manualID = raw_input("Please enter the location you believe holds the SD Card: ")
		driveTest(manualID)
	else:
		sdID = raw_input("I Believe this is your SD card: " + SD + " is that correct? (Y/n) ")
		if (sdID == 'Y') or (sdID == 'y'): #continue
			unmount(SD) #<--works, so don't need to test
			getImage(SD)
			
		if (sdID == 'N') or (sdID == 'n'):
			manualID = raw_input("Please enter the location you believe holds the SD Card: ")
			driveTest(manualID)

#logic:
#most of this stuff is pretty self explanitory, some of it could be put into a function, but I don't like 
#having loads of micro functions (the ones I do have are going to be expanded to cover all unix based OS's)
print getoutput('clear')
print boldStart + """
  ;d0KOd.  .oOK0x:  
 0xlllcoxolkolllloX 
 ;OccloddKNdxdocckc 
  .dkddkWNNMOdoxd,  
  .o:,x0....xd,ck'  
  K:xOoloOOccloocW  
.x;N:....xO....'K;k,
O..Nc...:XNl...:X.,X
.kkx0NXk'...dNNxldK'
 'k...0o....,O...d: 
  ;o;'oM0olkWc.;oc  
    .cOx....dOl.    
       .x00k.    
""" + end
print """//////////////////////// """ + boldStart + """
* Raspberry Pi SD Writer """ + end + """
* Matt Jump
* exaviorn.com
////////////////////////
(Version 1.0 -MACOSX-)
"""
OS = os.uname() #gets OS vars
if OS[0] != 'Darwin': #if Mac OS, will change to posix once I have worked around some of the command differences
	print WARNING + 'I\'m sorry, but your os isn\'t supported at this time, Linux/Unix users - please tune in soon for a posix version' + end
	exit()
if not os.geteuid()==0:
	print WARNING + 'Please run the script as root, or use sudo e.g. sudo python raspidwrite.py, or sudo ./raspidwrite.py (need to chmod +x)' + end
	exit()
print 'The following script is designed to copy a Raspberry Pi compatiable disk image to an SD Card'
print boldStart + 'INCORRECTLY FOLLOWING THE WIZARD COULD RESULT IN THE CORRUPTION OF YOUR HARD DISK, PARTITIONS OR A BACKUP USB DRIVE' +end
print 'It is advisable to remove any other USB HDDs or memory sticks, the wizard might select that one, %s if you have multiple hard drives installed, please take a LOT of care selecting the right drive %s'% (boldStart, end) 
text = getoutput('df -h')
raw_input('Now enter your SD Card, press enter when you are ready...')
text2 = getoutput('df -h')
print """
\n---------------------------------------------------------
""" + boldStart + """The following drives were found:
""" + end
volumes =  cleanOutput(text,text2)
print volumes
print '---------------------------------------------------------\n'
SD = matchSD(volumes).group(1) #selects the first SD/USB drive located
driveTest(SD) #action gets delegated to driveTest, which then leads on to the next step, I found this to be the easiest way
