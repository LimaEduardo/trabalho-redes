import socket
import binascii

from convertCRC import CRC
from quadro import QuadroConfirmacao


def main():
    HOST = "177.105.60.169"              # Endereco IP do Servidor
    PORT = 60560                          # Porta que o Servidor esta

    #criando socket de conexao
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    meuIP = conn.getsockname()[0]

    # host de origem e porta de origem
    orig = (HOST, PORT)
    
    conn.bind(orig)
    conn.listen(1)
    # codExit = "#exit"
    # msgfinal = ""
    # while True:
    # Efetuando a conexao com cliente
    con, cliente = conn.accept()
    print("Concetado por", cliente)
    
    # byte a verificar é uma lista com todos bytes antes do codigo crc, para fazer verificação
    byteAVerificar = []

    # capturando o delimitador
    cabecalho = b''
    cabecalho += con.recv(1)
    byteAVerificar.append(cabecalho)
    if(len(cabecalho) <= 0):
        print("merda")

    # pegando dados de todo cabecalho (10bytes apos o delimitador)
    getBytes = geraListaBytes(con, 10)
    byteAVerificar += getBytes
    cabecalho += juntaBytes(getBytes)

    # pegando dados da msg (cabecalho[1] é lenght, que refere ao tamanho da mensagem)
    getBytes = geraListaBytes(con, cabecalho[1])
    byteAVerificar += getBytes
    dados = getBytes

    # pegando codigo CRC (2 bytes apos a msg)
    getBytes = geraListaBytes(con, 2)
    codeCrc = getBit(getBytes)[2:]
    
    msgCabeca = getBit(byteAVerificar)

    crcG = CRC(msgCabeca)
    # Teste o crc, ACK é o ultimo bit do campo sequence, ele refere se a mensagem foi enviada com sucesso
    if(crcG.verificarCRC(codeCrc)):
        # "Menssagem recebida com sucesso"
        meuAck = 1
    else:
        # "Mensagem corrompida"
        meuAck = 0

    bitSequence = [0, 1][cabecalho[2] == 128]
    quadroConfirmacao = QuadroConfirmacao(cliente[0], HOST, bitSequence, meuAck).getQuadro()

    dados = getBit(dados)
    n = int(dados, 2)
    dados = binascii.unhexlify('%x' % n).decode('ascii')
    print(dados)

    print(quadroConfirmacao)
    con.sendall(quadroConfirmacao)

    # print(cliente, str(msgfinal))

    print("Finalizando conexao do cliente", cliente)
    con.close()
    # return


def getBit(listaB):
    resultado = "0b"
    # print(listaB[0])
    for item in listaB:
        item = bin(int(str(item.hex()), 16))[2:]
        while(len(item) < 8):
            item = "0" + item
        resultado += item
    return resultado

def geraListaBytes(conn, qtdSerLido):
    lista = []
    for i in range(qtdSerLido):
        byteAtual = conn.recv(1)
        lista.append(byteAtual)
    return lista

def juntaBytes(listaDeBytes):
    result = b''
    for b in listaDeBytes:
        result += b
    return result

main()