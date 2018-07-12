class QuadroDados:
    def __init__(self, init, destination, source, payload):
        self.delimiter = bytes.fromHex('7E')
        self.length = bytes.fromHex(len(payload))
        self.sequence = None
        self.destinationAddress = bytes.fromHext(destination)
        self.sourceAddress = bytes.fromhex(source)
        self.payload = str(payload).encode('ascii')
        self.crc = None
    

    #Todo: Calcular CRC
    def CalculoCRC(self);
        return None
    
    #bytes from hex
    
    #A ideia aqui é retornar a mensagem de modo que ela esteja pronta para ser enviada
    def __str__(self):
        return str(str(self.delimiter)+str(self.length)+str(self.sequence)+str(self.destinationAddress)+str(self.sourceAddress)+str(self.payload())+str(self.crc)).encode('ascii')

class QuadroConfirmacao:
    def __init__(self, destination, source):
        self.delimiter = None
        self.sequence = None
        self.destinationAddress = destination
        self.sourceAddress = source
