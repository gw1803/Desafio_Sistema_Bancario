from abc import ABC, abstractmethod

class Cliente():
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    @property
    def contas(self):
        return self._contas
    
    def realizar_transacao(self, transacao, conta):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self._cpf = cpf
        self._nome = nome
        self.data_nascimento = data_nascimento
        super().__init__(endereco)
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @classmethod
    def Pessoa_Fisica(cls, cpf, nome, data_nascimento, endereco):
        return cls(cpf, nome, data_nascimento, endereco)

class Transacao(ABC):
    
    @abstractmethod
    def registrar(conta):
        pass

class Deposito(Transacao):

    def __init__(self):
        self.valor = 0
    
    @classmethod
    def Deposito(cls):
        return cls()

    def registrar(self,conta):
        valorString = input("\nInforme o valor para depósito: ")
        self.valor = float(valorString)
        return conta.depositar(self)

class Saque(Transacao):

    def __init__(self):
        self.valor = 0
    
    @classmethod
    def Saque(cls, ):
        return cls()

    def registrar(self,conta):
        valorString = input("\nInforme o valor para saque: ")
        self.valor = float(valorString)
        return conta.sacar(self)

class Historico():
    def __init__(self, conteudo = ""):
        self._conteudo = conteudo

    @classmethod
    def Criar_Historico(cls):
        return cls()
    
    @property
    def conteudo(self):
        return self._conteudo

    def adicionar_transacao(self, transacao):
        if not self._conteudo:
            self._conteudo = "====EXTRATO===="

        if type(transacao) is Deposito:
            self._conteudo += f"\nDepósito: R${transacao.valor}"
        elif type(transacao) is Saque:
            self._conteudo += f"\nSaque: R${transacao.valor}"        

class Conta():

    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico.Criar_Historico()
        self._numero_saques = 0
 
    @property
    def tirar_extrato(self):
        return self._historico.conteudo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def saldo(self):
        return self._saldo or 0

class Conta_Corrente(Conta):

    def __init__(self, numero, cliente,limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._LIMITE_SAQUES = limite_saques

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    def depositar(self, transacao):
        if transacao.valor <=0 : 
            print("\nValor para depósito inválido")
            return False
         
        self._saldo += transacao.valor
        self._historico.adicionar_transacao(transacao)   
        return True
    
    def sacar(self, transacao):
        if self._numero_saques >= self._LIMITE_SAQUES:
            print("\nLimite de saques diários atigido")
            return False
        
        if transacao.valor<=0: 
            print("\nValor para saque inválido")
            return False
        elif(transacao.valor>self._limite):
            print("\nValor inserido além do limite da conta.")
            return False
        elif(transacao.valor>self._saldo):
            print("\nSaldo insuficiente.")
            return False

        self._saldo -= transacao.valor
        self._historico.adicionar_transacao(transacao)    
        self._numero_saques += 1
        return True

def tirar_extrato(saldo,/,*,extrato):
    if not extrato:
        print("\nNão foram realizadas movimentações")
        return None 

    print(extrato)
    print(f"Saldo atual R${float(saldo):0.2f}")

def criar_cliente(clientes):

    nome = input("\nInsira o nome do cliente: ")
    data_nascimento = input("\nInsira a data de nascimento do cliente: ")
    cpf = input("\nInsira o CPF do cliente: ")
    
    if "." or "-" in cpf:
        cpf = cpf.replace(".", "")
        cpf = cpf.replace("-", "")

    for cliente in clientes:
        if cliente.cpf == cpf:
            print("\nNão é possível concluir o cadastro, CPF já existente no sistema")
            return clientes

    logradouro = input("\nInsira o logradouro do cliente: ")
    numero = input("\nInsira o numero da casa do cliente: ")
    bairro = input("\nInsira o bairo do cliente: ")
    cidade = input("\nInsira a cidade do cliente: ")
    endereco = f"{logradouro} - {numero} - {bairro} - {cidade}"

    c = Pessoa_Fisica.Pessoa_Fisica(cpf, nome, data_nascimento, endereco)
    clientes.append(c)

    print("\nCliente criado com sucesso!")
    return clientes

def criar_conta_corrente(clientes, numero_contas):
    cpf = input("\nInsira o cpf do usuário: ")
    c = None

    for cliente in clientes:
        if str(cliente.cpf) == cpf:
            c = cliente

    if c == None:
        print("\nNão existe cliente cadastrado com esse CPF no sistema!")
        return False

    c.adicionar_conta(Conta_Corrente.nova_conta(c, numero_contas))
    return True

def listar_clientes(clientes):
    if not clientes:
        print("\nNenhum cliente cadastrado.")
    for cliente in clientes:
        print(f"\n\tNome : {cliente.nome}, CPF: {cliente.cpf}")

def listar_contas(clientes):
    for cliente in clientes:
        contas = cliente.contas
        for conta in contas:
            print(f"\n\t{conta.numero} -> {cliente.nome}")

def entrar_na_conta( clientes):
    numero = float(input("\nInsira o número da conta: "))
    for cliente in clientes:
        for conta in cliente.contas:
            if conta.numero == numero:
                return conta
    
    return None

def main():
    numero_contas = 0
    clientes = []
    c1 = Pessoa_Fisica.Pessoa_Fisica(123123, "Gabriel", "18-03-2004", "End" )
    c1.adicionar_conta(Conta_Corrente.nova_conta(c1, numero_contas))
    numero_contas += 1
    clientes.append(c1)
    conta_atual = None

    menu_1 = """
    [1] Criar cliente
    [2] Criar conta corrente
    [3] Listar clientes
    [4] Listar contas
    [5] Entrar na conta
    [6] Sair
    Entrada: """

    menu_2 = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    Entrada: """


    while True:
        opcao = input(menu_1)
        if opcao == "1":
            clientes = criar_cliente(clientes)

        elif opcao == "3":
            listar_clientes(clientes)
        
        elif opcao == "2":
            if criar_conta_corrente(clientes, numero_contas):
                print("\nConta criada com sucesso!")
                numero_contas += 1
            else: 
                print("\nNão foi possível criar uma conta.")

        elif opcao == "4":
            listar_contas(clientes)

        elif opcao == "5":
            conta_atual = entrar_na_conta(clientes)
            if not conta_atual:
                print("\nNão foi possível entrar na conta")
            else:
                while conta_atual:
                    opcao2 = input(menu_2)
                    if opcao2 =="d":
                        d = Deposito.Deposito()
                        if d.registrar(conta_atual):
                            print("\nDepósito realizado com sucesso!")
                        else:
                            print("\nNão foi possível concluir o depósito.")
                    elif opcao2 == "s":
                        s = Saque.Saque()
                        if s.registrar(conta_atual):
                            print("\nSaque realizado com sucesso!")
                        else:
                            print("\nNão foi possível concluir o saque.")
                    elif opcao2 == "e":
                        print(f"\nSaldo atual = R${conta_atual.saldo}")

                        if not conta_atual.tirar_extrato:
                            print("\nNão há movimentações")
                        else:
                            print(conta_atual.tirar_extrato)
                    elif opcao2 == "q":
                        conta_atual = None

                    else:
                        print("\nOperação inválida, por favor selecione novamente\n")

        elif opcao =="6":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente\n")

main()
