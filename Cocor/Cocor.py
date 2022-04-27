######################################################
# Cristopher Jose Rodolfo Barrios Solis 
#
######################################################
# Cocor.py
######################################################

#imports
import os
import sys
sys.path.append(".")
from os.path import basename

from functions.functions import functions
from infix_postfix_related.InfixRegexToPostfixWords import InfixRegexToPostfixWords

#Clase de implementacion______________________________________________
class Cocor:
    """
        Clase con definiciones varias de COCO/R
        """
             #Constructor de las variables
    def __init__(self):
        self.asciiTable = set([chr(char) for char in range(0,255)])

        self.charactersInFile = {}
        self.charactersInFileSubs2 = {}

        self.keyWordsInFile = {}

        self.tokensInFile = {}
        self.tokensConvertionInFile = {}
        self.tokensReadyForPosFix = {}
        self.tokensPosFixInFile = {}
        self.tokensSubstitutionExp = {}
        self.tokensSubstitution = {}

        self.finalExpression = {}

        self.test_patterns = []

        self.functions = functions()
        self.objToPostfix = InfixRegexToPostfixWords()

# gets ------------------

    def getCharacters(self):
        return self.charactersInFileSubs2

    def getTokens(self):
        return self.tokensSubstitution

    def getKeywods(self):
        return self.keyWordsInFile

# ZONA PARA LA LECTURA DEL ARCHIVO-----------------------------------------------------------------------        
    def read_def_cfg(self,file='def_file.cfg'):
        here = os.path.dirname(os.path.abspath(__file__))
        file_ = file
        filepath = os.path.join(here+'\\archivos\\', file_) 
        header =''

        with open(filepath, 'r')as fp:
            line = fp.readline()
            cnt = 1
            while line:
                line = line.rstrip()
                line.rstrip()
                if not(line.startswith('(.')) and len(line) > 0:
                    if(line.startswith('CHARACTERS')):
                        header = 'CHARACTERS'
                    elif(line.startswith('KEYWORDS')):
                        header = 'KEYWORDS'
                    elif(line.startswith('TOKENS')):
                        header = 'TOKENS'
                    
                    if('=' in line):
                        arr_ = line.split('=')
                        arr_[0] = arr_[0].replace(' ','')
                        arr_[1] = arr_[1][:-1]
                        if(header == 'CHARACTERS'):
                            self.charactersInFile[arr_[0]] = arr_[1]
                        elif(header == 'KEYWORDS'):
                            self.keyWordsInFile[arr_[0]] = arr_[1]
                        elif(header == 'TOKENS'):
                            self.tokensInFile[arr_[0]] = arr_[1]

                #print("Line {}: {}".format(cnt, line.strip()))
                #imprime cada linea
                line = fp.readline()
                cnt += 1

