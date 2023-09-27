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


# -- Idenfica o escalonamento --
def identifica_escalonamento():
    algoritmos = ['FIRST COME FIRST SERVED', 'FCFS', 'SHORTEST JOB FIRST', 'SJF', 'ROUND ROBIN', 'RR', 'PRIORITY']

    if nome_escalonamento in algoritmos:
        posicao = algoritmos.index(nome_escalonamento)
    else:
         print('Não foi possível identificar o algoritmo de escalonamento! :(')

    return posicao

# -- Gráfico de Gantt --
def criar_linha_do_tempo(tempo_conclusao, id_processo, tempo_cpu):
    
    fig, ax = plt.subplots(figsize=(8, 4))

    for i, processo in enumerate(id_processo):
        ax.barh(processo, tempo_cpu[i], left=id_processo[i], label=processo)
    
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Processo')
    ax.set_title('Gráfico de Gantt')

    ax.set_xlim(0, max(id_processo) + max(tempo_cpu) + 1)

    plt.grid(True)
    plt.show()

    with open('linhadotempo.txt', 'w') as arquivo:
        for tempo, processo in zip(id_processo, tempo_conclusao):
            arquivo.write(f"{tempo}: {processo}\n")

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

  tabela_formatada = tabulate(tabela_dados, headers="firstrow", tablefmt="grid")
  with open("saida.txt", "w") as arquivo:
    arquivo.write(tabela_formatada)

    criar_linha_do_tempo([4, 7, 8, 10, 15], ['1', '2', '3', '4', '5'], ['4', '3', '1', '2', '3'])


#while(processos_ordenados.length() > processsos_finalizados):
      
     




identifica_escalonamento()
utiliza_first_come_first_served()
