import pandas as pd
import requests
from ponderado import GrafoPonderado
import time

class Votacao:
 def __init__(self) -> None:
    pass



 def votacao_dados(self, url_votacoes):
    start = time.time()
    # Fazendo a requisição GET para obter o objeto JSON das votações
    response_votacoes = requests.get(url_votacoes)

    # Verifica se a requisição foi bem-sucedida (código de status 200)
    if response_votacoes.status_code == 200:
        # Convertendo o conteúdo da resposta para objeto JSON
        data_votacoes = response_votacoes.json()

        # Pré-processamento dos dados
        votos_deputados = {}
        nome_deputados = {}
        votacoes_ids = []

        # Acessando as informações relevantes no objeto JSON das votações
        for votacao in data_votacoes["dados"]:
            votacao_id = votacao["id"]
            votacoes_ids.append(votacao_id)

            # Endpoint da API para obter a lista de votos de uma votação específica
            url_votos = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{votacao_id}/votos"
            

            # Fazendo a requisição GET para obter o objeto JSON dos votos
            response_votos = requests.get(url_votos)

            # Verifica se a requisição dos votos foi bem-sucedida (código de status 200)
            if response_votos.status_code == 200:
                # Convertendo o conteúdo da resposta para objeto JSON
                data_votos = response_votos.json()

                votos_votacao = {}
                for voto in data_votos["dados"]:
                    deputado_id = voto["deputado_"]["id"]
                    nome_deputado = voto["deputado_"]["nome"]
                    voto_deputado = voto["tipoVoto"]
                    nome_deputados[deputado_id] = nome_deputado

                    # Relaciona o voto especifico de um deputado numa votação com seu ID
                    votos_votacao[deputado_id] = voto_deputado

                # Delega para cada votação especifica um dicionario com os votos dos deputados nela envolvidos
                votos_deputados[votacao_id] = votos_votacao

        # Criar o grafo ponderado
        g = GrafoPonderado()
        g.add_nodes(list(nome_deputados.values()))

        # Contador de participações de cada deputado
        count = {}
        for deputado_id in nome_deputados:
            count[deputado_id] = 0
        
        # Loop para percorrer todas as votações
        for votacao_id in votacoes_ids:
            # Passa os votos dos deputados naquela votação especifica para uma variavel
            votos_votacao = votos_deputados[votacao_id] 

            # Cria uma lista com os ids dos deputados que votaram naquela votação
            deputados_ids_votacao = list(votos_votacao.keys()) 

            # Pega o primeiro deputado do par
            for i in range(len(deputados_ids_votacao)):
                deputado_1_id = deputados_ids_votacao[i]
            

                # Contar se esse deputado participou da votação com um voto válido
                if votos_votacao[deputado_1_id] in ["Sim", "Não", "Abstenção"]:
                    count[deputado_1_id] += 1

                # Passa pra frente, formando 1 par de deputados
                for j in range(i + 1, len(deputados_ids_votacao)):
                    deputado_2_id = deputados_ids_votacao[j]
                    if votos_votacao[deputado_1_id] == votos_votacao[deputado_2_id] and votos_votacao[deputado_1_id] in ["Sim", "Não", "Abstenção"]:
                        # Incrementar o peso da aresta no grafo
                        if g.there_is_edge(nome_deputados[deputado_1_id], nome_deputados[deputado_2_id]):
                            g.adj_list[nome_deputados[deputado_1_id]][nome_deputados[deputado_2_id]] += 1
                            g.adj_list[nome_deputados[deputado_2_id]][nome_deputados[deputado_1_id]] += 1
                        else:
                            g.add_two_way_edge(nome_deputados[deputado_1_id], nome_deputados[deputado_2_id], 1)



        # Escrever no arquivo das relações
        with open("relacoes.txt", "w",encoding= 'utf-8') as file:
            file.write(g.__str__())

        # Escrever no arquivo das participações
        with open("participacoes.txt", "w",encoding= 'utf-8') as file:
            for deputado_id, nome_deputado in nome_deputados.items():
                file.write(str(nome_deputado).replace(" ", "_") + " " + str(count[deputado_id]) + "\n")

        end = time.time()
        print("Dados extraídos com sucesso em", end - start, "segundos.\n")

    else:
        # Caso a requisição das votações não seja bem-sucedida, imprimir o código de status para depuração
        print("Erro na requisição das votações. Código de status:", response_votacoes.status_code)