# ZONA DE TRATAMIENTO DE CARACTERES -----------------------------------------------------------------------
#----------------------------------------------------------------------

    def setOperations(self,i,char_def,set1):
        chr_result_operations = [set1]
        while i < len(char_def):
            if(char_def[i] == '+'):
                set2 = char_def[i+1]
                set1_ = chr_result_operations.pop()
                snum = ''
                if('chr(' in set2.lower()):
                    for e in set2:
                        if(e.isdigit()):
                            snum += e
                    num = int(snum)
                    set2 = set(chr(num))
                    if(isinstance(set1_, str)):
                        set1_ = set(set1_)
                    if(isinstance(set2, str)):
                        set2 = set(set2)
                    if(isinstance(set1_, list)):
                        set1_ = set1_[0]
                    if(isinstance(set2, list)):
                        set2 = set2[0]
                    chr_result_operations.append(set1_.union(set2))
                else:
                    if(isinstance(set1_, str)):
                        set1_ = set(set1_)
                    if(isinstance(set2, str)):
                        set2 = set(set2)
                    if(isinstance(set1_, list)):
                        set1_ = set1_[0]
                    if(isinstance(set2, list)):
                        set2 = set2[0]
                    chr_result_operations.append(set1_.union(set2))
                i += 2
            elif(char_def[i] == '-'):
                set2 = char_def[i+1]
                set1_ = chr_result_operations.pop()
                snum = ''
                if('chr(' in set2.lower()):
                    for e in set2:
                        if(e.isdigit()):
                            snum += e
                    num = int(snum)
                    set2 = set(chr(num))
                    chr_result_operations.append(set1_.difference(set2))
                else:
                    chr_result_operations.append(set1_.difference(set2))
                i += 2
            else:
                print('no operations else!!!!!!!!!!! :O')
                i += 1
        return i, chr_result_operations

    def whenAoraFound(self,char_def,i,subs_char_def):
        if('..' in char_def):
            start = ord(char_def[i])
            end = ord(char_def[i+2])
            letter_range = [set([chr(char) for char in range(start,end)])]
            i += 3
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,letter_range)
                subs_char_def.append(chr_result_operations)
            else:
                subs_char_def.append(letter_range)
        else:
            any_word = set(char_def[i])
            i += 1
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,any_word)
                subs_char_def.append(chr_result_operations)
            else:
                subs_char_def.append([any_word])

        return i, subs_char_def

    def whenANYFound(self,char_def,i,subs_char_def):
        anyy = set([chr(char) for char in range(0,255)])
        i += 1
        if(i < len(char_def)):
            i,chr_result_operations = self.setOperations(i,char_def,anyy)
            subs_char_def.append(chr_result_operations) 
        else:
            subs_char_def.append(anyy)

        return i, subs_char_def

    def whenChrFound(self,char_def,i,subs_char_def):
        if('..' in char_def):
            snum = ''
            enum = ''
            for e in char_def[i]:
                if(e.isdigit()):
                    snum += e
            for e in char_def[i+2]:
                if(e.isdigit()):
                    enum += e
            start = int(snum)
            end = int(enum)
            i += 3
            chr_range = set([chr(char) for char in range(start,end)])
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,chr_range)
                subs_char_def.append(chr_result_operations)
            else:
                subs_char_def.append(chr_range)

            return i, subs_char_def
        else:
            snum = ''
            for e in char_def[i]:
                if(e.isdigit()):
                    snum += e
            num = int(snum)
            i += 1
            first_char_in_expresion = [set([chr(num)])]
            if(i < len(char_def)):
                i,chr_result_operations = self.setOperations(i,char_def,first_char_in_expresion)
                subs_char_def.append(chr_result_operations) 
            else:
                subs_char_def.append(first_char_in_expresion)

            return i, subs_char_def
                    
    def dictSubstitionItself(self,dict1):
        dict_result = {}
        for key,char_def in dict1.items():
            i = 0
            new_exp = []
            while i < len(char_def):
                value_key = char_def[i]
                substitution = self.functions.get_value_from_dict(value_key,dict1)
                if(substitution != None):
                    new_exp.append(substitution[0])
                else:
                    new_exp.append(char_def[i])
                i += 1

            dict_result[key] = new_exp
        return dict_result

    def dictSubstitionOther(self,dict1,dict2):
        dict_result = {}
        for key,char_def in dict1.items():
            i = 0
            new_exp = []
            while i < len(char_def):
                value_key = char_def[i]
                substitution = self.functions.get_value_from_dict(value_key,dict2)
                if(substitution != None):
                    new_exp.append(substitution)
                else:
                    new_exp.append(char_def[i])
                i += 1

            dict_result[key] = new_exp
        return  dict_result

    def charactersSubstitution(self):
        """funcion que sustituye caracteres
        """
        charactersInFileSubs0 = {}
        charArray = []
        # ciclo para convertir los strings en arrays que encapsulen cada operando (item) de la expresion del caracter
        for key, char_def in self.charactersInFile.items():
            new_char_def = []
            has_space_char = False

            ss = char_def.split(' ')
            for i in ss:
                if (len(i) > 0):
                    e = ''
                    if(i.count('"') == 2):
                        e = i.replace('"','')
                        new_char_def.append(e)
                    elif(i.count("'") == 2):
                        e = i.replace("'",'')
                        new_char_def.append(e)
                    else:
                        new_char_def.append(i)

            # if para espacio en blanco ' '
            if("'" in new_char_def):
                ind = new_char_def.index("'")
                if(ind+1 < len(new_char_def)):
                    obj_ind2 = new_char_def[ind+1]
                    if(obj_ind2 == "'"):
                        new_char_def.pop(ind)
                        new_char_def.pop(ind)
                        new_char_def.insert(ind,'CHR(32)')
            if key == 'operadores' or key == 'operators':
                new_char_def[0] = new_char_def[0] + '='
            charactersInFileSubs0[key] = new_char_def

        charactersInFileSubs1 = self.dictSubstitionItself(charactersInFileSubs0)


        #! CHECAR LUEGO DE HEXDIGIT!!!!
        for key,char_def in charactersInFileSubs1.items():

            subs_char_def = []
            subs_char_def2 = []

            i = 0
            while i < len(char_def):
                curr = char_def[i]
                if(char_def[i] == ' '):
                    i +=1
                    continue
                elif('chr(' in char_def[i].lower()):
                    i, subs_char_def = self.whenChrFound(char_def,i,subs_char_def)
                elif('ANY' in char_def[i]):
                    i, subs_char_def = self.whenANYFound(char_def,i,subs_char_def)
                elif('A' in char_def[i] or 'a' in char_def[i]):
                    i, subs_char_def = self.whenAoraFound(char_def,i,subs_char_def)
                else:
                    any_word = set(char_def[i])
                    i += 1
                    if(i < len(char_def)):
                        i,chr_result_operations = self.setOperations(i,char_def,any_word)
                        subs_char_def.append(chr_result_operations) 
                    else:
                        subs_char_def.append([any_word])

            self.charactersInFileSubs2[key] = set(map(ord,subs_char_def[0][0])) 


