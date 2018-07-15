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
    
# def reenviaQuadro(quadro, bitSequence)

def main():
    HOST = "177.105.60.169"     # Endereco IP do Servidor 55
    PORT = 60560                 # Porta que o Servidor esta

    # HOST = "177.105.60.155"
    # PORT = 50017                 

    MAX_LENGHT = 20

    #criando socket de conexao
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    conn.connect(dest)

    # capturando o meu IP
    meuIP = conn.getsockname()[0]

    msg = "Esse E um trabalho de redes, e aqui na mensagem nao pode ter nenhum caracter acentuado"
    
    msg = divideMsg(msg, MAX_LENGHT)
    bitSequenceEnvio = ""

    for indice,mensagem in enumerate(msg):
        bitSequenceEnvio = str(indice%2)

        # Criando quadro de envio da mensagem e colocando na posicao de msg
        msg[indice] = QuadroDados(HOST, meuIP, mensagem, bitSequenceEnvio).getQuadro()

        # Enviando mensagem à quem estiver conectado
        conn.send(msg[indice])

        # Capturando o quadro de confirmaçao que é enviado pela conexao
        quadConfirmacao = b''
        # capturando 'bit delimiter'
        quadConfirmacao += conn.recv(1)
        # Caso esteja vazio, quer dizer que quadro se perdeu no caminho
        if(len(quadConfirmacao) <= 0):
            # ------> aqui deveria reenviar o quadro <------
            continue
        
        # Capturando 'bit sequence'
        quadConfirmacao += conn.recv(1)
        bitSequence = quadConfirmacao[1]
        for i in range(8):
            quadConfirmacao += conn.recv(1)
        

        bitSequenceRequest = ['0', '1'] [bitSequence >= 128]
        # Teste se resquest é referente ao ultimo quadro enviado pelo cliente

        if(bitSequenceRequest == bitSequenceEnvio):
            # Caso seja, eu vejo se mensagem foi recebida com sucesso
            if(bitSequence % 2 == 0):
                print("quadro corrompido")
            else:
                print("quadro enviado ao servidor com sucesso")
        else:
            # Caso nao seja, o quadro recebido não é referente ao ultimo enviado: 
            # ------> aqui deveria reenviar o quadro <------
            print("A confirmação recebida não corresponde com o quadro enviado")
    
    # Enviando pacote de desconexao
    bitSequenceEnvio = ['1', '0'][bitSequenceEnvio == '1']
    msgDesconexao = QuadroDados(HOST, meuIP, "#desconectar#", bitSequenceEnvio).getQuadro()
    conn.send(msgDesconexao)

    conn.close()

main()