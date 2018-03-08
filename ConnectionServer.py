import threading
import thread
import tableForwarding
from threading import Thread,Timer

class ConnectionServer(threading.Thread):
    '''Represente une interface d'un routeur'''
    def __init__(self,connection):
        threading.Thread.__init__(self)
        self.config=connection
        self.s=self.config[0]
        self.adresses=self.config[1]
        self.fw=self.config[3]
        self.timer = Timer(600,self.checkFailureOnLink)
        self.Terminated = False
    
    def checkFailureOnLink(self):
        '''Verifie si l'interface a recu un message dans les dix minutes.Si ce n'est pas le cas,
        l'interface arrete d'ecouter'''
        #si on a pas recu un message dans les 10 minutes sur cette interface, arreter la thread
        pass
    
    def getInputAdress(self):
        '''Permet d'obtenir l'adresse et le port d'ecoute'''
        return self.adresses[0],self.adresses[1]
    
    def getOutputAdress(self):
        '''Permet d'obtenir l'adresse et le port joignable directement a partir de l'interface'''
        return self.adresses[2],self.adresses[3]
    
    def sendMessage(self,message):
        '''Permet l'envoi de message'''
        self.s.send(message)
        
    def run(self):
        '''Methode qui permet d'ecouter les messages arrivant sur l'interface'''
        #creation de la table de forwarding
        self.fw.add(str(self.adresses[2]+self.adresses[3]),(self.adresses[0],self.adresses[1]),self.adresses[4])
        
        """while self.Terminated == False and 'localhost' != self.adresses[0]:
            data,addr = self.s.recvfrom(1024)
            #on test si l'origine de l'addresse 
                #mise a jour de vecteur distance 
            if self.fw.exist() != None:
                #traitement du massage
                #cas mise a jour de table vecteur distance
                vectRecu
                # on test si l'adresse a metre a jour existe
                if self.fw.exist('localhost') != None:
                    #on regarde si l'adresse a mettre a jour n'est pas celle du routeur
                    #if 'localhost' != adresse[0]:
                        p=self.fw.exist('localhost')
                        if vectRecu[2]+1<p[2]:
                            self.fw.add('localhost',('localhost',port),vectRecu[2]+1)
                        elif vectRecu[2]+1>p[2]:
                            if 'localhost'==p[1][0]:
                                self.fw.add('localhost',p,vectRecu[2]+1)
                    # si po vect-dist si c'est un message de trafere verifier si il est dans liaion"""            
        self.s.close()
        
    def stop(self):
        '''Permet d'arreter l'ecoute de message de l'interface'''
        self.Terminated = True