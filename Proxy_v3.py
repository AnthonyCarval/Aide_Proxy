''' Test de modification avec Git

BlaBlaBlaBlaBlaBlaBlaBla
BlaBlaBlaBlaBlaBlaBlaBla
BlaBlaBlaBlaBlaBlaBlaBla
BlaBlaBlaBlaBlaBlaBlaBla
BlaBlaBlaBlaBlaBlaBlaBla
BlaBlaBlaBlaBlaBlaBlaBla
'''



# -*- coding: utf8 -*-
import os
import random
import time
import json
import sys

os.system("clear")





recherche= ("www","https","http","api","wiki",".fr",".com")
liste_time=[]

log='log_V3.json'
log_squid='/var/log/squid/access.log'
conf_squid='/etc/squid/squid.conf'



#Vérification que le choix entré est bien dans les choix possibles
def verif_choix(nbs,choix):

	liste_choix=[]
	
	for choise in range(nbs):

		liste_choix.append(str(choise))
		
	if choix  in (liste_choix) : 
			
		return True
			
	else :
		print ( "\n\nChoix hors de la liste \n ")
		return False
		
 



# Compatage des visites en analysant le fichier
# de log squid, puis enregistrement des résultats
# dans un fichier au format JSON



def loop_verif_log(dico):

	
	file = open(log_squid, "r")
	lines = file.readlines()

	for line in lines: 
		
		
		ma_requete=decoup_requete(line)

		
		
		if recherche_string(recherche,ma_requete["url"]) == True :
				
					
			if ma_requete["method"] != "POST":
					
				
				if "/" in ma_requete["url"]:
					
					request=ma_requete["url"].split("/")
					url=request[2]
					
				else:
					
					preextension = ma_requete["url"].split(".")
					extension= "." + preextension[-1][:-4]
					request=ma_requete["url"].split(extension)
					url=request[-2]+extension
									
				if url in dico.keys() : 
						
					time_enregistre = dico[url]["timestamp"]
						
					if ma_requete["timestamp"] not in time_enregistre: 
									
						nombre =len (time_enregistre)
						time_enregistre.append(str(ma_requete["timestamp"]))
						dico[url] = {"visit":nombre,"timestamp":time_enregistre}


					
				else: 
					print("Nouveau site visité")
						
					liste_time=ma_requete["timestamp"]
					dico[url] =	{"visit":1,"timestamp":[str(ma_requete["timestamp"])]}
						
	file.close()	
	save_log(dico)

	


# recherche de plusieurs string différents  dans des datas		
def recherche_string(liste_a_rechercher,datas):

	
	
	for item in liste_a_rechercher:	
		
			if str(item) in datas:
				return True
				
					
		
# mise en forme de chaque ligne de requete
def decoup_requete(line):

	ma_requete={"timestamp":"",
				"total_time":"",
				"ip_source":"",
				"action":"",
				"size_requete":"",
				"method":"",
				"url":"",
				"ident":"",
				"hier":"",
				"content":""}
			
	timestamp=""
	total_time=""
	chaine=""

	for x in  range(14):
		timestamp += str(line[x])
	for x in  range(14,22):
		total_time += str(line[x])	

		

	chaine=line[21:]
	chaine2=chaine.split(" ")
	ma_requete["timestamp"]=str(timestamp)
	ma_requete["total_time"]=str(total_time)
	ma_requete["ip_source"]=str(chaine2[1])
	ma_requete["action"]=str(chaine2[2])
	ma_requete["size_requete"]=str(chaine2[3])
	ma_requete["method"]=str(chaine2[4])
	ma_requete["url"]=str(chaine2[5])
	ma_requete["ident"]=str(chaine2[6])
	ma_requete["hier"]=str(chaine2[7])
	ma_requete["content"]=str(chaine2[8]) 
	time_requete_line = ma_requete["timestamp"]
	
	return ma_requete


# lecture d'un fichier
# puis return son contenu
def lecture_fichier(file):
	with open(file, "r") as fichier:
		contenu = fichier.readlines()
		fichier.close()
		return contenu	

	

def write_file(file, data):
	fichier= open(file,"w")
	fichier.writelines(data)	
	fichier.close()	





# mise a jour et affichage des données 
# dans l'ordre décroissant des visites 
def affiche_data(dict):
	loop_verif_log(file)
	tri = input('\n\nEntrez le seuil de visite : \n\n')
	check=verif_choix(999999,tri)
	if check == True :



		rangement=[]
		tuples=()
		matrice="{\n}"
		
		if matrice in dict.items():
			print ( "Aucune visite pour le moment !!! ")

		else :	
			for cle, valeur in dict.items():	
				if valeur["visit"]>int(tri): 
						
						
					tuples=int(valeur["visit"]), cle
					rangement.append(tuples)
						
				
			for visite in sorted(rangement, reverse=True):

				print ( "visite : " , visite[0] , " site : " ,visite[1] )
		
				
# Vérification de la présence du fichier de log
# S'il n'existre pas il est créé avec un exemple
# de visite
def verif_log(file):
	
	print ("Vérification présence du fichier ", file)

	isExist = os.path.exists(file)
	
	print("le fichier est : ", isExist)

	if isExist == False:
		dico={}
		ma_requete={"timestamp":"0000000000",
					"total_time":"",
					"ip_source":"",
					"action":"POST",
					"size_requete":"",
					"method":"",
					"url":"www.google.fr",
					"ident":"",
					"hier":"",
					"content":""}

		dico[ma_requete["url"]] =	{"visit":1,"timestamp":[str(ma_requete["timestamp"])]}	
		save_log(dico)
	
  
	
