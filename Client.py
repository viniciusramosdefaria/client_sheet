#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from Data import *
import subprocess

import traceback

import os
import pwd


home = os.path.dirname(os.path.realpath(__file__))


def update():
	try:
		sheet_list = open(home+'/data/Lista Planilhas.txt','r')
		for row in sheet_list:
			if row[0] != "#" and row[0] != '\n':
				s = row.split(';')
				c = Data(s[0],s[1],s[2],s[3],int(s[4]),int(s[5]),int(s[6]),int(s[7]))
				c.update()
	except:
		traceback.print_exc()
		print ("\nNão foi possível ler o arquivo que contém a lista das planilhas.\n")
	finally:
		sheet_list.close()


def search(f):
	try:
		Lista = []
		busca = input("\nBusca: ").lower()
		if(busca == ""):
			busca = "."
		print(f.readline(),end='')
		print('\t '+f.readline())
		i = 0
		for line in f:
			serv = line[0:34].strip().lower()
			ipmng = line[35:59].strip().lower()
			hosp = line[60:79].strip().lower()
			ipserv = line[80:96].strip().lower()
			if(serv.find(busca) >= 0 or ipmng.find(busca) >= 0 or hosp.find(busca) >= 0 or ipserv.find(busca) > 0):
				tupla = (i,serv,ipmng,hosp,ipserv)
				Lista.append(tupla)
				print('{:<4}'.format(i),'{:<34}'.format(serv),'{:<24}'.format(ipmng),'{:<19}'.format(hosp),'{:<20}'.format(ipserv))
				i+=1
		index = input("\nMáquina(s): ")
		if(index.find("all") >= 0):
			return Lista
		hosts = index.split(' ')
		Listaf = []
		for x in hosts:
			Listaf.append(Lista[int(x)])
		return Listaf
	except:
		#traceback.print_exc()
		print("\nNão foi possível encontrar as maquinas solicitadas.")
	finally:
		f.close()


def connection(Lista):
	try:
		if(len(Lista) < 1):
			print("\nNão foi localizada nenhuma máquina em sua busca.")
			return;
		if(len(Lista) == 1):
			#subprocess.call(['ssh',user+'@'+Lista[0][2]])
			subprocess.call(['ssh',Lista[0][2]])
		else:
			s = 'cssh '
			for num in Lista:
				s += num[2] + ' '
			print(s)
			os.system(s);
	except:
		#traceback.print_exc()
		print("\nNão foi possível acessar as maquinas solicitadas.")


#Afazeres:

	# adicionar pexpect
	# adicionar TGs das máquinas na planilha
	# melhorar forma como chamar o script
	# padronizar variáveis/prints em ingles
	# verificar alternativa a xlrd (não funciona quando a planilha é salva pelo libreoffice)

##PROVISORIO


def call(name):
	print("home" + home)
	caminho = home +'/data/database_' + name.upper() + ".txt"
	print("caminho: " + caminho)
	try:
		f = open(caminho,'r')
		l = search(f)
		connection(l)
	except:
		return
	finally:
		f.close()

user = pwd.getpwuid(os.getuid())[0]

args = len(sys.argv)
if(args < 2 or args > 4):
	print("Ex: client [cmd] [username] [up] example")
elif(len(sys.argv) == 2):
	if(sys.argv[1] == "up"):
		update()
	else:
		call(sys.argv[1])
elif(len(sys.argv) == 3):
		user = sys.argv[1]
		call(sys.argv[2])
elif(len(sys.argv) == 4):
	if(sys.argv[2] == "cmd"):
		print("RUN COMMAND")
		user = sys.argv[1]
		f = open(home + '/data/database_' + sys.argv[3].upper() + ".txt" , 'r')
		l = search(f)
		com = input("\nComando: ").lower()
		co = Command(user,l,com,home + "/key/" +  user + "_rsa")
		c.execute()
