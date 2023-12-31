from tabulate import tabulate

# -- Ler o arquivo --
doc = open('./arquivos-txt/in-fcfs-2.txt', 'r', encoding='utf8')
nome_escalonamento = doc.readline().strip()

# -- Dados do Processo --
quantum = 0
prioridade_maior = 0
prioridade_menor = 0
processo_dados = []
execucoes = []

# -- Idenfica o escalonamento --

def identifica_escalonamento(nome_escalonamento):
    algoritmos = ['FIRST COME FIRST SERVED', 'FCFS',
                  'SHORTEST JOB FIRST', 'SJF', 'ROUND ROBIN', 'RR', 'PRIORITY']

    if nome_escalonamento in algoritmos:
        posicao = algoritmos.index(nome_escalonamento)

        if posicao == 0 or posicao == 1:
            utiliza_first_come_first_served()
        elif posicao == 2 or posicao == 3:
            utilizar_sjf()
        elif posicao == 4 or posicao == 5:
            utiliza_round_robin()
        elif posicao == 6:
            utiliza_prioridade()
    else:
        print('Não foi possível identificar o algoritmo de escalonamento! :(')

# -- Calcula tempo médio no sistema --


def calcula_media_tempo_sistema(tempos_no_sistema, total_processos):
    tempo_soma = 0

    for tempo in tempos_no_sistema:
        tempo_soma += tempo

    media = round((tempo_soma / total_processos), 2)
    return "Media de tempo no sistema: " + str(media)

# -- Calcula tempo médio de espera --


def calcula_media_tempo_espera(tempos_espera, total_processos):
    tempo_soma = 0

    for tempo in tempos_espera:
        tempo_soma += tempo

    media = round((tempo_soma / total_processos), 2)
    return "Media de tempo de espera: " + str(media)

# -- Gráfico de Gantt --
def registrar_execucao(pid, inicio, fim):
    return {'pid': pid, 'inicio': inicio, 'fim': fim}

def exibir_linha_do_tempo(execucoes):
    timeline = ""
    for execucao in execucoes:
        timeline += f" | P{execucao['pid']} ({execucao['inicio']} - {execucao['fim']})"
    return timeline + " |"

# -- Função que escreve no arquivo --

def escreve_saida(tabela_formatada, media_tempo_sistema, media_tempo_espera, linha_tempo):

    with open("saida.txt", "w") as arquivo:
        arquivo.write(tabela_formatada)
        arquivo.write("\n")
        arquivo.write(media_tempo_sistema)
        arquivo.write("\n")
        arquivo.write(media_tempo_espera)
        arquivo.write("\n\n")
        arquivo.write("Grafico de Gantt")
        arquivo.write("\n")
        arquivo.write(linha_tempo)


# -- Algoritmo FCFS --

def utiliza_first_come_first_served():

    processo_dados = [linha.replace('\u00a0', '').strip()
                      for linha in doc.readlines() if linha.strip() != ""]
    processos_inteiro = [[eval(dado) for dado in linha.split()]
                         for linha in processo_dados]

    processos_inteiro = sorted(processos_inteiro, key=lambda x: x[1])

    tabela_dados = [["Pid", "AT", "BT", "CT", "TAT", "WT"]]

    tempo_conclusao = 0
    tempo_atual = processos_inteiro[0][1]
    tempos_sistema = []
    tempos_espera = []
    processos_finalizados = []

    while processos_inteiro:

        fila = [
            p for p in processos_inteiro if p[1] <= tempo_atual]

        if not fila:
            tempo_atual += 1
            continue

        processo = fila[0]

        id_processo = processo[0]
        tempo_chegada = processo[1]
        tempo_cpu = processo[2]

        tempo_inicio = tempo_atual
        tempo_atual += tempo_cpu
        tempo_conclusao = tempo_atual
        tempo_sistema = tempo_conclusao - tempo_chegada
        tempo_espera = tempo_sistema - tempo_cpu

        execucoes.append(registrar_execucao(
            id_processo, tempo_inicio, tempo_conclusao))

        tempos_sistema.append(tempo_sistema)
        tempos_espera.append(tempo_espera)

        tabela_dados.append([id_processo, tempo_chegada, tempo_cpu,
                            tempo_conclusao, tempo_sistema, tempo_espera])

        processos_inteiro.remove(processo)
        processos_finalizados.append(processo)

    media_tempo_sistema = calcula_media_tempo_sistema(
        tempos_sistema, len(processos_finalizados))
    media_tempo_espera = calcula_media_tempo_espera(
        tempos_espera, len(processos_finalizados))
    
    tabela_dados = sorted(tabela_dados[1:], key=lambda x: x[0])
    tabela_dados.insert(0, ["Pid", "AT", "BT", "CT", "TAT", "WT"])

    tabela_formatada = tabulate(
        tabela_dados, headers="firstrow", tablefmt="grid")
    linha_tempo = exibir_linha_do_tempo(execucoes)

    escreve_saida(tabela_formatada, media_tempo_sistema,
                  media_tempo_espera, linha_tempo)

