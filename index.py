from tabulate import tabulate
import matplotlib.pyplot as plt

# -- Ler o arquivo --
doc = open('teste.txt', 'r', encoding='utf8')
nome_escalonamento = doc.readline().strip()
quantum = 0
prioridade_maior = 0
prioridade_menor = 0
processo_dados = []
processsos_finalizados = []
processos_prontos = []


# -- Idenfica o escalonamento --
def identifica_escalonamento():
    algoritmos = ['FIRST COME FIRST SERVED', 'FCFS', 'SHORTEST JOB FIRST', 'SJF', 'ROUND ROBIN', 'RR', 'PRIORITY']

    if nome_escalonamento in algoritmos:
        posicao = algoritmos.index(nome_escalonamento)
    else:
         print('Não foi possível identificar o algoritmo de escalonamento! :(')

    return posicao

# -- Calcula tempo médio no sistema --
def calcula_media_tempo_sistema(tempos_no_sistema, total_processos):
    tempo_soma = 0

    for tempo in tempos_no_sistema:
        tempo_soma += tempo
    
    media = tempo_soma / total_processos
    return "Media de tempo no sistema: " + str(media)

# -- Calcula tempo médio de espera --
def calcula_media_tempo_espera(tempos_espera, total_processos):
    tempo_soma = 0

    for tempo in tempos_espera:
        tempo_soma += tempo
    
    media = tempo_soma / total_processos
    return "Media de tempo de espera: " + str(media)


# -- Gráfico de Gantt --
# def criar_linha_do_tempo(tempo_conclusao, id_processo, tempo_cpu):
#     # Crie o gráfico de Gantt
#     fig, ax = plt.subplots(figsize=(8, 4))

#     for i, processo in enumerate(id_processo):
#         ax.barh(processo, tempo_conclusao[i], label=f"{tempo_conclusao[i]} unidades de tempo")

#     # Defina os rótulos dos eixos
#     ax.set_xlabel('Tempo')
#     ax.set_ylabel('ID do Processo')
#     ax.set_title('Gráfico de Gantt')

#     # Defina a escala do eixo x
#     ax.set_xlim(0, max(tempo_conclusao) + 2)

#     # Adicione uma legenda
#     ax.legend()

#     # Exiba o gráfico de Gantt
#     plt.grid(True)
#     plt.show()


    # with open('linhadotempo.txt', 'w') as arquivo:
    #     for tempo, processo in zip(id_processo, tempo_conclusao):
    #         arquivo.write(f"{tempo}: {processo}\n")

# -- Algoritmo FCFS --
def utiliza_first_come_first_served():
  processo_dados = [linha.replace('\u00a0', '').strip() for linha in doc.readlines() if linha.strip() != ""]
  processos_string = []
  processos_inteiro = []

  for n in processo_dados:
      processos_string.append(n.split())

  for processo in processos_string:
      aux = []
      for dado in processo:
         dado = eval(dado)
         aux.append(dado)

      processos_inteiro.append(aux)

  print(processos_inteiro)
 
  tabela_dados = [
      ["Pid", "AT", "BT", "CT", "TAT", "WT"]
    ]

  processos_ordenados = sorted(processos_inteiro, key=lambda x: x[1])

# -- Variáveis do processo --
  id_processo = 0
  tempo_chegada = 0
  tempo_cpu = 0
  tempo_conclusão = 0
  tempo_sistema = 0
  tempo_espera = 0
  tempos_sistema = []
  tempos_espera = []
      
  for processo in processos_ordenados:

      processo_calculado = []

      id_processo = processo[0]
      processo_calculado.append(id_processo)

      tempo_chegada = processo[1]
      processo_calculado.append(tempo_chegada)

      tempo_cpu = processo[2]
      processo_calculado.append(tempo_cpu)

      tempo_conclusão += tempo_cpu
      processo_calculado.append(tempo_conclusão)

      tempo_sistema = tempo_conclusão - tempo_chegada
      processo_calculado.append(tempo_sistema)

      tempo_espera = tempo_sistema - tempo_cpu
      processo_calculado.append(tempo_espera)

      tabela_dados.append(processo_calculado)
      tempos_sistema.append(tempo_sistema)
      tempos_espera.append(tempo_espera)

  media_tempo_sistema = calcula_media_tempo_sistema(tempos_sistema, len(processos_ordenados))
  media_tempo_espera = calcula_media_tempo_espera(tempos_espera, len(processos_ordenados))

  tabela_formatada = tabulate(tabela_dados, headers="firstrow", tablefmt="grid")
  with open("saida.txt", "w") as arquivo:
    arquivo.write(tabela_formatada)
    arquivo.write("\n")
    arquivo.write(media_tempo_sistema)
    arquivo.write("\n")
    arquivo.write(media_tempo_espera)

    # criar_linha_do_tempo([4, 7, 8, 10, 15], ['1', '2', '3', '4', '5'], ['4', '3', '1', '2', '3'])

def utilizar_sjf():
    processo_dados = [linha.replace('\u00a0', '').strip() for linha in doc.readlines() if linha.strip() != ""]
    processos_string = []
    processos_inteiro = []

    for n in processo_dados:
        processos_string.append(n.split())

    for processo in processos_string:
        aux = []
        for dado in processo:
            dado = eval(dado)
            aux.append(dado)

        processos_inteiro.append(aux)

    print(processos_inteiro)
    
    tabela_dados = [
        ["Pid", "AT", "BT", "CT", "TAT", "WT"]
        ]

    processos_ordenados = sorted(processos_inteiro, key=lambda x: x[2])

    # -- Variáveis do processo --
    id_processo = 0
    tempo_chegada = 0
    tempo_cpu = 0
    tempo_conclusão = processos_ordenados[0][1]
    tempo_sistema = 0
    tempo_espera = 0
    tempos_sistema = []
    tempos_espera = []

    while (len(processos_ordenados) > len(processsos_finalizados)):
        tempo_atual = 0

        for processo in processos_ordenados:
            if processo[1] == tempo_atual:
                processos_prontos.append(processo)
        
        processos_prontos = sorted(processos_prontos, key=lambda x: x[2])

        for processo in processos_prontos:

            processo_calculado = []

            id_processo = processo[0]
            processo_calculado.append(id_processo)

            tempo_chegada = processo[1]
            processo_calculado.append(tempo_chegada)

            tempo_cpu = processo[2]
            processo_calculado.append(tempo_cpu)

            tempo_conclusão += tempo_cpu
            processo_calculado.append(tempo_conclusão)

            tempo_sistema = tempo_conclusão - tempo_chegada
            processo_calculado.append(tempo_sistema)

            tempo_espera = tempo_sistema - tempo_cpu
            processo_calculado.append(tempo_espera)

            tabela_dados.append(processo_calculado)
            tempos_sistema.append(tempo_sistema)
            tempos_espera.append(tempo_espera)

            processsos_finalizados.append(processo)
            processos_prontos.remove(0)

        tempo_atual += 1

    media_tempo_sistema = calcula_media_tempo_sistema(tempos_sistema, len(processos_ordenados))
    media_tempo_espera = calcula_media_tempo_espera(tempos_espera, len(processos_ordenados))

    tabela_formatada = tabulate(tabela_dados, headers="firstrow", tablefmt="grid")
    with open("saida.txt", "w") as arquivo:
        arquivo.write(tabela_formatada)
        arquivo.write("\n")
        arquivo.write(media_tempo_sistema)
        arquivo.write("\n")
        arquivo.write(media_tempo_espera)


#while(processos_ordenados.length() > processsos_finalizados):
      
     




identifica_escalonamento()
utiliza_first_come_first_served()
