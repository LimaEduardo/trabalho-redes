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
    PORT = 60560                 # Porta que o Servidor esta

    # HOST = "177.105.60.155"
    # PORT = 50017                 

    MAX_LENGHT = 50

    #criando socket de conexao
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    conn.connect(dest)

    # capturando o meu IP
    meuIP = conn.getsockname()[0]

    msg = "Aqui uma mensagem de tamanho menor que MAX_LENGHT"
    
    msg = divideMsg(msg, MAX_LENGHT)
    # print(msg)
    for indice,mensagem in enumerate(msg):
        msg[indice] = QuadroDados(HOST, meuIP, mensagem, str(indice%2)).getQuadro()
        # print(msg[indice])

        conn.send(msg[indice])

        quadConfirmacao = b''
        # capturando 'bit delimiter'
        quadConfirmacao += conn.recv(1)
        if(len(quadConfirmacao) <= 0):
            continue
        
        # Capturando 'bit sequence'
        quadConfirmacao += conn.recv(1)
        bitSequence = quadConfirmacao[1]
        print(quadConfirmacao)
        for i in range(8):
            quadConfirmacao += conn.recv(1)
        
        if(bitSequence % 2 == 0):
            print("Menssagem corrompida")
        else:
            print("Mensagem eviada ao servidor com sucesso")

    # conn.send("#exit".encode('ascii'))
    # print(msg)

    conn.close()

main()