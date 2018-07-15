import binascii
from convertCRC import CRC

class QuadroDados:
    def __init__(self, destination, source, payload, bitSequence):
        self.delimiter = "0b01111110"
        self.length = self.defineTamanho(payload)
        self.sequence = self.defineSequence(bitSequence)
        self.destinationAddress = self.converteIpBinario(destination)
        self.sourceAddress = self.converteIpBinario(source)
        self.payload = self.definePayload(payload)
        self.mensagemEmBits = self.preparaMensagem()
        self.codeCRC = CRC(self.mensagemEmBits).gerarCRC()
        self.mensagemFinal = self.mensagemEmBits + self.codeCRC
        print(self.mensagemEmBits)
        # self.traduzMensagem()
    
    def getQuadro(self):
        mensagemSeparada = []
        i = 0
        # print(self.mensagemFinal)
        mensagemEmBit = self.mensagemFinal[2:]
        while(i < len(mensagemEmBit)):
            novaMensagem = '0b'
            novaMensagem = mensagemEmBit[i:(i+8)]
            mensagemSeparada.append(novaMensagem)
            i += 8
        
        for posicao, mensagem in enumerate(mensagemSeparada):
            mensagemSeparada[posicao] = str(hex(int(mensagemSeparada[posicao], 2)))[2:]
            while(len(mensagemSeparada[posicao]) < 2):
                mensagemSeparada[posicao] = "0" + mensagemSeparada[posicao] 
            
        mensagemFinal = ""
        for mensagem in mensagemSeparada:
            mensagemFinal += mensagem
        
        mensagemFinal = bytes.fromhex(mensagemFinal)
        # print(mensagemFinal)
        return mensagemFinal
     
    def defineTamanho(self, payload):
        length = bin(len(payload))
        length = length[2:]

        while (len(length) < 8):
            length = "0"+length
        length = "0b" + length
        return length
    
    def defineSequence(self,bitSequence):
        return "0b"+str(bitSequence)+"0000000"
    
    def converteIpBinario(self, ip):
        ip = ip.split(".")
        for posicao in range(len(ip)):
            ip[posicao] = bin(int(ip[posicao]))[2:]
            while(len(ip[posicao]) < 8):
                ip[posicao] = "0" + ip[posicao]
            ip[posicao] = "0b" + ip[posicao]
        
        sequencia = "0b"
        for byte in ip:
            sequencia += byte[2:]
        return sequencia
    
    def definePayload(self,payload):
        binario = "0b"

        for char in payload:
            novoChar = bin(int(binascii.hexlify(char.encode('ascii')), 16))
            novoChar = novoChar[2:]

            while(len(novoChar) < 8):
                novoChar = "0"+novoChar
            
            binario += novoChar
        return binario

    def preparaMensagem(self):
        mensagem = self.delimiter + self.length[2:] + self.sequence[2:] + self.destinationAddress[2:] + self.sourceAddress[2:] + self.payload[2:]
        return mensagem
    
    def traduzMensagem(self):
        mensagem = self.mensagemFinal[87:-8]
        n = int(mensagem, 2)
        string = binascii.unhexlify('%x' % n)
        return string

    def __str__(self):
        msg =  "Delimitador : " + self.delimiter + "\n"
        msg += "Lenght : " + self.length[2:] + "\n"
        msg += "Sequence : " + self.sequence[2:] + "\n"
        msg += "Destine Adress : " + self.destinationAddress[2:] + "\n"
        msg += "Source Adress : " + self.sourceAddress[2:] + "\n"
        msg += "Msg : " + self.payload[2:] + "\n"
        msg += "CRC: " + self.codeCRC
        
        return msg

class QuadroConfirmacao:
    def __init__(self, destination, source, bitSequence, ack):
        self.delimiter = self.delimiter = "0b01111110"
        self.sequence = self.defineSequence(bitSequence, ack)
        self.destinationAddress = self.converteIpBinario(destination)
        self.sourceAddress = self.converteIpBinario(source)
        self.mensagemEmBits = self.preparaMensagem()
    
    def defineSequence(self,bitSequence, ack):
        return "0b"+str(bitSequence)+"000000"+str(ack)
    
    def getMensagem(self):
        return self.mensagemEmBits
    
    def converteIpBinario(self, ip):
        ip = ip.split(".")
        for posicao in range(len(ip)):
            ip[posicao] = bin(int(ip[posicao]))[2:]
            while(len(ip[posicao]) < 8):
                ip[posicao] = "0" + ip[posicao]
            ip[posicao] = "0b" + ip[posicao]
        
        sequencia = ""
        for byte in ip:
            sequencia += byte[2:]
        return sequencia
    
    def preparaMensagem(self):
        mensagem = self.delimiter + self.sequence[2:] + self.destinationAddress[2:] + self.sourceAddress[2:]
        return mensagem

#Exemplo de uso
if __name__ == "__main__":
    quadroDados = QuadroDados("192.168.0.1", "192.168.0.2", "ola mundo", 0).getQuadro()
