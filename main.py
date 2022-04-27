######################################################
# Cristopher Jose Rodolfo Barrios Solis 
#
######################################################
# main.py
######################################################

# imports _________________________
import os
import sys
sys.path.append(".")
from direct.DirectAFDWords import DirectAFDWords
from Cocor.Cocor import Cocor

from Cocor.Scanner import Scanner
from functions.functions import functions
import collections
import pickle

#funciones______________________
def bienvenido():
    print("")
    print("========================================================")
    print("---------------------- Bienvenido ----------------------")
    print("========================================================")
    print("")

def bienvenidoMenuPrincipal():
    print("-------------------- Menu principal ---------------------")
    print("")

def bienvenidoCocor():
    print("\n--------------------Coco/R tests----------------------")
    print("")

def bienvenidoScanner():
    print("\n----------------------SCANNER-------------------------")
    print("")

def menuPrincipal():
    print("Selecionar opcion: ")
    print("1. Coco/R tests.")
    print("2. SCANNER")
    print("3. Salir del programa")

def menuCocor():
    print("Selecionar opcion: ")
    print("1. Leer archivo.")
    print("2. Metodo de conversion directa y generar escaner ")
    print("3. Salir del programa")

def menuScanner():
    print("Seleccione una opcion.")
    print("\t1. Leer archivo de prueba")
    print("\t2. Leer un solo token en archivo (pruebas aceptacion)")
    print("\t3. Salir")


####COCOR_________________________________________________________________________
def mainCocor():
    coco_obj = Cocor()
    postfixRegex = []
    def_file = ''

    while True:

        bienvenidoCocor()

        menuCocor()
        option = input('ingrese una opcion: ')
        print("")

           
        if(option == '1'): #logica para leer archivo
            def_file = input('Ingrese el nombre del archivo con las definiciones (Ej. Aritmetica.cfg): ')
            print("")
        
            coco_obj.read_def_cfg(def_file) 
            coco_obj.charactersSubstitution() 
            coco_obj.cocorToP1Convention()

            coco_obj.tokensPreparationPostfix()

            coco_obj.orBetweenExpresions()
            postfixRegex = coco_obj.expresionSubstitutions()
            coco_obj.tokensSubstitutions()
            tks = coco_obj.getTokens()
            chars = coco_obj.getCharacters()
            kws = coco_obj.getKeywods()


        elif(option == '2'):
            if(postfixRegex == ['ERROR_POSTFIX_)']):
                print('\n ")" faltante en la expresion regular ingresdigit. Vuelva a intentar. \n')
            else:
                print(' - postfix     = '+ str(postfixRegex))
                tokens = functions.getRegExUniqueTokensV2(postfixRegex)
                print(' - alfabeto (tokens): '+str(tokens))

                chain = '12356'

                objdirect = DirectAFDWords(tokens,chain,postfixRegex,chars,tks,kws)
                AFD = objdirect.generateDirectAFD()

                # Its important to use binary mode
                store_transitions = open('Cocor/archivosScanner/scanner'+def_file[:-4]+'.scann'.lower(), 'ab')
                # source, destination
                pickle.dump(objdirect, store_transitions)                     
                store_transitions.close()

                #logica para convertir y generar escaner
        elif(option == '3'):
            print('\nAdios! ')
            break
        else:
            input('No se a escogido opcion valida, presiona Enter')


####SCANNER_________________________________________________________________________
def mainScanner():
    while True:
        bienvenidoScanner()
        menuScanner()
        option = input('Ingrese una opcion: ')
        print("")

        if(option == '1'):
            file_name = str(input("Ingrese el nombre del archivo de prueba (Ej. aritmetica.txt): "))
            print("")
            obj = Scanner(file_name)
            obj.read_test_file()
            obj.simulation()

        elif(option == '2'):
            file_name = str(input("Ingrese el nombre del archivo de prueba (Ej. aritmetica.txt): "))
            print("")
            obj = Scanner(file_name)
            obj.read_test_file()
            obj.simulationTest()

        elif(option == '3'):
            print('\nAdios! ')
            break
        else:
            input('No se ha elejido ninguna opcion en el menu. Intentalo de nuevo! Enter -->')

def main():
    while True:
        bienvenidoMenuPrincipal()
        menuPrincipal()
        option = input('ingrese una opcion: ')
        print("")

        if(option == '1'):
            mainCocor()
        elif(option == '2'):
            mainScanner()
        elif(option == '3'):
            print('\nAdios! ')
            break
        else:
            input('No se ha elejido ninguna opcion en el menu. Intentalo de nuevo! Enter -->')

#ejecuciones____________________
bienvenido()
functions = functions()
if __name__ == "__main__":
    main()