# -- Algoritmo SJF ---

def utilizar_sjf():
    processo_dados = [linha.replace('\u00a0', '').strip()
                      for linha in doc.readlines() if linha.strip() != ""]
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

        fila = [
            p for p in processos_inteiro if p[1] <= tempo_atual]

        if not fila:
            tempo_atual += 1
            continue

        processo = min(fila, key=lambda x: x[2])

        id_processo, tempo_chegada, tempo_cpu = processo
        tempo_conclusao = tempo_atual + tempo_cpu
        tempo_sistema = tempo_conclusao - tempo_chegada
        tempo_espera = tempo_sistema - tempo_cpu

        tempos_sistema.append(tempo_sistema)
        tempos_espera.append(tempo_espera)

        tabela_dados.append([id_processo, tempo_chegada, tempo_cpu,
                            tempo_conclusao, tempo_sistema, tempo_espera])

        tempo_inicio = tempo_atual
        tempo_atual = tempo_conclusao
        processos_inteiro.remove(processo)
        processos_finalizados.append(processo)

        execucoes.append(registrar_execucao(
            id_processo, tempo_inicio, tempo_conclusao))

    tabela_dados = sorted(tabela_dados[1:], key=lambda x: x[0])
    tabela_dados.insert(0, ["Pid", "AT", "BT", "CT", "TAT", "WT"])

    media_tempo_sistema = calcula_media_tempo_sistema(
        tempos_sistema, len(processos_finalizados))
    media_tempo_espera = calcula_media_tempo_espera(
        tempos_espera, len(processos_finalizados))

    tabela_formatada = tabulate(
        tabela_dados, headers="firstrow", tablefmt="grid")
    linha_tempo = exibir_linha_do_tempo(execucoes)
    escreve_saida(tabela_formatada, media_tempo_sistema,
                  media_tempo_espera, linha_tempo)

# -- algoritmo round robin --
def utiliza_round_robin():
    quantum = eval(doc.readline().strip())
    processo_dados = [linha.replace('\u00a0', '').strip()
                      for linha in doc.readlines() if linha.strip() != ""]
    processos = [[eval(dado) for dado in linha.split()]
                 for linha in processo_dados]
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

            tempo_inicio = tempo_atual
            tempo_executado = min(tempo_bt, quantum)
            tempo_atual += tempo_executado
            tempo_bt -= tempo_executado

            execucoes.append(registrar_execucao(
                id_processo, tempo_inicio, tempo_atual))

            processos_chegados = [p for p in processos if p[1] <= tempo_atual]
            for p in processos_chegados:
                p.append(p[2])
                fila.append(p)
                processos.remove(p)

            if tempo_bt > 0:
                fila.append([id_processo, tempo_chegada,
                            tempo_bt, tempo_cpu_original])
            else:
                tempo_conclusao = tempo_atual
                tempo_sistema = tempo_conclusao - tempo_chegada
                tempo_espera = tempo_sistema - tempo_cpu_original
                tabela_dados.append(
                    [id_processo, tempo_chegada, tempo_cpu_original, tempo_conclusao, tempo_sistema, tempo_espera])
        else:
            tempo_atual += 1

    media_tempo_sistema = calcula_media_tempo_sistema(
        [row[4] for row in tabela_dados[1:]], len(tabela_dados) - 1)
    media_tempo_espera = calcula_media_tempo_espera(
        [row[5] for row in tabela_dados[1:]], len(tabela_dados) - 1)

    tabela_dados = sorted(tabela_dados[1:], key=lambda x: x[0])
    tabela_dados.insert(0, ["Pid", "AT", "BT", "CT", "TAT", "WT"])

    tabela_formatada = tabulate(
        tabela_dados, headers="firstrow", tablefmt="grid")
    linha_tempo = exibir_linha_do_tempo(execucoes)
    escreve_saida(tabela_formatada, media_tempo_sistema,
                  media_tempo_espera, linha_tempo)

