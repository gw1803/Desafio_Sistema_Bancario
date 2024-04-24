menu = """

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

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = input("\nInforme o valor para depósito: ")
        if float(valor)<=0: 
            print("\nValor para depósito inválido")
            continue
        saldo += float(valor)

        extrato += f"\nDepósito: R${float(valor)}"

    elif opcao =="s":
        print("Saque")
    
    elif opcao =="e":
        if not extrato:
            print("\nNão foram realizadas movimentações")
            continue
        print(extrato)
        print(f"Saldo atual R${float(saldo):0.2f}")

    elif opcao =="q":
        break

    else:
        print("\nOperação inválida, por favor selecione novamente\n")

