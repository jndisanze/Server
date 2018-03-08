import MessageThread as message
from threading import *

class Help(object):
    '''Classe d'utilitaire permettant d'afficher le menu du routeur de maniere modulaire'''
    
    def __init__(self):
        '''Cree un Help avec un buffer'''
        self.buffer = ""
    
    def welcomeMessage(self,numRouter, numNetID):
        '''Retourne sous forme textuelle un message de bienvenue sur un routeur '''
        return "Bienvenue sur le routeur virtuel ", numRouter, " du reseau ", numNetID
    
    def putInBuffer(self,string):
        '''Enregistre dans un buffer un message destine au routeur et qui sera affiche juste avant
        que le menu ne reapparaisse'''
        self.buffer += "\n"
        self.buffer += string
        
    def readOption(self):
        '''
        Permet la lecture au clavier d'un numero d'option choisis par l'utilisateur et de le verifier
        '''
        isOptionCorrect = False
        nrOption = 0
        
        while isOptionCorrect == False:
            print self.choiceQuestion()
            numOption = raw_input()
            try:
                nrOption = int(numOption)
                
                isOptionCorrect = nrOption > 0 and nrOption < 10
            except ValueError: pass
            
        return nrOption
            
    def options(self):
        '''Retourne sous forme textuelle la liste des options possibles du routeur'''
        msgHelp = 'Aide:\n'
        msgInterval = '1 - Modifier la valeur de l\'intervalle de mise a jour des vecteurs de distance\n'
        msgWeight = '2 - Modifier le poids d\'un lien\n'
        msgChat = '3 - Envoyer un message a un routeur\n'
        msgPing = '4 - Envoyer un Ping vers une destination\n'
        msgTraceroute = '5 - Envoyer un Traceroute vers une destination\n'
        msgForwardingTable = '6 - Afficher la table de forwarding\n'
        msgDistanceVector = '7 - Afficher les vecteurs de distance recus des voisins\n'
        msgLog = '8 - Afficher le journal d\'evenements\n'
        msgQuit = '9 - Quitter le routeur\n'
        
        return msgHelp+msgInterval+msgWeight+msgChat+msgPing+msgTraceroute+msgForwardingTable+msgDistanceVector+msgLog+msgQuit

    def choiceQuestion(self):
        '''Retourne sous forme textuelle la demande de choix d'une option'''
        return 'Quel est votre choix?'
    
    def getAndClearBuffer(self):
        '''
        Permet d'obtenir le contenu du buffer et de le vider en meme temps
        '''
        buf = self.buffer
        self.buffer = ""
        
        return buf
        
    def choiceIntervalValue(self):
        '''
        Permet la lecture au clavier de la nouvelle valeur de l'intervalle de mise a jour des
        vecteurs de distance
        '''
        isCorrect = False
        intervalValue = 0
        
        while(isCorrect == False):
            intervalValueTxt = raw_input("Nouvelle valeur de l'intervalle(0-600 sec) : ")
            
            try:
                intervalValue = int(intervalValueTxt)
                isCorrect = intervalValue >= 0 and intervalValue <= 600
            except ValueError:
                print "Mauvaise valeur introduite !!!"
            
        return intervalValue
    
    def sendChatToRouter(self):
        '''
        Methode qui propose a l'utilisateur de taper le nom du destinataire et le message
        en vue de l'envoie d'un message de type CHAT.
        La methode retourne le nom du destinataire et le message
        '''
        isReceiverNameNotEmpty = False
        
        while( isReceiverNameNotEmpty == False ):
            receiverName = raw_input("Entrez le nom du destinataire : ")
            isReceiverNameNotEmpty = (self.isEmpty(receiverName) == False)
        
        messageToSend = raw_input("Entrez votre message : ")
        
        return (receiverName,messageToSend)
    
    def sendPingOrTraceRouteToReceiver(self):
        '''
        Methode qui propose a l'utilisateur de donner le nom du destinataire a joindre dans le cas
        d'un message de type PING ou TRACEROUTE
        '''
        isReceiverEmpty=False
        receiverName = ""
        
        while(isReceiverEmpty == False):
            receiverName = raw_input("Entrez le nom du destinataire : ")
            isReceiverEmpty = (self.isEmpty(receiverName) == False)
        
        return receiverName
    
    def weightListToString(self,linkList):
        '''Retourne sous forme textuelle un message demandant a l'utilisateur de choisir le lien
        dont il faut modifier le cout'''
        string = "Veuillez choisir le numero du lien a modifier le poids\n"
        cpt = 0
        
        for link in linkList:
            string += cpt," - ",link
            cpt+=1
        
        return string
    
    def distanceVectorsToString(self,distanceVectors):
        '''Retourne la liste des vecteurs de distance fournit en parametre sous forme textuelle'''
        txt = ""
        
        for distanceVector in distanceVectors:
            txt += distanceVector[0]
            txt += "     "
            txt += distanceVector[1]
            txt += "\n"
            
        return txt
    
    def loggingToString(self,logging):
        '''Retourne la liste de message de logging sous forme textuelle'''
        string = ""
        
        for log in logging:
            string += log
            string += "\n"
        
        return string
      
    def isEmpty(self,string):
        '''Verifie si une chaine est vide'''
        empty = True
        i = 0
        
        while( empty and i < len(string) ):
            empty = (string[i] == ' ')
            i+=1
        
        return empty