import socket
import binascii

from convertCRC import CRC

def main():
    HOST = "177.105.60.169"     # Endereco IP do Servidor 55
    PORT = 6060                 # Porta que o Servidor esta

    # HOST = "177.105.60.155"
    # PORT = 50017                 

    #criando socket de conexao
    conectionTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    conectionTcp.connect(dest)

    msg = "gabriel ribeiro"
    msg = bin(int(binascii.hexlify(msg.encode('ascii')),16))
    crcG = CRC(msg)
    msg += crcG.gerarCRC()

    codFim = "#exit"
    print(codFim)
    # msg = b''
    msg = msg.encode('ascii')
    while(msg.decode('ascii') != codFim):
        conectionTcp.send(msg)
        buffer = conectionTcp.recv(1024)
        
        print("Server diz: ", buffer.decode('ascii'))

        msg = input().encode('ascii')

    conectionTcp.close()

main()