import socket
import binascii

from convertCRC import CRC
from quadro import QuadroDados

#Essa é a função que transforma em bit
def transformaEmBit(listaBytes):
    resultado = "0b"
    for item in listaBytes:
        item = bin(int(str(item.hex()), 16))[2:]
        while(len(item) < 8):
            item = "0" + item
        resultado += item
    return resultado

# dividindo a msg em tamanhos permitidos a ser enviados pela conexao
def divideMsg(msg, tamMax):
    listMsg = []
    pos = 0
    tamList = len(msg)
    while(pos < tamList):
        if((pos + tamMax) < tamList):
            listMsg.append(msg[pos : pos + tamMax])
        else:
            listMsg.append(msg[pos:])
        pos += tamMax

    return listMsg
    
def main():
    HOST = "177.105.60.169"     # Endereco IP do Servidor 55
    PORT = 60660                 # Porta que o Servidor esta

    # HOST = "177.105.60.155"
    # PORT = 50017                 

    MAX_LENGHT = 20

    #criando socket de conexao
    conectionTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    conectionTcp.connect(dest)

    # capturando o meu IP
    meuIP = conectionTcp.getsockname()[0]

    msg = "Meu nome e Gabriel" #Ribeiro Oliveira e isso e um trabalho"
    
    msg = divideMsg(msg, MAX_LENGHT)
    print(msg)
    for indice,mensagem in enumerate(msg):
        msg[indice] = QuadroDados(HOST, meuIP, mensagem, str(indice%2)).getQuadro()
        msgEnvio = msg[indice].encode('ascii')

        conectionTcp.send(msgEnvio)
        buffer = conectionTcp.recv(2048)

        print("Server diz: ", buffer.decode('ascii'))

    conectionTcp.send("#exit".encode('ascii'))
    print(msg)

    conectionTcp.close()

main()