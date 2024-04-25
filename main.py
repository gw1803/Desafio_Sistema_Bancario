menu = """

[c] Criar usuário
[l] Listar usuários
[o] Criar conta corrente
[k] Listar contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0.0
limite = 500
extrato = """"""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"
usuarios = []
numero_contas = 0
contas = []

#keyword only
def sacar(*, saldo, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= LIMITE_SAQUES:
        print("O limite de saques diários foi atigido")
        return saldo, extrato
        
    valor = input("\nInforme o valor para saque: ")
    valorF = float(valor)
    if valorF<=0: 
        print("\nValor para saque inválido")
        return saldo, extrato
    if(valorF>limite):
        print("O valor requisitado está além do limite da conta.")
        return saldo, extrato

    elif(valorF>saldo):
        print("Não é possível sacar o dinheiro por falta de saldo.")
        return saldo, extrato

    saldo -= valorF
    extrato += f"\nSaque: R${valorF}"
    numero_saques += 1
    return saldo, extrato

#positional only
def despositar(saldo, extrato, /):
    valor = input("\nInforme o valor para depósito: ")
    if float(valor)<=0: 
        print("\nValor para depósito inválido")
        return saldo, extrato 
    saldo += float(valor)
    extrato += f"\nDepósito: R${float(valor)}"
    return saldo, extrato

#positional and keyword
def tirar_extrato(saldo,/,*,extrato):
    if not extrato:
        print("\nNão foram realizadas movimentações")
        return None 

    print(extrato)
    print(f"Saldo atual R${float(saldo):0.2f}")

def criar_usuario(usuarios):
    usuario = {"nome": "","data_de_nascimento": "", "cpf":"", "endereco": ""}

    usuario["nome"] = input("\nInsira o nome do usuário: ")
    usuario["data_de_nascimento"] = input("\nInsira a data de nascimento do usuário: ")
    usuario["cpf"] = input("\nInsira o CPF do usuário: ")
    
    if "." or "-" in usuario["cpf"]:
        usuario["cpf"] = usuario["cpf"].replace(".", "")
        usuario["cpf"] = usuario["cpf"].replace("-", "")

    for user in usuarios:
        if user["cpf"] == usuario["cpf"]:
            print("\nNão é possível concluir o cadastro, CPF já existente no sistema")
            return usuarios

    logradouro = input("\nInsira o logradouro do usuário: ")
    numero = input("\nInsira o numero da casa do usuário: ")
    bairro = input("\nInsira o bairo do usuário: ")
    cidade = input("\nInsira a cidade do usuário: ")
    usuario["endereco"] = f"{logradouro} - {numero} - {bairro} - {cidade}"

    usuarios.append(usuario)

    print("Usuário criado com sucesso!")
    return usuarios

def criar_conta_corrente( usuarios, numero_contas, agencia, contas):
    cpf = input("\nInsira o cpf do usuário: ")
    id_usuario = None

    for index, usuario in enumerate(usuarios):
        if usuario["cpf"] == cpf:
            id_usuario = index

    if id_usuario == None:
        print("\nNão existe um usuário com esse cpf no sistema!")
        return contas, numero_contas

    numero_contas += 1

    contas.append({"agencia":agencia, "numero_conta": numero_contas, "usuario": usuario })

    print("Conta criada com sucesso!")

    return contas, numero_contas

def listar_usuarios(usuarios):
    if not usuarios:
        print("\nNenhum usuário cadastrado.")
    for usuario in usuarios:
        print(f"\nNome : {usuario["nome"]}, CPF: {usuario["cpf"]}")

def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada.")
    for conta in contas:
        print(f"\nNúmero : {conta["numero_conta"]}, Usuário: {conta["usuario"]["nome"]}")
    
while True:

    opcao = input(menu)

    if opcao == "c":
       usuarios = criar_usuario(usuarios)

    elif opcao == "l":
        listar_usuarios(usuarios)
    
    elif opcao == "o":
        contas, numero_contas = criar_conta_corrente(usuarios, numero_contas, AGENCIA, contas)

    elif opcao == "k":
        listar_contas(contas)

    elif opcao == "d":
        saldo, extrato = despositar(saldo, extrato)

    elif opcao == "s":
        saldo, extrato = sacar(saldo = saldo, extrato = extrato, limite = limite, numero_saques = numero_saques, limite_saques = LIMITE_SAQUES)
        
    elif opcao == "e":
        tirar_extrato(saldo, extrato=extrato)

    elif opcao =="q":
        break

    else:
        print("\nOperação inválida, por favor selecione novamente\n")