#chargement des données Json
def load_data(file):
	
	#try :
		with open(file) as json_data:
			data_dict = json.load(json_data)
		
		return data_dict
	#except IOError: 
	
		
# enregistrement des données en Json 
def save_log(data):
	with open(log, 'w') as fp:	json.dump(data,fp, sort_keys=True, indent=2)


# Affichage des blocages en cours
def affiche_blocage():
	
	print ("\n\nListe des blocages :\n")
	liste= liste_blocage("dstdomain")

	for blocage in liste:
		print (blocage)


# création liste blocage
# on recherche la valeur var
# dans le fichier de conf de squid
def liste_blocage(var):
	
	
	
	fichier = lecture_fichier(conf_squid)	
	liste_blocage=[]
	
	for line in fichier :
		
		if var in line : 
			 
			block= (line.split())
			if var=="dstdomain":
				liste_blocage.append(block[3])
			else :
				liste_blocage.append(line )	
			
		
	
	return liste_blocage		
		

# On ajoute une regle dans le fichier 
# de conf Squid
# Tout en vérifiant qu'elle n'existe
# pas deja
# Soit une regle pré listé
# Soit une regle que l on saisie
def ajout_regle():
	
	fichier=load_data(log)
	liste=[]
	a_bloquer=""
	
	
	
	print (" \n\n0 Ajout manuel ?\n1 Ajout prédéfini ?\n2 Retour")

	choix_ajout=int(input ("\nchoix ?"))
	check=verif_choix(3,str(choix_ajout))

	if check ==True:

		if choix_ajout == 2 :
			menu()

		if choix_ajout == 0 :

			
			site_a_bloquer=input("Entrez le domaine à bloquer par exemple google.fr : \n ")
			
			bloquer=site_a_bloquer.split(".")
			
			
		
		if choix_ajout ==1:

			for site in fichier : 
				liste.append(site)
				print ( liste.index(site) , site)

			print ( len(liste) , "retour")
			
			choix = input("choix ?")
		
			check = verif_choix(len(liste)+1,choix)
			if check == True :


				choise =int(choix)
			
				if choise == len(liste) : menu()
			
			bloquer=liste[choise].split(".")
	

		a_bloquer="."+bloquer[len(bloquer)-2] +"."+  bloquer[len(bloquer)-1] 
		
		acl = "acl " + bloquer[len(bloquer)-2] +" dstdomain " + a_bloquer 
		http_access = "http_access deny " + bloquer[len(bloquer)-2]
		

	
		contenu=lecture_fichier(conf_squid)
				
	
	# vérification si la regle est deja presente
		for line in contenu:
				
			if acl  in line : 
				block = True
				break
			else : 
				block = False
							

		if block==False:
				
			for line in contenu:
				
				if "#debut ACL" in line: 
					
					contenu.insert(contenu.index(line)+1,acl+"\n")
					break
				
			for line in contenu:	
					
				if "#debut blocage" in line: 
					
					contenu.insert(contenu.index(line)+1,http_access+"\n")
					break
		
	
		write_file(conf_squid, contenu)
		


# Affichage et choix de suppression
# des regles déja actives

def supprime_regle():
	
	print ("\n\nsuppression de regles\n\n" )	
	
	regle=liste_blocage("dstdomain")
	liste_http_access=liste_blocage("http_access")
	
	for liste in regle:
		print (regle.index(liste), liste)
	
	print (len(regle),"Retour")
	choix = input("\nchoix ?")
	
	check = verif_choix(len(regle)+1,choix)
	
	if int(choix)== len(regle) : menu()

	if check == True :
		
		acl_a_supprimer=regle[int(choix)][1:-4]
	
	
		contenu=lecture_fichier(conf_squid)
		
	
		for line in contenu:
		
		
			if acl_a_supprimer in line:
				
				
				del contenu[contenu.index(line)]	
				

		write_file(conf_squid, contenu)
		
# On quitte le programme
def quitte():


	print ("\n\nMerci et au revoir  \n")
	print ("************************************************************")
	sys.exit()

		

# on relance squid
def reload_squid():
	print ("\n\nSquid en attente de restart ")
	os.system("sudo systemctl restart squid")
	print("\n\nSquid relancé ! ! !")



# Création du menu de l'utilitaire
def menu():
	
	os.system("clear")
	print ("************************************************************")
	print("   SCRIPT D'AIDE A LA GESTION DU PROXY SQUID ")
	print("\n\n    Program By Anthony Carval\n\n")
	print ("Faites votre choix  : ")
	print ("\n")
	print ("0 : Afficher les blocages en cours ")
	print ("1 : Afficher le top des visites")
	print ("2 : Ajouter un nouveau blocage ")
	print ("3 : Supprimer un blocage ")
	print ("4 : relancer Squid" )
	print ("5 : Quitter" )
	choix= input("\n\nChoix ?   ")
	check = verif_choix(6,choix)
	if check == True :
		if choix== "0" : affiche_blocage()
		if choix== "1" : affiche_data(file)
		if choix== "2" : ajout_regle()
		if choix== "3" : supprime_regle()
		if choix== "4" : reload_squid()
		if choix== "5" : quitte()
		print ("\n\nTapez entrée pour continuer" )
		
	input()
	menu()


verif_log(log)
file = load_data(log)
loop_verif_log(file)

menu()
