from abc import ABC, abstractmethod
from datetime import datetime
import functools
from pathlib import Path

ROOT_PATH = Path(__file__).parent

def decorador_de_log(funcao):
    @functools.wraps(funcao)
    def exibir_info(*args, **kwargs):
        now = datetime.now()
        tipoFuncao = None
        match funcao.__name__:
            case "registrar":
                if funcao.__qualname__ == "Deposito.registrar":
                    tipoFuncao = "Depósito"
                elif funcao.__qualname__ == "Saque.registrar":
                    tipoFuncao = "Saque"
            case "tirar_extrato":
                tipoFuncao = "Tirar extrato"
            case "criar_cliente":
                tipoFuncao = "Criar cliente"
            case "criar_conta_corrente":
                tipoFuncao = "Criar conta"

        argumentos = ""
        for arg in args:
            if argumentos:
                    argumentos += " | "
            if type(arg) is list:
                argumentos += f"Lista de {arg[0].__class__.__name__}"  
            elif type(arg) is int:
                argumentos += f"Valor inteiro: {arg}"
            else:  
                argumentos += f"{arg.__repr__()}"
        
        ret = funcao(*args, **kwargs)
        if type(ret) is list:
            argumentos += f" - Lista de {arg[0].__class__.__name__}" 
        else:
            argumentos += f" - {ret}"

        try:
            with open(ROOT_PATH / "log.txt", "a", encoding = "utf-8") as arquivo:
                arquivo.write(f"{now.strftime("%Y/%m/%d - %H:%M:%S")} - {tipoFuncao} - {argumentos}\n")
        except IOError as exc:
            print("Erro")

        
        return ret
    
    return exibir_info

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
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.nome}"
    
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
    
    def __repr__(self):
        return f"Transacao: {self.__class__.__name__}"

    @classmethod
    def Deposito(cls):
        return cls()

    @decorador_de_log
    def registrar(self,conta):
        valorString = input("\nInforme o valor para depósito: ")
        self.valor = float(valorString)
        return conta.depositar(self)

class Saque(Transacao):

    def __init__(self):
        self.valor = 0
    
    def __repr__(self):
        return f"Transacao: {self.__class__.__name__}"
    
    @classmethod
    def Saque(cls, ):
        return cls()
    
    @decorador_de_log
    def registrar(self,conta):
        valorString = input("\nInforme o valor para saque: ")
        self.valor = float(valorString)
        return conta.sacar(self)

class Historico():
    def __init__(self, conteudo = ""):
        self._conteudo = []

    @classmethod
    def Criar_Historico(cls):
        return cls()

    @property
    def conteudo(self):
        return self._conteudo

    def gerador_relatorio(self, tipo_transacao = None):
               
        for conteudo in self._conteudo:
            if conteudo.get("tipo") == tipo_transacao or tipo_transacao == None:
                yield conteudo
    
    def adicionar_transacao(self, transacao):
            tipo = None
            if transacao.__class__.__name__ == "Deposito":
                tipo = "Depósito"
            else:
                tipo = transacao.__class__.__name__
            self._conteudo.append(
                {
                    "tipo": tipo,
                    "valor": transacao.valor,
                }
            ) 
         
class Conta():

    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico.Criar_Historico()
        self._numero_saques = 0
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self._cliente.nome}"

    @decorador_de_log
    def tirar_extrato(self, tipo_transacao = None):
        for i in self._historico.gerador_relatorio(tipo_transacao):
            print(f"{i.get("tipo")} - R${i.get("valor")}")
    
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

@decorador_de_log
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

@decorador_de_log
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

class conta_iterador:
    def __init__(self, contas):    
        self.contas = contas
        self.contador = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self.contas[self.contador]
            self.contador += 1
            return f"\n\t{conta._numero}"
        
        except IndexError:
            raise StopIteration

def listar_contas(clientes):
    for cliente in clientes:
        contas = cliente.contas
        for conta in conta_iterador(contas):
            print(f"\n\t{conta} -> {cliente.nome}")

def entrar_na_conta(clientes):
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

    menu_extrato = """
    [d] = Exibir apenas depósitos
    [s] = Exibir apenas saques
    [Caracter] = Exibir tudo
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
                        opcao3 = input(f"\n{menu_extrato}")

                        match opcao3:
                            case "d":
                                conta_atual.tirar_extrato("Depósito")
                            case "s":
                                conta_atual.tirar_extrato("Saque")
                            case other:
                                conta_atual.tirar_extrato()

                        print(f"\nSaldo atual = R${conta_atual.saldo}")

                    elif opcao2 == "q":
                        conta_atual = None

                    else:
                        print("\nOperação inválida, por favor selecione novamente\n")

        elif opcao =="6":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente\n")

main()