# ZONA DE FUNCIONES PARA RECORRER EXPRESIONES REGULARES DE COCO/R -----------------------------------------------------------------------
    #-----------------------------------------------------------
    def intoQuotationsApostrophesV2(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de ' ' o " " sin cosidrerar | y retorna el valor.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        if tokens_exp[c] == '"':
            q = '"'
        elif tokens_exp[c] == "'":
            q = "'"
        word_set = []
        c += 1
        word_set.append(q) #no se necesita que este la comilla o el apostrofe dentro del string
        while c < len(tokens_exp):
            if tokens_exp[c] == q:
                word_set.append(tokens_exp[c])
                c += 1
                break
            else:
                word_set.append(tokens_exp[c])
                c += 1

        #print('')
        
        itemsCount = 0
        expTempArray = []
        for i in word_set:
            if i not in '\'"':
                if(itemsCount > 0):
                    expArray.append(set(map(ord,set(i))))
                    expArray.append('~')
                else:
                    expArray.append(set(map(ord,set(i))))
                    expArray.append('~')
                    expTempArray.append(set(map(ord,set(i))))
                itemsCount += 1

        if len(expTempArray) == 0:
            if(word_set.count("'") > word_set.count('"')):
                expArray.append(set(map(ord,set('"'))))
            elif(word_set.count("'") < word_set.count('"')):
                expArray.append(set(map(ord,set("'"))))
        else:
            #sacamos el ultimo operador de concatenacion que esta demas
            if(itemsCount > 0):
                expArray.pop() 
                
        return expArray, c 
#---
    def intoQuotationsApostrophes(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de ' ' o " " considerando | dentro y retorna el valor.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        if tokens_exp[c] == '"':
            q = '"'
        elif tokens_exp[c] == "'":
            q = "'"
        word_set = []
        c += 1
        word_set.append(q) #no se necesita que este la comilla o apostrofe del principio
        while c < len(tokens_exp):
            forwardOr = False
            if c+1 < (len(tokens_exp)):
                if tokens_exp[c+1] == "|":
                    forwardOr = True
            if forwardOr:
                if tokens_exp[c+2] in "'\"":
                    word_set.append(tokens_exp[c]) #se inserta el '
                    word_set.append(tokens_exp[c+1]) #se inserta el |
                    word_set.append(tokens_exp[c+2]) #se inserta el proximo '
                    c += 3
                else:
                    word_set.append(tokens_exp[c])
                    c += 1
                #continues
            elif tokens_exp[c] == q:
                #no se necesita que este la comilla o apostrofe del final
                word_set.append(tokens_exp[c]) 
                c += 1
                break
            else:
                word_set.append(tokens_exp[c])
                c += 1

        expArray.append(''.join(word_set))
        return expArray, c 
        
    def alphaNumericIterator(self,tokens_exp,c,expArray,considerOr=True):
        """Recorre una cadena de letras tomando en cuenta | y la retorna.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = []
        if considerOr:
            while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] == "|")):
                word_set.append(tokens_exp[c])
                c += 1
        else:
            while (c < len(tokens_exp) and tokens_exp[c].isalpha()):
                word_set.append(tokens_exp[c])
                c += 1
        word = ''.join(word_set)

        expArray.append(''.join(word_set))
        return expArray, c

    def intoParenthesis(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de ( ) y retorna el valor. 
        Hay recursion ya que pueden haber mas ( ) dentro.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = ['(']
        c += 1
        currentChar = (tokens_exp[c])
        while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] in "|)('\"") ):
            currentChar = (tokens_exp[c])
            if tokens_exp[c] == ')':
                word_set.append(tokens_exp[c])
                c += 1
                expArray.append(''.join(word_set))
                break
            elif tokens_exp[c] == '(':
                expArray, c = self.intoParenthesis(tokens_exp,c,expArray)
            else:
                word_set.append(tokens_exp[c])
                c += 1
        return expArray,c

    def intoBraces(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de { } y retorna el valor de conversion ()*. 
        Puede tener recursion pero se asume que no habran mas {} dentro de la expresion.

        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp

        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = ['(']
        c += 1
        currentChar = (tokens_exp[c])
        while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] in "|}{'\"") ):
            if tokens_exp[c] == '}':
                word_set.append(')*')
                c += 1
                expArray.append(''.join(word_set))
                break
            elif tokens_exp[c] == '{':
                expArray, c = self.intoBraces(tokens_exp,c,expArray)
            else:
                word_set.append(tokens_exp[c])
                c += 1
        return expArray,c

    def intoBrackets(self,tokens_exp,c,expArray):
        """Recorre los contenidos dentro de [ ] y retorna el valor. 
        Hay recursion ya que pueden haber mas [ ] dentro.
        Args:
            tokens_exp (str): cadena con tokens
            c (int): contador externo
            expArray (list): lista con todos los tokens encontrados en tokens_exp
        Returns:
            list: expArray actualizado
            int: el contador actualizado
        """
        word_set = ['(']
        expArray.append('(')
        c += 1
        currentChar = (tokens_exp[c])
        while (c < len(tokens_exp) and (tokens_exp[c].isalpha() or tokens_exp[c] in "|][}{'\"") ):
            currentChar = (tokens_exp[c])
            if tokens_exp[c] == ']':
                word_set.append(')|ε')
                openp = 0
                closep = 0
                for b in expArray:
                    if(')|ε' in b):
                        closep +=1
                    elif(b == '('):
                        openp += 1

                if(''.join(word_set) == "()|ε" and (closep != openp-1)):
                    exp = expArray.pop()
                    exp = exp + ')|ε'
                    expArray.append(exp)
                elif(''.join(word_set) == "()|ε" and (closep == openp-1)):
                    expArray.append(')|ε')
                else: 
                    expArray.append(''.join(word_set))
                c += 1
                break
            elif tokens_exp[c] == '[':
                expArray, c = self.intoBrackets(tokens_exp,c,expArray)
            elif tokens_exp[c] == '{':
                expArray, c = self.intoBraces(tokens_exp,c,expArray)
            elif tokens_exp[c] in "'\"":
                expArray, c = self.intoQuotationsApostrophes(tokens_exp,c,expArray)
            elif tokens_exp[c].isalpha():
                expArray, c = self.alphaNumericIterator(tokens_exp,c,expArray)
            else:
                word_set.append(tokens_exp[c])
                c += 1
        return expArray,c

# ZONA DE TRATAMIENTO DE TOKENS -----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
    def cocorToP1Convention(self):
        """funcion para acoplar las expresiones regulares al proyecto 1 haciendo conversiones como: 
        - kleene closure
            - digit{digit} = digit digit *
            - {} = * (0 o mas)  -->  r*
        - positive closure
            - [digit] = digit? = digit|ε
            - [] = ? (cero o una instancia)  -->  r? = r|ε
        - concatenacion
            - '~' = operador explicito para concatenacion
        """
        closures = []
        expArray = []
        for key, tokens_exp in self.tokensInFile.items():
            c = 0
            while c < len(tokens_exp):
                currentChar = tokens_exp[c]
                if tokens_exp[c] == " ":
                    c += 1
                    continue
                elif(tokens_exp[c] == "{"):
                    expArray, c = self.intoBraces(tokens_exp,c,expArray)
                elif(tokens_exp[c] == "("):
                    expArray, c = self.intoParenthesis(tokens_exp,c,expArray)
                elif(tokens_exp[c] == "["):
                    expArray, c = self.intoBrackets(tokens_exp,c,expArray)
                elif(tokens_exp[c].isalpha() or c == '|'):
                    expArray, c = self.alphaNumericIterator(tokens_exp,c,expArray)
                elif(tokens_exp[c] in "'\""):
                    expArray, c = self.intoQuotationsApostrophes(tokens_exp,c,expArray)
                elif(tokens_exp[c] in "})]"):
                    print('Revisar cerraduras de apertura en la expresion')
                else:
                    c += 1
                    print('else')

            finalExpArray = []
            c = 0

            if('(' in expArray):
                while (c < len(expArray)):
                    if(expArray[c] == '('):
                        exp = expArray[c] + expArray[c+1]
                        finalExpArray.append(exp)
                        c += 2
                    else:
                        finalExpArray.append(expArray[c])
                        c += 1

                finalExpString = '~'.join(finalExpArray)
                finalExpString = finalExpString.replace('~)',')')
                self.tokensConvertionInFile[key] = finalExpString
            else:
                expString = '~'.join(expArray)
                expString = expString.replace('~)',')')
                self.tokensConvertionInFile[key] = expString
            expArray = []

    def tokensPreparationPostfix(self):
        """funcion que prepara las expresiones para ser convertidas a formato postfix ya que estan en infix
        """
        expOpArray = []
        except_arr = []
        for key, tokens_exp in self.tokensConvertionInFile.items():
            c = 0
            if ('EXCEPT' in tokens_exp or 'KEYWORDS' in tokens_exp):
                except_arr.append('EXCEPT KEYWORDS')
                numToRemove = (len('EXCEPT')+len('KEYWORDS')+2)
                numCharacters = len(tokens_exp)-numToRemove
                tokens_exp_new = tokens_exp[:numCharacters]
            else:
                tokens_exp_new = tokens_exp

            while c < len(tokens_exp_new):
                currentChar = tokens_exp_new[c]
                if tokens_exp_new[c] == " ":
                    c += 1
                    continue
                elif(tokens_exp_new[c] in "~*|)("):
                    expOpArray.append(tokens_exp_new[c])
                    c += 1
                elif(tokens_exp_new[c].isalpha()):
                    expOpArray, c = self.alphaNumericIterator(tokens_exp_new,c,expOpArray,False)
                elif(tokens_exp_new[c] in "'\""):
                    expOpArray, c = self.intoQuotationsApostrophesV2(tokens_exp_new,c,expOpArray)
                else:
                    print(tokens_exp_new[c])

            if(len(except_arr) == 0):
                self.tokensReadyForPosFix[key] = expOpArray
            else:
                self.tokensReadyForPosFix[key] = expOpArray
            expOpArray = []
            except_arr = []


        #! esta conversion se hara luego de hacer el OR entre expresiones en orBetweenExpresions()

    def orBetweenExpresions(self):
        exp_final = []

        for key, exp in self.tokensReadyForPosFix.items():
            exp.insert(0,'(')
            exp += ['~','#',')']
            exp.append('|')
            exp_final += exp

        #Eliminamos el ultimo or | que no se necesita
        exp_final.pop() 

        exp_final_dict = {}
        exp_final_dict['exp'] = exp_final

        for key, exp in exp_final_dict.items():
            self.finalExpression[key] =  self.objToPostfix.infix_to_postfix(exp)

    def expresionSubstitutions(self):
        """Expresion final postfix con sustituciones aplicadas
        """
        dict1 = self.finalExpression
        dict2 = self.charactersInFileSubs2
        self.tokensSubstitutionExp = self.dictSubstitionOther(dict1,dict2)
        #print('')

        result = self.tokensSubstitutionExp['exp']
        return result

    def tokensSubstitutions(self):
        """Visualizar todas las expresiones infix sustituidas. 
            Funciona bien sin correr orBeetweenExpressions antes
        """
        dict1 = self.tokensReadyForPosFix
        dict2 = self.charactersInFileSubs2
        self.tokensSubstitution = self.dictSubstitionOther(dict1,dict2)

def main():


       


    obj = Cocor()

if __name__ == "__main__":
    main()