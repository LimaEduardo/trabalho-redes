import socket
import binascii

from convertCRC import CRC

def main():
    HOST = "177.105.60.169"              # Endereco IP do Servidor
    PORT = 60660                          # Porta que o Servidor esta

    #criando socket de conexao
    conectionTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host de origem e porta de origem
    orig = (HOST, PORT)
    msgfinal = ""
    conectionTcp.bind(orig)
    conectionTcp.listen(5)
    # codExit = "#exit"
    while True:
        # Efetuando a conexao com cliente
        con, cliente = conectionTcp.accept()
        print("Concetado por", cliente)
        meusBytes = []
        while True:
            # msg = con.recv(1024)
            cabecalho = b''
            cabecalho += con.recv(1)
            
            # Tamanho do cabeçalho ate o campo de dados = 11 bytes
            for i in range(11):
                cabecalho += con.recv(1)
            meusBytes += cabecalho

            quantDados = cabecalho[1]

            dados = []
            for i in range(quantDados):
                dados += con.recv(1)
            
            meusBytes += dados

            codCRC = con.recv(2)
            meusBytes += codCRC

            print("meus bytes: ", meusBytes)
            # testa Caso tenha recebido uma mensagem vazia
            if cabecalho:
                msg = dados.decode('ascii')
                
                code = codCRC.decode('ascii')
                msg = msg[:-17]

                # mensagem = msg[87:]
                # print(mensagem)
                # n = int(mensagem, 2)
                # string = binascii.unhexlify('%x' % n)
                
                msgfinal += msg 
                # msg = int(msg)
                print(cliente, str(msgfinal))

                crcG = CRC(msg)
                if(crcG.verificarCRC(code)):
                    resposta = "Menssagem recebida com sucesso"
                else:
                    resposta = "Mensagem corrompida"
            else:
                print("Conexao: ", cliente, " desconectado")
                return

            # Resposta do servidor ao cliente
            con.sendall(resposta.encode('ascii'))

        
        print(cliente, str(msgfinal))

        print("Finalizando conexao do cliente", cliente)
        con.close()

main()