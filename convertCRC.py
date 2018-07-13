import binascii

class CRC:
    def __init__(self, msg):
        self.polinomio = '11000000000000101'
        self.msg = msg[2:]
        self.code = (len(self.polinomio) - 1) * '0'


    def verificarCRC(self, code):
        return self.gerarCRC(code)

    def gerarCRC(self, code = '-1'):
        if(code == '-1'):
            code = self.code

        # print(self.msg)
        # print(code)

        tamanhoMsg = len(self.msg)

        # Adicionando o codigo ao fim da menssagem
        msg = self.msg + code

        # convertendo em listas
        msg = list(msg)
        polinomio = list(self.polinomio)

        for i in range(tamanhoMsg):
            # Caso encontre 1, percorremos len(code) bits para frente para verificar
            if msg[i] == '1':
                # teste com o polinomio os valores da msg
                for j in range(len(polinomio)):
                    msg[i+j] = str((int(msg[i+j]) ^ int(polinomio[j])))
        print(msg)
        # enviando somente o codigo que esta ao fim da menssagem
        return ''.join(msg[-len(code):])

def main():
    msg = bin(int(binascii.hexlify("Gabriel".encode('ascii')),16))
    
    m = CRC(msg)
    code = m.gerarCRC()
    msg = msg + code
    print(m.verificarCRC(code))

main()