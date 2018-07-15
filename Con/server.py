import socket
import binascii

from convertCRC import CRC
from quadro import QuadroConfirmacao


def main():
    HOST = "177.105.60.169"              # Endereco IP do Servidor
    PORT = 60560                          # Porta que o Servidor esta

    #criando socket de conexao
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host de origem e porta de origem
    orig = (HOST, PORT)
    
    conn.bind(orig)
    conn.listen(1)

    
    while True:

        # Efetuando a conexao com cliente
        con, cliente = conn.accept()
        print("Concetado por", cliente)
        ultimoSeq = None
        conectado = True
        msgfinal = ""
        loopTest = 0
        while conectado:
            # byte a verificar é uma lista com todos bytes antes do codigo crc, para fazer verificação
            byteAVerificar = []

            # capturando o delimitador
            cabecalho = b''
            cabecalho += con.recv(1)
            
            byteAVerificar.append(cabecalho)
            if(len(cabecalho) <= 0):
                if loopTest <= 5:
                    continue
                else:
                    print("Falha ao receber mensagem")
                    return

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
            # Testa se o ultimo quadro enviado é referente ao quadro atual
            if(ultimoSeq == bitSequence):
                # continua para receber o proximo pacote
                continue

            # Pego os dados obtidos da captura e converto para string
            dados = getBit(dados)
            n = int(dados, 2)
            dados = binascii.unhexlify('%x' % n).decode('ascii')
            
            # Caso a msg seja #desconectar# finalizo a conexao com servidor
            if(dados == "#desconectar#"):
                conectado = False
                continue
            msgfinal += dados

            quadroConfirmacao = QuadroConfirmacao(cliente[0], HOST, bitSequence, meuAck).getQuadro()
            con.sendall(quadroConfirmacao)
            ultimoSeq = bitSequence


        print(cliente, str(msgfinal))

        print("Finalizando conexao do cliente", cliente)
        con.close()
        return


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