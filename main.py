from ponderado import GrafoPonderado
from votacao import Votacao


print("Deseja puxar os dados de determinada ano de votação? (S/N)\n ")
opcao = input()
if(opcao == "S" or opcao == "s"):
    print("Qual votação? (Digite 1 p/ 2023, Digite 2 p/ 2022)")
    Votacao = Votacao()
    i = int(input())
    if(i==1):
        url_votacoes = "https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio=2023-01-01&ordenarPor=dataHoraRegistro"
        print("Dados estão sendo extraídos do site https://dadosabertos.camara.leg.br/...\n")
        Votacao.votacao_dados(url_votacoes)
    elif(i==2):
        url_votacoes = "https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio=2022-01-01&ordenarPor=dataHoraRegistro"
        print("Dados estão sendo extraídos do site https://dadosabertos.camara.leg.br/...\n")
        Votacao.votacao_dados(url_votacoes)
    
else:
    print("Opção inválida.")