from tabulate import tabulate
import matplotlib.pyplot as plt

# -- Ler o arquivo --
doc = open('teste.txt', 'r', encoding='utf8')
nome_escalonamento = doc.readline().strip()

# -- Dados do Processo --
quantum = 0
prioridade_maior = 0
prioridade_menor = 0
processo_dados = []

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
    processos_inteiro = [[eval(dado) for dado in linha.split()] for linha in processo_dados]

    tabela_dados = [["Pid", "AT", "BT", "CT", "TAT", "WT"]]

    tempo_conclusao = 0
    tempos_sistema = []
    tempos_espera = []

    for id_processo, tempo_chegada, tempo_cpu in processos_inteiro:

        tempo_conclusao += tempo_cpu
        tempo_sistema = tempo_conclusao - tempo_chegada
        tempo_espera = tempo_sistema - tempo_cpu

        tempos_sistema.append(tempo_sistema)
        tempos_espera.append(tempo_espera)

        tabela_dados.append([id_processo, tempo_chegada, tempo_cpu, tempo_conclusao, tempo_sistema, tempo_espera])

    media_tempo_sistema = calcula_media_tempo_sistema(tempos_sistema, len(processos_inteiro))
    media_tempo_espera = calcula_media_tempo_espera(tempos_espera, len(processos_inteiro))

    tabela_formatada = tabulate(tabela_dados, headers="firstrow", tablefmt="grid")
    with open("saida.txt", "w") as arquivo:
        arquivo.write(tabela_formatada)
        arquivo.write("\n")
        arquivo.write(media_tempo_sistema)
        arquivo.write("\n")
        arquivo.write(media_tempo_espera)


    # criar_linha_do_tempo([4, 7, 8, 10, 15], ['1', '2', '3', '4', '5'], ['4', '3', '1', '2', '3'])

# -- Algoritmo JSF ---
def utilizar_sjf():
    processo_dados = [linha.replace('\u00a0', '').strip() for linha in doc.readlines() if linha.strip() != ""]
    processos_string = []
    processos_inteiro = []

    for n in processo_dados:
        processos_string.append(n.split())

    for processo in processos_string:
        aux = [eval(dado) for dado in processo]
        processos_inteiro.append(aux)

    tabela_dados = [
        ["Pid", "AT", "BT", "CT", "TAT", "WT"]
    ]

    # Inicializando variáveis
    tempo_atual = 0
    tempos_sistema = []
    tempos_espera = []
    processos_finalizados = []

    while processos_inteiro:

        processos_prontos = [p for p in processos_inteiro if p[1] <= tempo_atual]
        
        if not processos_prontos:
            tempo_atual += 1
            continue

        processo = min(processos_prontos, key=lambda x: x[2])

        id_processo, tempo_chegada, tempo_cpu = processo
        tempo_conclusao = tempo_atual + tempo_cpu
        tempo_sistema = tempo_conclusao - tempo_chegada
        tempo_espera = tempo_sistema - tempo_cpu

        tempos_sistema.append(tempo_sistema)
        tempos_espera.append(tempo_espera)

        tabela_dados.append([id_processo, tempo_chegada, tempo_cpu, tempo_conclusao, tempo_sistema, tempo_espera])

        tempo_atual = tempo_conclusao
        processos_inteiro.remove(processo)
        processos_finalizados.append(processo)

    tabela_dados = sorted(tabela_dados[1:], key=lambda x: x[1]) 
    tabela_dados.insert(0, ["Pid", "AT", "BT", "CT", "TAT", "WT"]) 

    media_tempo_sistema = calcula_media_tempo_sistema(tempos_sistema, len(processos_finalizados))
    media_tempo_espera = calcula_media_tempo_espera(tempos_espera, len(processos_finalizados))

    tabela_formatada = tabulate(tabela_dados, headers="firstrow", tablefmt="grid")
    with open("saida.txt", "w") as arquivo:
        arquivo.write(tabela_formatada)
        arquivo.write("\n")
        arquivo.write(media_tempo_sistema)
        arquivo.write("\n")
        arquivo.write(media_tempo_espera)

def utiliza_round_robin():
    quantum = eval(doc.readline().strip())
    processo_dados = [linha.replace('\u00a0', '').strip() for linha in doc.readlines() if linha.strip() != ""]
    processos = [[eval(dado) for dado in linha.split()] for linha in processo_dados]
    tabela_dados = [["Pid", "AT", "BT", "CT", "TAT", "WT"]]

    tempo_atual = 0
    fila = []

    while processos or fila:
        processos_chegados = [p for p in processos if p[1] <= tempo_atual]
        for p in processos_chegados:
            p.append(p[2]) 
            fila.append(p)
            processos.remove(p)

        if fila: 
            processo = fila.pop(0)
            id_processo, tempo_chegada, tempo_bt, tempo_cpu_original = processo
            
            tempo_executado = min(tempo_bt, quantum)
            tempo_atual += tempo_executado
            tempo_bt -= tempo_executado

            processos_chegados = [p for p in processos if p[1] <= tempo_atual]
            for p in processos_chegados:
                p.append(p[2]) 
                fila.append(p)
                processos.remove(p)
            
            if tempo_bt > 0:
                fila.append([id_processo, tempo_chegada, tempo_bt, tempo_cpu_original])
            else:
                tempo_conclusao = tempo_atual
                tempo_sistema = tempo_conclusao - tempo_chegada
                tempo_espera = tempo_sistema - tempo_cpu_original
                tabela_dados.append([id_processo, tempo_chegada, tempo_cpu_original, tempo_conclusao, tempo_sistema, tempo_espera])
        else:
            tempo_atual += 1 

    media_tempo_sistema = calcula_media_tempo_sistema([row[4] for row in tabela_dados[1:]], len(tabela_dados) - 1)
    media_tempo_espera = calcula_media_tempo_espera([row[5] for row in tabela_dados[1:]], len(tabela_dados) - 1)

    tabela_formatada = tabulate(tabela_dados, headers="firstrow", tablefmt="grid")
    with open("saida.txt", "w") as arquivo:
        arquivo.write(tabela_formatada)
        arquivo.write("\n")
        arquivo.write(media_tempo_sistema)
        arquivo.write("\n")
        arquivo.write(media_tempo_espera)

# -- Algoritmo Priority ---
def utiliza_prioridade():
    ...

identifica_escalonamento()
#utiliza_first_come_first_served()
#utilizar_sjf()
utiliza_round_robin()

