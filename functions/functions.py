######################################################
# Cristopher Jose Rodolfo Barrios Solis 
#
######################################################
# funtions.py
######################################################

class functions:
    """functions class
    """

    def representsInt(self,st):
        try: 
            int(st)
            return True
        except ValueError:
            return False

    def getRegExUniqueTokens(self,postfix_regex,words=False):
        '''
        Funcion que obtiene los tokens unicos o el lenguaje de una expresion regular en formato postfix.
        '''
        ops = '*|.#'
        tokens = []
        for i in range(len(postfix_regex)):
            token = postfix_regex[i]
            op_exist = token in ops
            if(op_exist == False):
                tokens.append(token)

        return list(dict.fromkeys(tokens))

    def getRegExUniqueTokensV2(self,postfix_regex):
        '''
        Funcion que obtiene los tokens unicos o el lenguaje de una expresion regular en formato postfix.
        '''
        ops = '*|~#'
        tokens = []
        for i in range(len(postfix_regex)):
            token = postfix_regex[i]

            if(token != '*' and token != '|' and token != '~' and token != '#'):
                tokens.append(token)

        tokens_ = []
        [tokens_.append(x) for x in tokens if x not in tokens_]

        return tokens_


    def stringToArray(self,string):
        result = string.replace('',' ').split(' ')
        result.pop(0)
        result.pop()
        return result


    def isOperand(self,character):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        if character.isalnum() or character == "ε" or character == "#":
            return True
        return False

    def isOperandV2(self,character):
        """
        REtorna TRUE si el caracter ingresado es un alfanumerico, FALSE de lo contrario
        *@param ch: el caracter a ser probado
        """
        sett = False
        if (isinstance(character,set)): sett = True
        if sett or character == "ε" or character == "#":
            return True
        return False

    def is_op(self, a):
        """
        Testeamos si el caracter de entrada es un operando
        *@param a: caracter a ser probado
        """
        if a == '+' or a == '.' or a == '*' or a == '?' or a == '|':
            return True
        return False

    def replace_all_non_alphabet_chars_string(self,currentString,type):
        resultString = ''.join([s for s in currentString if s.isalpha()])
        return resultString

    def replace_all_non_digit_chars_string(self,currentString):
        resultString = ''.join([s for s in currentString if s.isdigit()])
        return resultString

    def get_value_from_dict(self,ext_key,dictionary):
        '''
        Funcion que retorna la llave para un caracter cualquiera en un diccionario.

        Parametros:
        - character: un caracter o token 
        '''
        for key, value in dictionary.items():
            if ext_key == key:
                return value

        return None