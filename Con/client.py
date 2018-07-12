import socket

def main():
    HOST = "177.105.60.169"     # Endereco IP do Servidor 55
    PORT = 6060                 # Porta que o Servidor esta

    # HOST = "177.105.60.155"
    # PORT = 50017                 

    #criando socket de conexao
    conectionTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    conectionTcp.connect(dest)

    codFim = "#exit"
    print(codFim)
    msg = b''
    while(msg.decode('ascii') != codFim):
        msg = input().encode('ascii')

        conectionTcp.send(msg)
        buffer = conectionTcp.recv(1024)
        
        print("Server diz: ", buffer.decode('ascii'))

    conectionTcp.close()

main()