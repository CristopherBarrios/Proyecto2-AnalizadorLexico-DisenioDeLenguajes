######################################################
# Cristopher Jose Rodolfo Barrios Solis 
#
######################################################
# Scanner.py
######################################################

import os
from os.path import basename
import sys
sys.path.append(".")

import pickle

# Clase de implementacion_________________________________________________

class Scanner:
    """Archivo que utiliza las transiciones del AFD generado
    a partir de una gramatica cualquiera escrita en COCO/R,
    para reconocer los tokens un archivo de prueba cualquiera.
    """
    def __init__(self,testFile = 'test_file.txt'):
        self.scanner = pickle.load(open('Cocor/archivosScanner/scanner'+testFile[:-4]+'.scann'.lower(),'rb'))
        #self.acceptingStatesDict = pickle.load(open('cocor/accADict','rb'))
        self.resultAFDArray = self.scanner.resultAFDArray
        self.acceptingStatesIdentifiers = self.scanner.acceptingStatesIdentifiers

        self.test_patterns = []
        self.testFile = 'Tests\\'+testFile
        self.line_to_read = ''

    def read_test_file(self):
        """Funcion para leer el archivo de prueba 
            y almacenar sus contenidos.
        """
        here = os.path.dirname(os.path.abspath(__file__))
        file_ = self.testFile
        filepath = os.path.join(here, file_)
        with open(filepath, 'r') as fp:
            line = fp.readline()
            while line:
                print("\nFile contents: {}".format(line.strip()))
                print('')
                self.line_to_read = line
                line = fp.readline()

    def getStateId(self, states_list):
        """Regresara el identificador del estado

        Args:
            states_list (list): lista de estados

        Returns:
            int: el estado
        """
        for value in self.resultAFDArray:
            if(value[1] == states_list):
                return value[0]

    def move(self,states_set,character):
        """Representacion de la funcion move(A,a) 
        para la simulacion del AFD formado a partir 
        de los tokens definidos en un archivo atg.

        - Args:
            - states_set (list): arreglo de estados
            - c_state (set): el caracter o estado en cuestion

        - Returns:
            - list: nuevo array de estados si hay transicion
        """
        new_states_array = []
        for state in states_set:
            # trans sera nuestra transicion y debemos 
            # verificar si el caracter en cuestion esta
            # en ese set con uno o varios valores
            for trans in self.resultAFDArray:
                inSet = (ord(character)) in trans[2]
                if( inSet and len(trans[3]) > 0 and state == trans[0]):
                    nextState = self.getStateId(trans[3])
                    if(nextState not in new_states_array):
                        new_states_array.append(nextState)
        return new_states_array

    def getTokenExplicitIdentifierV2(self, tokenArray):
        """Funcion que retornara el identificador explicito 
        del token en cuestion. Retornara el lado izquierdo
        de la expresion, por asi decirlo. 
        Ej. [number = digit(digit)*] --> <number>

        Args:
            estados (list): lista de estados

        Returns:
            set: el set con los posibles caracteres pertenecientes
            a ese token particular
        """
        statesSetList = []
        tokenExplicitIdentifier = ""
        finalStates = self.scanner.getFinalStateId()
        for value in self.resultAFDArray:
            for finalState in finalStates:
                if(str(finalState) in value[1]):
                    for current_token in tokenArray:
                        if(current_token == value[0]):
                            if(value[1] not in statesSetList):
                                statesSetList.append(value[1])

        acceptingIdentifier = {}
        acceptingIdentifierNumbers = []
        # En esta seccion se comprobara 
        # cual es el identificador explicito
        # del token
        for statesSet in statesSetList:
            for posibleState in statesSet:
                for keyy, value in self.acceptingStatesIdentifiers.items():
                    if(int(posibleState) == keyy):
                        acceptingIdentifier[keyy] = value
                        acceptingIdentifierNumbers.append(keyy)

        # En caso que la lista de identificadores 
        # tuviera varios elementos
        if(len(acceptingIdentifier) > 1):
            minValueIdent = min(acceptingIdentifierNumbers)
            for keyy, value in acceptingIdentifier.items():
                if(minValueIdent == keyy):
                    tokenExplicitIdentifier = value
        else:
            for keyy, value in acceptingIdentifier.items():
                tokenExplicitIdentifier = value

        return tokenExplicitIdentifier

    def getAcceptingStatesAFD(self):
        """Obtenemos estados de aceptacion 
        del AFD

        Returns:
            list: los estados de aceptacion del afd
        """
        statesSetList = []
        for value in self.resultAFDArray:
            finalstates = self.scanner.getFinalStateId()
            for fstate in finalstates:
                if(str(fstate) in value[1]):
                    statesSetList.append(value[0])

        return statesSetList

    def simulationTest(self):
        """Simulacion del AFD de resultado
        """
        s = [0]
        for x in self.line_to_read:
            s = self.move(s, x)
        lastId = self.getAcceptingStatesAFD()

        if(len(s) > 0):
            if(s[0] in lastId):
                print('-------------------------------------------------')
                print('La cadena '+self.line_to_read+' fue aceptada por el AFD.')
                print('-------------------------------------------------')
            else:
                print('-------------------------------------------------')
                print('La cadena '+self.line_to_read+' NO fue aceptada por el AFD.')
                print('-------------------------------------------------')
        else:
            print('-------------------------------------------------')
            print('La cadena '+self.line_to_read+' NO fue aceptada por el AFD.')
            print('-------------------------------------------------')   

    def simulation(self):
        """Funcion para simular una linea de entrada
        desde un archivo de prueba.

        - Returns:
            - int: 0
        """

        #contador local para llevar la posicion del caracter leido
        counter = 0

        #la dinamica aqui es leer un token y leer al mismo tiempo el siguiente
        # para saber si existira transicion cuando pasemos al siguiente
        # caracter leido, de lo contrario no sabriamos como continuar 
        # en cierto punto
        S = [0]
        S_next = [0]

        #construccion de la cadena leida
        token_construction = ""
        #acumulador de estados
        string_array = []
        #estado de aceptacion
        accepting_state = []

        # En este ciclo encapsularemos cada uno de 
        # los caracteres de la linea de entrada
        for character in self.line_to_read:
            string_array.append(character)

        #insertamos un espacio vacio al inicio
        string_array.append(" ")
        
        #Este caso se da cuando hay un solo token en el archivo
        while len(string_array) > 0:
            if(counter == len(self.line_to_read)-1):
                characterToEvaluate = self.line_to_read[counter]
                token_construction += characterToEvaluate
                S = self.move(S,characterToEvaluate)
                token = self.getTokenExplicitIdentifierV2(S)

                if(len(token) == 0):
                    print('Invalid token: ', token_construction)
                    break
                else:
                    print('token: '+ token_construction + ' has type: '+str(token))
                    break
            characterToEvaluate = self.line_to_read[counter]
            nextCharacterToEvaluate = self.line_to_read[counter+1]
            token_construction += characterToEvaluate
            S = self.move(S,characterToEvaluate)
            S_next = self.move(S,nextCharacterToEvaluate)

            # Este caso se da cuando a travez del siguiente token ya no hay 
            # transicion hacia otro estado
            if(len(S) > 0 and len(S_next) == 0):  
                token = self.getTokenExplicitIdentifierV2(S)

                if(len(token) == 0):
                    print('Invalid token: ', token_construction)
                    S = [0]
                    S_next = [0]
                    token_construction = ""
                    counter -= 1
                else:
                    print('token: '+ token_construction + ' has type: '+str(token))
                    S = [0]
                    S_next = [0]
                    token_construction = ""
            elif(len(S) == 0):
                print('Invalid token: ', token_construction)
                S = [0]
                S_next = [0]
                token_construction = ""

            counter += 1
            character_popping = string_array.pop()

        print('')