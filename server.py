# coding: utf-8 

import socket

class Server():
    def __init__(self, hote, port):
        self.hote = hote
        self.port = port
        self.connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_principale.bind((self.hote, self.port))
        self.connexion_principale.listen(5)
        print("Le serveur écoute à présent sur le port {}".format(port))
        self.connexion_avec_client, self.infos_connexion = self.connexion_principale.accept()

    def close_con(self):
        print("Fermeture de la connexion")
        self.connexion_avec_client.close()
        self.connexion_principale.close()

    def connexion(self):
        continu = True
        essaie = 0
        while essaie < 3 and continu :
            self.connexion_avec_client.send(b"WHO")
            identifiant = self.connexion_avec_client.recv(1024)
            identifiant = identifiant.decode("utf-8")
            print("Identifiant:", identifiant)
            self.connexion_avec_client.send(b"PASSWD")
            passwd = self.connexion_avec_client.recv(1024)
            passwd = passwd.decode("utf-8")
            print("Passwd:", passwd)
            done = self.read_file(identifiant, passwd)
            if done :
                continu = False
            else:
                essaie = essaie + 1
        return continu;
            
    def read_file(self, identifiant, passwd):
        fichier = open("identifiants.txt","r")
        for ligne in fichier:
            tmp = ligne.split(" ")
            print(tmp[0], tmp[1].replace("\n",""))
            print(identifiant, passwd)
            if  tmp[0] == identifiant and tmp[1].replace("\n","") == passwd:
                return True
        fichier.close()
        return False

    def listen(self):
        msg_recu = b""
        while msg_recu != b"fin":
            i=0;
            msg_recu = self.connexion_avec_client.recv(1024)
            # L'instruction ci-dessous peut lever une exception si le message
            # Réceptionné comporte des accents
            print(msg_recu.decode())
            msg = msg_recu.decode()
            if msg == "BONJ":
                res = self.connexion()
                if res :
                    self.connexion_avec_client.send(b"BYE")
                    break
                else:
                    self.connexion_avec_client.send(b"WELC")
            else:
                self.connexion_avec_client.send(b"BOBOBOBO")
            
        self.close_con()


server = Server("", 12800)
server.listen()
