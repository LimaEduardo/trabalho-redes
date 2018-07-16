import binascii
from convertCRC import CRC

# Essa classe é responsável por criar um quadro que vai ser utilizado no envio de informações para o servidor
# Ela deve receber:
    #IP da máquina que está destino (destination)
    #IP da máquina que está enviando (source)
    #A mensagem (payload)
    #Um bit de sequencia (bitSequence)
class QuadroDados:
    def __init__(self, destination, source, payload, bitSequence):
        # O byte delimitador é fixo
        self.delimiter = "0b01111110"
        # O byte tamanho é referente ao tamanho da mensagem(payload)
        self.length = self.defineTamanho(payload)
        # O byte de sequência do quadro
        self.sequence = self.defineSequence(bitSequence)
        # Endereço de destino do quadro. Ele recebe o ip de destino em string
        #e é convertido para bits (4 bytes).
        self.destinationAddress = self.converteIpBinario(destination)
        # Endereço da fonte do quadro. Ele recebe o ip da fonte em string
        #e é convertido para bits (4 bytes).
        self.sourceAddress = self.converteIpBinario(source)
        #Essa é a mensagem que vai ser enviada. Ela é convertida para bits
        self.payload = self.definePayload(payload)
        #Essa variável possui a concatenação dos campos anteriores em bits
        #Vai ser utilizada para criar o código CRC
        self.mensagemEmBits = self.preparaMensagem()
        #Enviamos os campos e recebemos o código
        self.codeCRC = CRC(self.mensagemEmBits).gerarCRC()
        #A mensagem final vai ser a concatenação dos campos + o código crc
        #esta é a mensagem que vai ser enviada na rede
        self.mensagemFinal = self.mensagemEmBits + self.codeCRC
    
    #Função que devolve o quadro em bytes para ser enviado para o servidor
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
     
    #Define o tamanho da mensagem em bits
    def defineTamanho(self, payload):
        #Pegamos o tamanho da string mensagem
        length = bin(len(payload))
        #retiramos os dois primeiros bits (que são '0b', indicando que estamos tratando um binário)
        length = length[2:]

        #Pode ser que a mensagem seja pequena, o que irá gerar um binário pequeno
        #Sendo assim, completamos a mensagem com 0's até que ela tenha 1 byte
        while (len(length) < 8):
            length = "0"+length
        #Concatenamos 0b no início para indicar que a string se trata de um binário
        length = "0b" + length
        return length
    
    # O bit de sequência irá variar o seu primeiro e seu último bit
    # O bit mais a esquerda será o número de sequência de envio de quadro (0 ou 1)
    # O bit mais a direita será o bit ACK. Como esse quadro apenas será utilizado no envio, 
    #   o bit ACK se torna irrelevante, logo, pode ser sempre 0
    def defineSequence(self,bitSequence):
        return "0b"+str(bitSequence)+"0000000"
    
    #Nessa função convertemos um ip para um número binário
    def converteIpBinario(self, ip):
        #Primeiro separamos os IP's por ponto
        #Exemplo: 192.168.0.1 se torna ['192','168','0','1']
        ip = ip.split(".")
        #Para cada item do nosso ip
        for posicao in range(len(ip)):
            #convertemos aquele número para binário retirando os dois primeiros bits '0b'
            ip[posicao] = bin(int(ip[posicao]))[2:]
            #Caso o item seja menor que um byte, devemos preenchê-los com zero.
            #Semelhante ao caso da mensagem.
            while(len(ip[posicao]) < 8):
                ip[posicao] = "0" + ip[posicao]
            #No final, incluímos o '0b' para dizer que trata-se de um número binário
            ip[posicao] = "0b" + ip[posicao]
        #No final, apenas concatenamos todos os elementos da lista ignorando o '0b'
        sequencia = "0b"
        for byte in ip:
            sequencia += byte[2:]
        return sequencia
    
    #Nesse momento iremos converter a mensagem para binário
    def definePayload(self,payload):
        #Começamos indicando que se trata de um binário
        binario = "0b"
        # para cara caracter da mensagem...
        for char in payload:
            #convertemos aquele char para um código binário
            novoChar = bin(int(binascii.hexlify(char.encode('ascii')), 16))
            #convertemos aquele char para um código binário
            novoChar = novoChar[2:]
            #caso seja um binário pequeno, colocaremos 0's no ínio para completar um byte
            while(len(novoChar) < 8):
                novoChar = "0"+novoChar
            #concatenamos aquele char a mensagem
            binario += novoChar
        return binario

    #Essa função prepara a mensagem para ser enviada para a 'criação' do código CRC
    def preparaMensagem(self):
        mensagem = self.delimiter + self.length[2:] + self.sequence[2:] + self.destinationAddress[2:] + self.sourceAddress[2:] + self.payload[2:]
        return mensagem
    
    def __str__(self):
        msg =  "Delimitador : " + self.delimiter + "\n"
        msg += "Lenght : " + self.length[2:] + "\n"
        msg += "Sequence : " + self.sequence[2:] + "\n"
        msg += "Destine Adress : " + self.destinationAddress[2:] + "\n"
        msg += "Source Adress : " + self.sourceAddress[2:] + "\n"
        msg += "Msg : " + self.payload[2:] + "\n"
        msg += "CRC: " + self.codeCRC
        
        return msg

# Essa classe é responsável por criar um quadro que vai ser utilizado no envio de confirmações para o cliente
# Ela deve receber:
    #IP da máquina que está destino (destination)
    #IP da máquina que está enviando (source)
    #Um bit de sequencia (bitSequence)
    #Confirmação de recebimento
class QuadroConfirmacao:
    def __init__(self, destination, source, bitSequence, ack):
        # bit fixo
        self.delimiter = self.delimiter = "0b01111110"
        # O byte de sequência do quadro, dessa vez utilizaremos o ack para confirmar o recebimento do quadro
        self.sequence = self.defineSequence(bitSequence, ack)
        # Endereço de destino do quadro. Ele recebe o ip de destino em string
        #e é convertido para bits (4 bytes).
        self.destinationAddress = self.converteIpBinario(destination)
        # Endereço da fonte do quadro. Ele recebe o ip da fonte em string
        #e é convertido para bits (4 bytes).
        self.sourceAddress = self.converteIpBinario(source)
        #Converte a mensagem para bit e prepare para o envio
        self.mensagemEmBits = self.preparaMensagem()
    
    # O bit de sequência irá variar o seu primeiro e seu último bit
    # O bit mais a esquerda será o número de sequência de envio de quadro (0 ou 1)
    # O bit mais a direita será o bit ACK. Como esse quadro apenas será utilizado no envio, 
    def defineSequence(self,bitSequence, ack):
        return "0b"+str(bitSequence)+"000000"+str(ack)
    
    #Retorna a mensagem em bytes para que o servidor possa enviar ao cliente
    def getQuadro(self):
        mensagemSeparada = []
        i = 0
        mensagemEmBit = self.mensagemEmBits[2:]
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
    
    #Nessa função convertemos um ip para um número binário
    # Mesma função lá de cima
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
    
    #Concatena todos os campos para em bits para depois converter em bytes
    def preparaMensagem(self):
        mensagem = self.delimiter + self.sequence[2:] + self.destinationAddress[2:] + self.sourceAddress[2:]
        return mensagem

#Exemplo de uso
if __name__ == "__main__":
    quadroDados = QuadroDados("192.168.0.1", "192.168.0.2", "ola mundo", 0).getQuadro()
    QuadroConfirmacao = QuadroConfirmacao("192.168.0.1", "192.168.0.2",0,1).getQuadro()
