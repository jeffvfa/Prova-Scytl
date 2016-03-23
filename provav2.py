#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket   #biblioteca para realizar a conexão com o servidor
import binascii #biblioteca utilizada para transformar a mensagem recebida em binários

#informações de conexão obtidas no endereço http://test.scytlbrasil.com/
IP_SERVIDOR = "54.94.159.157"
PORTA = 50008

#dados sobre os pacotes obtidos através da tabela 2
START_PACKAGE = "11000110"
END_PACKAGE = "01101011"
END = "00100001"

#dicionários criados através da tabela 1 para realizar a conversão de base
FIVE_TO_FOUR = {
    '11110' : '0000',
    '01001' : '0001',
    '10100' : '0010',
    '10101' : '0011',
    '01010' : '0100',
    '01011' : '0101',
    '01110' : '0110',
    '01111' : '0111',
    '10010' : '1000',
    '10011' : '1001',
    '10110' : '1010',
    '10111' : '1011',
    '11010' : '1100',
    '11011' : '1101',
    '11100' : '1110',
    '11101' : '1111',
};

FOUR_TO_FIVE = {
    '0000': '11110',
    '0001': '01001',
    '0010': '10100',
    '0011': '10101',
    '0100': '01010',
    '0101': '01011',
    '0110': '01110',
    '0111': '01111',
    '1000': '10010',
    '1001': '10011',
    '1010': '10110',
    '1011': '10111',
    '1100': '11010',
    '1101': '11011',
    '1110': '11100',
    '1111': '11101',
}

#cria o socket
try:
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print 'Socket criado\n'
except Exception as e:
    print "ERRO! : " + e
    exit()
#conecta ao servidor
try:
    socket.connect((IP_SERVIDOR,PORTA))
    print 'Conectado ao servidor\n'
except Exception as e:
    print "ERRO! : " + e
    exit()

#função que adiciona 0 à esquerda para quando for  preciso os pacotes terem 8 bits
def addPad(string):
    novo = ''
    for binnarySeq in string.split():

        while len(binnarySeq) != 8:

            binnarySeq = '0'+ binnarySeq


        novo = novo + binnarySeq + ' '
    return novo

#função que retira os pacotes especiais (tabela 2)
def removeSpecial(string):
    x = ''
    trabalho = addPad(string)

    for package in trabalho.split():

        if package == START_PACKAGE:
            continue

        elif package == END_PACKAGE:
            continue

        elif package == END:
            return x

        else:
            x = x + package

    return x

#função que separa com um espaço em branco os bits em grupos de 5 bits
def splitInBaseFive(string):
    j = 1
    dividido = ''

    for bit in string:
        if j <= 5:
            dividido = dividido + bit
            j= j+1
        else:
            j = 2
            dividido = dividido + ' ' + bit

    return dividido

#função que realiza a mudança de base de acordo com o dicionário vindo da tabela 1
def encodeToFour(string):
    nova = ''

    for byte in string.split():
        nova = nova + FIVE_TO_FOUR[byte]

    return nova

#função que realiza a mudança de base de acordo com o dicionário vindo da tabela 1
def encodeToFive(string):
    nova = ''

    for byte in string.split():
        nova = nova + FOUR_TO_FIVE[byte]

    return nova

#função que separa com um espaço em branco os bits em grupos de 8 bits
def splitInBaseEight(string):
    j = 1
    dividido = ''
    for bit in string:
        if j <= 8:
            dividido = dividido + bit
            j= j+1
        else:
            j = 2
            dividido = dividido + ' ' + bit

    return dividido

#função que separa com um espaço em branco os bits em grupos de 4 bits
def splitInBaseFour(string):
    j = 1
    dividido = ''
    for bit in string:
        if j <= 4:
            dividido = dividido + bit
            j= j+1
        else:
            j = 2
            dividido = dividido + ' ' + bit

    return dividido

#função que converte a sequencia de bits para uma string ascii
def binToText(string):
    s = int(string, 2)
    s = binascii.unhexlify('%x' % s)
    return s

#função que converte uma string ascii para uma sequencia de bits
def textToBin(string):
    s = bin(int(binascii.hexlify(string), 16))
    s = str(s).replace('0b','')

    return s

#função para inverter a mensagem
def invert(string):
    string = string.rstrip()

    invertida = ''

    for letra in string:
        invertida = letra + invertida

    return invertida

#função que acrescenta os pacotes especiais da tabela 2
def codificarXProtocol(string):
    x = START_PACKAGE
    j = 1
    for pacote in string.split():
        if j <= 5:
            x = x + pacote
            j= j+1
        else:
            j = 2
            x = x + END_PACKAGE + START_PACKAGE + pacote

    x = x + END

    return x

#função que decodifica a mensagem
def decodeMessage(string):
    #converte a mensagem em binários
    trabalho = textToBin(string)

    #remove os pacotes especiais da tabela 2
    trabalho = removeSpecial(splitInBaseEight(trabalho))

    #faz a conversão de base da tabela 1
    trabalho = splitInBaseFive(trabalho)
    trabalho = encodeToFour(trabalho)

    #converte os binários já convertidos em uma string ascii
    trabalho = binToText(trabalho)

    #retorna a mensagem sem espaços em branco que podem estar à sua direita
    return trabalho.rstrip()

#função que codifica a mensagem
def encodeMessage(string):
    #verifica o tamanho da mensagem
    tam = len(string)

    #converte a mensagem em binário
    trabalho = textToBin(string)

    #se o tamanho da mensagem não for divisível por 4 acrescenta espaços em branco
    #   no final da mensagem até ser divisível por 4
    while (tam % 4) !=0 :
        trabalho = trabalho + '00100000'
        tam = tam+1

    #a funçãao 'textToBin' causa a perda de uns binários no começo, aqui eles são recuperados
    while (len(trabalho)%8) != 0:
        trabalho = '0'+trabalho

    #conversão de base da tabela 1
    trabalho = splitInBaseFour(trabalho)
    trabalho = encodeToFive(trabalho)

    #acréscimo dos pacotes especias da tabela 2
    trabalho = splitInBaseEight(trabalho)
    trabalho = codificarXProtocol(trabalho)

    #conversão dos binários para string ascii
    trabalho = binToText(trabalho)

    return trabalho

def main():
    mensagem = socket.recv(1024)

    print"mensagem recebida: " + mensagem + '\n'
    mensagem_decodificada = decodeMessage(mensagem)

    print "mensagem decodificada: " + mensagem_decodificada + "\n"

    invertida = invert(mensagem_decodificada)

    print "mensagem invertida: " + invertida + "\n"

    var = encodeMessage(invertida)

    print "mensagem encodificada novamente: " + var

    socket.send(var)
    socket.close()

    print "\nAcabou!\n"

if __name__ == '__main__':
    main()
