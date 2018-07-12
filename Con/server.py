import socket
def main():
    HOST = "177.105.60.169"              # Endereco IP do Servidor
    PORT = 6060                          # Porta que o Servidor esta

    #criando socket de conexao
    conectionTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # host de origem e porta de origem
    orig = (HOST, PORT)

    conectionTcp.bind(orig)
    conectionTcp.listen(1)
    # codExit = "#exit"
    while True:
        # Efetuando a conexao com cliente
        con, cliente = conectionTcp.accept()
        print("Concetado por", cliente)
        while True:
            msg = con.recv(1024)
            # Caso tenha recebido uma mensagem vazia
            if msg:
                print(cliente, msg.decode('ascii'))
            else:
                print("Conexao comprometida ", cliente, " desconectado")
                return

            # Resposta do servidor ao cliente
            con.sendall('Recebido com sucesso'.encode('ascii'))

        print("Finalizando conexao do cliente", cliente)
        con.close()

main()