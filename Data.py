#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import xlrd
import re

import os
import traceback


class Data:

	def __init__(self,name,url,workbook,sheet,column_name_serv,column_name_hosp,column_ip_mng,column_ip_svc):
		self.name = name
		self.url = url
		self.workbook = workbook
		self.sheet = sheet
		self.column_name_serv = column_name_serv
		self.column_name_hosp = column_name_hosp
		self.column_ip_mng = column_ip_mng
		self.column_ip_svc = column_ip_svc
		self.home = os.path.dirname(os.path.realpath(__file__))

	#Retorna uma lista de todos IP's contidos em uma string.
	@staticmethod
	def split_ip(s):
		ipPattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
		return re.findall(ipPattern,s)

	#Realiza Download da planilha.
	def update(self):
		try:
			print ("Update " + self.name)
			subprocess.call(["wget","-q",self.url,"-O",self.home + "/data/" + self.workbook])  # parametro -q para não mostrar progresso do download...
			print ("Download " + self.name + " with wget: Success")
			self.create_db()
			print (self.name + " updated.\n")
		except:
			#traceback.print_exc()
	        	print ("Update Failed: " + self.name)

	#Atraves da planilha, gera um arquivo organizado com os dados da mesma.
	def create_db(self):
		try:
			self.workbook = self.home + "/data/" + self.workbook
			planilha = xlrd.open_workbook(self.workbook)
			tabela = planilha.sheet_by_name(self.sheet)
			name_database = 'database_' + self.name + '.txt'
			arquivo = open(self.home + '/data/' + name_database,'w')
			arquivo.write(self.name + '\n')
			arquivo.write('{:<40}'.format("Maquina"))
			arquivo.write('{:<25}'.format("IP - GERENCIA"))
			arquivo.write('{:<20}'.format("HOSPEDEIRA"))
			arquivo.write('{:<25}'.format("IP - SERVICO / VIRTUAL"))
			arquivo.write('\n')

			num_linhas = tabela.nrows;
			i = 0

			while i < num_linhas:
				name_serv  = str(tabela.cell_value(i,self.column_name_serv)).rstrip()
				ip_planeta = str(tabela.cell_value(i,self.column_ip_mng)).rstrip()
				ip_servico = str(tabela.cell_value(i,self.column_ip_svc)).rstrip()
				hospedeira = str(tabela.cell_value(i,self.column_name_hosp)).rstrip()

				lista = Data.split_ip(ip_planeta)
				if(len(lista) > 0):
					arquivo.write('{:<35}'.format(name_serv)[:35])
					for x in lista:
							arquivo.write('{:<25}'.format(x)[:25])
							break #cutting just the first ip for a while
					arquivo.write('{:<20}'.format(hospedeira)[:20])
					arquivo.write('{:<25}'.format(ip_servico)[:25])
					arquivo.write('\n')
				i += 1

		except:
			#traceback.print_exc()
			print ("Can't update database with this sheet: " + self.name + ".\n")
		finally:
			arquivo.close()
