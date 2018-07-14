import socket
import binascii

from convertCRC import CRC

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
        
        
        # while a != 1:
        
        cabecalho = b''
        cabecalho += con.recv(1)

        if(len(cabecalho) <= 0):
            continue
        # print(len(cabecalho))
            
        listByte = geraListaBytes(con, 10)

        cabecalho += juntaBytes(listByte)
        print(cabecalho[0])
        print(cabecalho[1])
        print(cabecalho[2])
        print(cabecalho[3:6])
        print(cabecalho[6:10])

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
        resposta = "nada"
        con.sendall(resposta.encode('ascii'))
        return
        
        # print(cliente, str(msgfinal))

        print("Finalizando conexao do cliente", cliente)
        con.close()

main()