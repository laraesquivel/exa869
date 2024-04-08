from config import (OP_LOGIC_ONE_CHAR_SET, OP_RELATIONAL_ONE_CHAR_SET, 
                    REGEX_BLOCK_COMMENT_PATTERN)
import re

class Lexer:
    bloco_comentario_aberto = False
    bloco_commment = ""

    def __init__(self,line,line_number) -> None:
        self.line = line
        self.line_number = line_number
        self.current_char = line[0]
        self.next_char = line[1]
        self.before_char = None
        self.pos = 0
        self.current_token = None

        self.comentario_linha_aberto = False
        self.comentario_bloco_aberto = False
        self.cadeia_aberta = False
        self.op_logico_aberto = False
        self.op_relational_aberto = False

        self.raise_stop_iter = False
        self.end_block_comment = None

    def __iter__(self):
        return self
    
    def advance(self):
        self.pos+= 1
        print(self.pos)
        if self.pos < len(self.line):
            self.current_char = self.line[self.pos]
            self.before_char = self.line[self.pos - 1]
        else:
            self.current_char = None

        if self.pos < len(self.line) - 1:
            self.next_char = self.line[self.pos + 1]
        else:
            self.next_char = None

    def logic_operator(self):
        if self.op_logico_aberto:
            self.op_logico_abertoaberto = False
            self.current_token= ('','DESCARTE')
            
        else:
            if self.current_char == '!': #Subestado 1, Not
                self.current_token = (self.current_char, 'LOG', self.line_number)

            elif(self.current_char == self.next_char and not self.current_char== '!'): #Subsestado 2, Or ou and
                self.current_token = (self.current_char + self.next_char, 'LOG', self.line_number)
                self.op_logico_aberto = True
            
           

    def relational_operator(self):
        if self.op_relational_aberto:
            self.op_relational_aberto = False
            self.current_token = ('','DESCARTE')
        else:
            if self.next_char == '=':
                self.current_token = (self.current_char+self.next_char,'REL',self.line_number)
                self.op_relational_aberto = True
            elif self.next_char not in OP_RELATIONAL_ONE_CHAR_SET:
                self.current_token=(self.current_char, 'REL',self.line_number)
    
    def block_comment(self):
        text = self.line[self.pos:]
        correspondencia = re.findall(REGEX_BLOCK_COMMENT_PATTERN, text)

        if not any(correspondencia):
            print('entrei aqui')
            self.current_token=(self.line[self.pos:],'COM_ABERTO',self.line_number)
            print(self.current_token)
            self.raise_stop_iter = True
            
        else:
            coors = correspondencia[0]
            fim = self.pos + len(coors) 
            self.end_block_comment = fim
            self.current_token = (self.line[self.pos:fim],'DESCARTE',self.line_number)
            self.comentario_bloco_aberto = True
            




    def __next__(self):
        while self.pos < len(self.line): #Estado 0
            if self.comentario_linha_aberto or self.raise_stop_iter:
                raise StopIteration
            if self.comentario_bloco_aberto:
                if self.end_block_comment == self.pos:
                    self.comentario_bloco_aberto = False
                else:
                    self.current_token = ('','DESCARTE',self.line_number)

            if self.current_char == '/' and self.next_char=='*': #Estado 1 Comentario de Bloco
                self.block_comment()

            elif not self.comentario_bloco_aberto:
                if self.current_char =='/' and self.next_char=='/': #Estado 2 Comentario de Linha
                    self.current_token = ((self.line[self.pos:]),'DESCARTE',self.line_number)

                elif self.current_char in OP_LOGIC_ONE_CHAR_SET and self.next_char != '=': #Estado 4 Operador Lógico
                    self.logic_operator()

                elif self.current_char in OP_RELATIONAL_ONE_CHAR_SET: #Estado 5 Operador Relacional
                    self.relational_operator()
                
                else:
                    self.current_token = (self.current_char, "TESTE",self.line_number)


            self.advance()
            return self.current_token
        raise StopIteration



#a = "Ola  mundo! && || &| != == <=  => =-4 <=== /* Ola Lara Esquivel */"
a = '/*Ola Lara Esquivel'
l = Lexer(a,0)
for t in l:
    print(t)
