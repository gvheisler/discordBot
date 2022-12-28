from os.path import exists
import pickle



# Pickle functions
def load_pickle(default, filename):
   if exists(f'{filename}.pickle'):
       with open(f'{filename}.pickle', 'rb') as f:
           return pickle.load(f)
   else:
       with open(f'{filename}.pickle', 'wb') as f:
           pickle.dump(default, f)
           return default

def save_pickle(obj, filename):
    with open(f'./{filename}.pickle', 'wb') as f:
        pickle.dump(obj, f)

prodID = load_pickle(1, 'prod_ids')

class Produto:
    def __init__(self, nome, custo, quant):
        global prodID
        self.id = prodID
        prodID+=1
        save_pickle(prodID, 'prod_ids')
        self.nome = nome
        self.custo = custo
        self.valor = float(custo*1.3)
        self.quant = quant

produtosCadastrados = load_pickle([], 'prod_cadastrados')

relatorio = load_pickle('tipo,data_venda,id_produto,nome_produto,valor_venda,quantidade,lucro,nova_quantidade\n', 'relatorio')


def cadastrarProduto(nome, custo, quant):
    for prod in produtosCadastrados:
        if prod.nome == nome:
            prod.custo = custo
            prod.valor = custo*1.3
            prod.quant += quant
            save_pickle(produtosCadastrados, 'prod_cadastrados')
            return
        
    p = Produto(nome, custo, quant)
    produtosCadastrados.append(p)
    save_pickle(produtosCadastrados, 'prod_cadastrados')
    return

def printaProdutos():
    s = ''
    str1 = ''
    if len(produtosCadastrados) == 0:
        print("Sem produtos cadastrados!")
    else:
        print('--------------------------------------------------------------------------------------')
        for prod in produtosCadastrados:
            s = str(s + str(prod.id) + ' | ' + str(prod.nome) + '\t| valor: ' + str(prod.valor) + '\t| quantidade: ' +str(prod.quant) + '\n--------------------------------------------------------------------------------------\n')
    print(s)     

def vendeProdutoID(id, quant):
    for prod in produtosCadastrados:
        if prod.id == id:
            if prod.quant - quant < 0:
                print("Estoque insuficiente")
                return
            else:
                prod.quant = prod.quant - quant
                relata(prod.id, quant)
                save_pickle(produtosCadastrados, 'prod_cadastrados')
                print(f'Agora o estoque de {prod.nome} é {prod.quant}')
                return
    print('Produto não cadastrado!')
    return

def vendeProdutoNome(nome, quant):
    for prod in produtosCadastrados:
        if prod.nome == nome:
            if prod.quant - quant < 0:
                print("Estoque insuficiente")
                return
            else:
                prod.quant = prod.quant - quant
                relata(prod.id, quant)
                save_pickle(produtosCadastrados, 'prod_cadastrados')
                print(f'Agora o estoque de {prod.nome} é {prod.quant}')
                return
    print('Produto não cadastrado!')
    return

def relata(id, quant):
    global relatorio
    data = '21/12/2022'
    for prod in produtosCadastrados:
        if prod.id == id:
            relatorio = str(relatorio + 'venda' + ',' + data + ',' + str(prod.id) + ',' + str(prod.nome) + ',' + str(prod.valor) + ',' + str(quant) + ',' + str((prod.valor - prod.custo) * quant) + ',' + str(prod.quant) + '\n')
            save_pickle(relatorio, 'relatorio')

def printaRelatorio():
    global relatorio
    print(relatorio)

def main():
    printaProdutos()
    cadastrarProduto('bis xtra', 2, 5)
    cadastrarProduto('coca café', 2.59, 10)
    cadastrarProduto('kit kat', 3.0, 8)
    cadastrarProduto('fanta laranja', 2.50, 15)
    printaProdutos()
    vendeProdutoID(1, 2)
    vendeProdutoID(2, 2)
    vendeProdutoID(1, 4)
    vendeProdutoID(4, 1)
    vendeProdutoID(4, 7)
    vendeProdutoID(6, 1)
    printaProdutos()
    printaRelatorio()


if __name__ == "__main__":
    main()