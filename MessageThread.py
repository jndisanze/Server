import threading
import socket
from RequestTask import *

def createMessage(sourceAdress, destAdress, ttl, type, reason):
    '''
    Cree un message respectant le format de message standard convenu a partir des parametres fournis
    '''
    spaceCharacter = " "
    endOfLine = "\r\n"
        
    message = sourceAdress
    message += spaceCharacter
    message += destAdress
    message += spaceCharacter
    message += str(ttl)
    message += spaceCharacter
    message += type
    message += spaceCharacter
    message += str(len(reason))
    message += endOfLine
    message += reason
    message += endOfLine
        
    return message
    
class MessageThread(threading.Thread):
    '''
    Thread permettant de decortiquer et analyser un message arrivant sur une interface donnee
    '''
    def __init__(self, router, message, nameOfRouter, inputInterface, forwardingTable, help):
        '''
        Construit un MessageThread
        router --> instance du routeur
        message --> message a decortiquer
        nameOfRouter --> Nom du routeur
        inputInterface --> Adresse de l'interface(ip+port) ayant recu le message
        forwardingTable --> Table de forwarding
        help --> instance d'un Help
        '''
        threading.Thread.__init__(self)
        self.__msg = message
        self.__nameOfRouter = nameOfRouter
        self.__inputInterface = inputInterface
        self.__forwardingTable = forwardingTable
        self.__help = help
        self.__router = router
        
    def run(self):
        '''Decortique et analyse le message pour un eventuel traitement'''
        message = self.__msg
        argList, message = self.getHeader(self, message)
        contentLength = int(argList[4])
        contentOfMsg = self.getContentOfMessage(self, message, contentLength)
        
        if self.isFormatCorrect(self, argList):
            messageToSend = ""
            sourceAdress = argList[0]
            destAdress = argList[1]
            ttl = int(argList[2])
            
            ttl -= 1
            type = argList[3]
            
            if ttl == 0:
                if type != "ERREUR" :
                    self.__router.addLogging(sourceAdress + " "+ destAdress + " " + type + " TTL expired" )
                    messageToSend = self.createMessage(self.nameOfRouter, sourceAdress, 255, "ERREUR", "1 TTL EXPIRED")
            else:
                if destAdress == "UNKNOWN" or self.nameOfRouter == destAdress:
                    if type == "CHAT":
                        help.putInBuffer(contentOfMsg)
                    else:
                        if type == "ERREUR":
                            if contentOfMsg[0] == "1" or contentOfMsg[0] == "2":
                                RequestTask.addResponse(sourceAdress + " " + contentOfMsg)
                            else:
                                help.putInBuffer(contentOfMsg)
                            
                            self.__router.addLogging(sourceAdress + " "+ destAdress +" "+ type +" "+ contentOfMsg )
                        else:
                            if type == "PONG":
                                RequestTask.addResponse(sourceAdress + " " + contentOfMsg)
                                    
                            if type == "PING":
                                messageToSend = self.createMessage(self.nameOfRouter, sourceAdress, 255, "PONG", contentOfMsg)
                            else:
                                if type == "VECTEUR-DISTANCE":
                                    distanceVectorList = self.distanceVectorInfo(self, contentLength, contentOfMsg)
                                    self.__saveDistanceVectorList(distanceVectorList)
                                    self.forwardingTable.update(distanceVectorList, self.inputInterface)
                                else:
                                    messageToSend = self.createMessage(self.nameOfRouter, sourceAdress, 255, "ERREUR", "4 TYPE NOT RECOGNIZED")
                else:
                    if self.forwardingTable.exist(destAdress):
                        messageToSend = self.createMessage(sourceAdress, destAdress, ttl, type, contentOfMsg)
                    else:
                        self.__router.addLogging(sourceAdress+" "+destAdress+" "+type+ " "+"DESTINATION UNKNOWN")
                        if type != "ERREUR":
                            messageToSend = self.createMessage(self.nameOfRouter, sourceAdress, 255, "ERREUR", "2 DESTINATION UNKWOWN")
        else:
            self.__router.addLogging(sourceAdress+ " " + destAdress + " " + type + " " + " MESSAGE NOT CORRECTLY FORMATTED")
            messageToSend = self.createMessage(self.nameOfRouter, sourceAdress, 255, "ERROR", "3 MESSAGE NOT CORRECTLY FORMATTED")
        
        if messageToSend != "":
            #recuperation de l'adresse de destination
            partition = messageToSend.partition(" ")
            stringAfterSpace = partition[2]
            destAdress = stringAfterSpace[0:stringAfterSpace.find(" ")]
            self.__router.sendMessage(destAdress, messageToSend)
    
    def __saveDistanceVectorList(self, distanceVectorList):
        '''Ajout des vecteurs de distance dans la liste de vecteurs de distance du routeur'''
        for distanceVector in distanceVectorList:
            self.__router.addDistanceVector(distanceVector)
        
    def __distanceVectorInfo(self, contentLength, contentOfMessage):
        '''decortique le contenu d'un message de vecteur de distance et retourne dans une liste 
        les differents vecteurs de distance'''
        distanceVectorList = []
        
        while contentLength != 0:
            #recuperation de l'adresse de destination
            partition = contentOfMessage.partition(" ")
            destAdress = partition[0]
            contentOfMessage = partition[2]
            
            #recuperation du cout vers cette adresse de destination
            partition = contentOfMessage.partition("\r")
            cost = partition[0]
            contentOfMessage = partition[2]
            
            """Les deux prochaines lignes permettent de mettre une info de vecteur de distance
            dans une liste"""
            tab = [ destAdress, int(cost) ]
            distanceVectorList.append([tab])
            
            contentLength -= (len(destAdress) + len(cost) + 3)
        
        return distanceVectorList
    
    
    def __isFormatCorrect(self, argList):
        '''Regarde si les arguments dans le header du message ont le bon format'''
        return not(argList[0].isDigit()) and not(argList[1].isDigit()) and argList[2].isDigit() and not(argList[3].isDigit()) and argList[4].isDigit()
    
    def __getContentOfMessage(self, message, contentLength):
        '''Retourne le contenu du message sur base de sa taille'''
        msg = ""
        i = 0
        
        while contentLength != 0:
            msg += message[i]
            contentLength -= 1
            i += 1
            
        return msg
    
    def __getHeader(self, message):
        '''Permet d'obtenir la liste des arguments se trouvant dans le header du message ainsi que
        le reste du message a analyser'''
        argList = ["", "", "", "", ""]
        
        #recuperation de l'adresse source-destination, TTL + type
        for i in range(4) :
            partition = message.partition(" ")
            argList[i] = partition[0]
            message = partition[2]
    
        #recuperation de la longueur du message
        partition = message.partition("\r")
        argList[4] = partition[0]
        message = partition[2]
        
        return argList, message
        
