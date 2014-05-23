#!/usr/bin/python

import argparse
import string
import os
import shutil
import sys


def print_header():
	print('-------------------------')
	print('Password generator\n')
	print('Professor :')
	print('\tMarc Schaeffer')
	print('Created by :')
	print('\tEtienne Frank, Dany juppile')
	print('-------------------------')
	# print("Cet application génère des mots de passe et les stocks dans des fichiers (repertoire ./pass)")
	print("This application generate passwords and store it in files (./pass directory)")
	print("Data are split in 100 mega octet files\n\n")


def is_int(val):
	try:
		int(val)
		return True
	except ValueError:
		return False


def zero_fill(number):
	return str(number).zfill(5)


def word(pass_dir, alphabet, start, deep_start, deep_end, deep_actual=0, file_number=1):
	isFile = False
	if "-f" in sys.argv:
		isFile = True
		file_path = pass_dir+zero_fill(file_number)+'.txt'
		file = open(file_path, 'a')

	if deep_actual >= deep_start:
		for char in alphabet:
			if isFile is False:
				print(start+char)
			else:
				file.write(start+char+'\n')

				# if the file is too big, generate a new file
				if os.stat(file_path).st_size > 100000000:
					file_number += 1
					file.close()
					file_path = pass_dir+zero_fill(file_number)+'.txt'
					file = open(file_path, 'a')

	if isFile is True:
		file.close()

	deep_actual += 1

	if deep_end > 0:
		for char in alphabet:
			word(pass_dir, alphabet, start+char, deep_start, deep_end-1, deep_actual, file_number)

if __name__ == "__main__":

	minChars = 0
	maxChars = 2
	special = [chr(x) for x in range(33, 126)]  # 32 if we want to consider the space as a char
	special = [x for x in special if x not in list(string.ascii_letters)]  # remove letters in special
	special = [x for x in special if x not in list(string.digits)]  # remove numbers in special

	# try to clean old passwords
	password_dir = './pass/'
	if os.path.exists(password_dir):
		try:
			shutil.rmtree(password_dir)
		except:
			shutil.rmtree(password_dir)
	os.makedirs(password_dir)

	alphabet = []

	if "-h" in sys.argv or "--help" in sys.argv:
		print("\nArguments list:")
		print("    -l for lower alphabet")
		print("    -u for upper alphabet")
		print("    -n for numerical")
		print("    -s for special characters")
		print("    -f save in files\n")
		print("then add two numbers for min and max size")
		print("example numerical password, length 2 to 3 : "+str(sys.argv[0])+" -n 2 3")
		
		print_header()
		exit()
	
	for arg in sys.argv:
		if arg == "-l":
			alphabet += list(string.ascii_lowercase)
		if arg == "-u":
			alphabet += list(string.ascii_uppercase)
		if arg == "-n":
			alphabet += list(string.digits)
		if arg == "-s":
			alphabet += special

	# check if there is some arguments
	if len(sys.argv) <= 1:
		print("There is no arguments... try -h or --help")
		exit()
	
	if sys.argv[-2].isdigit():
		minChars = int(sys.argv[-2])-1
	else:
		raise NameError("not minimum password size setted at the end of the command line")
	if sys.argv[-1].isdigit():
		maxChars = int(sys.argv[-1])-1
	else:
		raise NameError("not maximum password size setted at the end of the command line")

	if minChars == -1 or maxChars == -1 or maxChars < minChars:
		raise NameError("passwords size are wrong")

	word(password_dir, alphabet, '', minChars, maxChars)

	if "-v" in sys.argv:
		print("program finished")


