class QuadroDados:
    def __init__(self):
        self.delimiter = None
        self.length = None
        self.sequence = None
        self.destinationAddress = None
        self.sourceAddress = None
        self.payload = None
        self.crc = None
        self.sequenceField = False # Variável usada pra alternar entre 0 e 1

    def novaMensagem(self, destination, source, payload):
        self.delimiter = bytes.fromhex('7E')
        self.length = bytes([len(payload)])
        self.sequence = self.calculoSequence()
        self.destinationAddress = str(destination).encode('ascii')
        self.sourceAddress = str(source).encode('ascii')
        self.payload = str(payload).encode('ascii')
        self.crc = self.calculoCRC()
        return self

    #Todo: Calcular CRC
    def calculoCRC(self):
        #retorno inutil
        return bytes.fromhex('7E')
    
    # O quadro dados só é utilizado em envios, logo, 
    # só vai varia o primeiro bit. Então ou é '80' ou '00'
    def calculoSequence(self):
        if self.sequenceField:
            self.sequenceField = not self.sequenceField
            return bytes.fromhex('80')
        else:
            self.sequenceField = not self.sequenceField
            return bytes.fromhex('00')
    
    #A ideia aqui é retornar a mensagem de modo que ela esteja pronta para ser enviada
    #Depois de preparar a mensagem, limpamos a classe para ser utilziada novamente
    def retornaMensagem(self):
        mensagem = str(str(self.delimiter)+str(self.length)+str(self.sequence)+str(self.destinationAddress)+str(self.sourceAddress)+str(self.payload)+str(self.crc)).encode('ascii')
        self.delimiter = None
        self.length = None
        self.sequence = None
        self.destinationAddress = None
        self.sourceAddress = None
        self.payload = None
        self.crc = None
        return mensagem

class QuadroConfirmacao:
    def __init__(self, destination, source):
        self.delimiter = None
        self.sequence = None
        self.destinationAddress = destination
        self.sourceAddress = source

#Exemplo de uso
if __name__ == "__main__":
    # A ideia é instânciar apenas uma variavel do quadro de dados 
    # Em seguida, devemos criar novas mensagens usando a função "novaMensagem(destino, fonte, mensagem)" e pegar a mensagem com "retornaMensagem()"
    quadroDados = QuadroDados()
    mensagem1 = quadroDados.novaMensagem("192.168.0.1", "192.168.0.2", "ola mund").retornaMensagem()
    mensagem2 = quadroDados.novaMensagem("192.168.0.3", "192.168.0.4", "huehue").retornaMensagem()
    print(mensagem1)
    print(mensagem2)