# -- Algoritmo Priority ---


def utiliza_prioridade():
    prioridades = doc.readline().split()
    menor_prioridade = eval(prioridades[0].strip())
    maior_prioridade = eval(prioridades[1].strip())

    processo_dados = [linha.replace('\u00a0', '').strip()
                      for linha in doc.readlines() if linha.strip() != ""]
    processos = [[eval(dado) for dado in linha.split()]
                 for linha in processo_dados]
    tabela_dados = [["Pid", "PR", "AT", "BT", "CT", "TAT", "WT"]]

    tempo_atual = 0
    fila = []

    while processos or fila:
        processos_chegados = [p for p in processos if p[2] <= tempo_atual]
        for p in processos_chegados:
            p.append(p[3])
            fila.append(p)
            processos.remove(p)

        if fila:
            if maior_prioridade > menor_prioridade:
                fila = sorted(fila, key=lambda x: x[1], reverse=True)
            elif maior_prioridade < menor_prioridade:
                fila = sorted(fila, key=lambda x: x[1])

            processo = fila.pop(0)
            id_processo, prioridade, tempo_chegada, tempo_bt, tempo_cpu_original = processo

            if processos:
                tempo_inicio = tempo_atual
                tempo_atual += 1
                tempo_bt -= 1

                execucoes.append(registrar_execucao(
                    id_processo, tempo_inicio, tempo_conclusao))
            elif not processos:
                tempo_inicio = tempo_atual
                tempo_atual += tempo_bt
                tempo_bt = 0
                execucoes.append(registrar_execucao(
                    id_processo, tempo_inicio, tempo_conclusao))

            if tempo_bt > 0:
                fila.append([id_processo, prioridade, tempo_chegada,
                            tempo_bt, tempo_cpu_original])
            else:
                tempo_conclusao = tempo_atual
                tempo_sistema = tempo_conclusao - tempo_chegada
                tempo_espera = tempo_sistema - tempo_cpu_original
                tabela_dados.append([id_processo, prioridade, tempo_chegada,
                                    tempo_cpu_original, tempo_conclusao, tempo_sistema, tempo_espera])
        else:
            tempo_atual += 1

    media_tempo_sistema = calcula_media_tempo_sistema(
        [row[5] for row in tabela_dados[1:]], len(tabela_dados) - 1)
    media_tempo_espera = calcula_media_tempo_espera(
        [row[6] for row in tabela_dados[1:]], len(tabela_dados) - 1)
    
    tabela_dados = sorted(tabela_dados[1:], key=lambda x: x[0])
    tabela_dados.insert(0, ["Pid", "AT", "BT", "CT", "TAT", "WT"])

    tabela_formatada = tabulate(
        tabela_dados, headers="firstrow", tablefmt="grid")
    linha_tempo = exibir_linha_do_tempo(execucoes)
    escreve_saida(tabela_formatada, media_tempo_sistema,
                  media_tempo_espera, linha_tempo)


identifica_escalonamento(nome_escalonamento.upper())
