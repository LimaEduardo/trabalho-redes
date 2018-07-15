import socket
import binascii

from convertCRC import CRC

def main():
    HOST = "177.105.60.169"              # Endereco IP do Servidor
    PORT = 6060                          # Porta que o Servidor esta

    #criando socket de conexao
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host de origem e porta de origem
    orig = (HOST, PORT)
    
    conn.bind(orig)
    conn.listen(1)
    # codExit = "#exit"
    # msgfinal = ""
    while True:
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
            continue

        # pegando dados de todo cabecalho (10bytes apos o delimitador)
        getBytes = geraListaBytes(con, 10)
        byteAVerificar += getBytes
        cabecalho += juntaBytes(getBytes)

        # pegando dados da msg (cabecalho[1] é lenght, que refere ao tamanho da mensagem)
        dados = b''
        getBytes = geraListaBytes(con, cabecalho[1])
        byteAVerificar += getBytes
        dados += juntaBytes(getBytes)

        # pegando codigo CRC (2 bytes apos a msg)
        getBytes = geraListaBytes(con, 2)
        # codeCrc += juntaBytes(getBytes)
        codeCrc = getBit(getBytes)[2:]
        
        msgCabeca = getBit(byteAVerificar)

        crcG = CRC(msgCabeca)
        if(crcG.verificarCRC(codeCrc)):
            resposta = "Menssagem recebida com sucesso"
        else:
            resposta = "Mensagem corrompida"
        
            # cabecalho = b''
            # cabecalho += con.recv(1)
            
            # # Tamanho do cabeçalho ate o campo de dados = 11 bytes
            # for i in range(11):
            #     cabecalho += con.recv(1)
            # meusBytes += cabecalho

            # quantDados = cabecalho[1]

            # dados = []
            # for i in range(quantDados):
            #     dados += con.recv(1)
            
            # meusBytes += dados
            # print(dados.decode('ascii'))
            # codCRC = con.recv(2)
            # meusBytes += codCRC

            # print("meus bytes: ", meusBytes)
            # a = 1
            # testa Caso tenha recebido uma mensagem vazia
            # if cabecalho:
            #     msg = dados.decode('ascii')
                
            #     code = codCRC.decode('ascii')
            #     msg = msg[:-17]

            #     # mensagem = msg[87:]
            #     # print(mensagem)
            #     # n = int(mensagem, 2)
            #     # string = binascii.unhexlify('%x' % n)
                
            #     msgfinal += msg 
            #     # msg = int(msg)
            #     print(cliente, str(msgfinal))

            #     crcG = CRC(msg)
            #     if(crcG.verificarCRC(code)):
            #         resposta = "Menssagem recebida com sucesso"
            #     else:
            #         resposta = "Mensagem corrompida"
            # else:
            #     print("Conexao: ", cliente, " desconectado")
            #     return

            # Resposta do servidor ao cliente

        con.sendall(resposta.encode('ascii'))
        return
        
        # print(cliente, str(msgfinal))

        print("Finalizando conexao do cliente", cliente)
        con.close()


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