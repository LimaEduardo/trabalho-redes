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

# Aqui no reenvio tratamos como um envio normal, ou seja, tudo aquilo que é feito no envio, fazemos no reenvio
def reenviaQuadro(conn, quadro, bitSequence):
    enviado = False
    while enviado:
        conn.send(quadro)
        # Capturando o quadro de confirmaçao que é enviado pela conexao
        quadConfirmacao = b''
        # capturando 'bit delimiter'
        quadConfirmacao += conn.recv(1)
        # Caso esteja vazio, quer dizer que quadro se perdeu no caminho
        if(len(quadConfirmacao) <= 0):
            enviado = False
            continue

        # Capturando 'bit sequence'
        quadConfirmacao += conn.recv(1)
        bitSequence = quadConfirmacao[1]
        for i in range(8):
            quadConfirmacao += conn.recv(1)

        bitSequenceRequest = ['0', '1'] [bitSequence >= 128]
        # Teste se resquest é referente ao ultimo quadro enviado pelo cliente

        if(bitSequenceRequest == bitSequence):
            # Caso seja, eu vejo se mensagem foi recebida com sucesso
            if(bitSequence % 2 == 0): # sucesso é: bit de sequencia ter 1 no ACK
                enviado = False
                continue
            else:
                enviado = True
                continue
        else:
            enviado = False
            continue

def main():
    HOST = "177.105.60.169"     # Endereco IP do Servidor 55
    PORT = 6060                 # Porta que o Servidor esta

    # HOST = "177.105.60.155"
    # PORT = 50017                 

    MAX_LENGHT = 255

    #criando socket de conexao
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    conn.connect(dest)

    # capturando o meu IP
    meuIP = conn.getsockname()[0]

    msg  = "Todos nos ja ouvimos falar certamente em redes de comunicacao (tambem designadas de redes informaticas ou redes de dados).\n"
    msg += "Uma \"rede\" (na Area da informatica), e definida como um conjunto de equipamentos interligados entre si, e que permitem o transporte e troca de varios tipos de informacao entre utilizadores e sistemas."
    msg += "O TCP e o protocolo mais usado isto porque fornece garantia na entrega de todos os pacotes entre um PC emissor e um PC receptor.\n"
    msg += "No estabelecimento de ligacao entre emissor e receptor existe um \"pre-acordo\" denominado de Three Way Handshake (SYN, SYN-ACK, ACK)."
    msg += "\n\nNo UDP: O UDP E um protocolo mais simples e por si so nao fornece garantia na entrega dos pacotes. No entanto, esse processo de garantia de dados pode ser simplesmente realizado pela aplicacao em si (que usa o protocolo UDP) e nao pelo protocolo.\n"
    msg += "Basicamente, usando UDP, uma maquina emissor envia uma determinada informacao e a maquina receptor recebe essa informacao, nao existindo qualquer confirmacao dos pacotes recebidos.\n"
    msg += "Se um pacote se perder nao existe normalmente solicitacao de reenvio, simplesmente nao existe."
    
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
            reenviaQuadro(conn, msg[indice], bitSequenceEnvio)
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
                print("Quadro corrompido... Reenviando")
                reenviaQuadro(conn, msg[indice], bitSequenceEnvio)
            else:
                print(indice + 1," º Quadro enviado ao servidor com sucesso")
        else:
            # Caso nao seja, o quadro recebido não é referente ao ultimo enviado: reenvia-lo
            reenviaQuadro(conn, msg[indice], bitSequenceEnvio)
            continue
    
    # Enviando pacote de desconexao
    bitSequenceEnvio = ['1', '0'][bitSequenceEnvio == '1']
    msgDesconexao = QuadroDados(HOST, meuIP, "#desconectar#", bitSequenceEnvio).getQuadro()
    conn.send(msgDesconexao)

    conn.close()

main()