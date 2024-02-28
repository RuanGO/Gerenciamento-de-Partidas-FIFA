import tkinter as tk
from tkinter import messagebox
import itertools
import random

class JogoFutebol:
    def __init__(self):
        self.jogadores = []
        self.partidas = []
        self.resultados = {}

    def adicionar_jogador(self, jogador):
        self.jogadores.append(jogador)
        self.resultados[jogador] = {'vitorias': 0, 'derrotas': 0, 'pontuacao': 0}

    def gerar_partidas(self):
        self.partidas = [(jogador1, jogador2) for jogador1, jogador2 in itertools.combinations(self.jogadores, 2)]

    def embaralhar_partidas(self):
        random.shuffle(self.partidas)

    def realizar_partida(self, partida_index, vencedor):
        partida = self.partidas[partida_index]
        perdedor = [jogador for jogador in partida if jogador != vencedor][0]
        self.resultados[vencedor]['vitorias'] += 1
        self.resultados[perdedor]['derrotas'] += 1
        self.resultados[vencedor]['pontuacao'] += 3
        self.resultados[perdedor]['pontuacao'] -= 1
        self.partidas.pop(partida_index)
        if not self.partidas:
            self.exibir_ranking()
        else:
            exibir_partidas()

    def exibir_ranking(self):
        ranking = sorted(self.resultados.items(), key=lambda x: (x[1]['pontuacao'], x[1]['vitorias']), reverse=True)
        mensagem = "Ranking Final:\n\n"
        for posicao, (jogador, resultado) in enumerate(ranking, start=1):
            mensagem += f"{posicao}. {jogador}: Pontuação: {resultado['pontuacao']}, Vitórias: {resultado['vitorias']}, Derrotas: {resultado['derrotas']}\n"
        messagebox.showinfo("Ranking Final", mensagem)

def adicionar_jogador():
    jogador = nome_entry.get().strip()
    if jogador:
        jogo_futebol.adicionar_jogador(jogador)
        jogadores_listbox.insert(tk.END, jogador)
        nome_entry.delete(0, tk.END)

def gerar_partidas():
    jogo_futebol.gerar_partidas()
    exibir_partidas()

def embaralhar_partidas():
    jogo_futebol.embaralhar_partidas()
    exibir_partidas()

def exibir_partidas():
    for widget in partidas_frame.winfo_children():
        widget.destroy()

    if jogo_futebol.partidas:
        for index, partida in enumerate(jogo_futebol.partidas, start=1):
            tk.Label(partidas_frame, text=f"{index}. {partida[0]} vs {partida[1]}").grid(row=index-1, column=0, padx=5, pady=5)
            tk.Button(partidas_frame, text="Registrar Vencedor", command=lambda idx=index-1: exibir_menu_vencedor(idx)).grid(row=index-1, column=1, padx=5, pady=5)
    else:
        tk.Label(partidas_frame, text="Todas as partidas foram concluídas!").grid(row=0, column=0, padx=5, pady=5)

def exibir_menu_vencedor(partida_index):
    vencedor_menu = tk.Toplevel(window)
    vencedor_menu.title("Escolha o Vencedor")

    partida = jogo_futebol.partidas[partida_index]
    tk.Label(vencedor_menu, text=f"{partida[0]} vs {partida[1]}").pack(pady=5)

    vencedor = tk.StringVar()
    tk.Radiobutton(vencedor_menu, text=partida[0], variable=vencedor, value=partida[0]).pack()
    tk.Radiobutton(vencedor_menu, text=partida[1], variable=vencedor, value=partida[1]).pack()

    confirmar_button = tk.Button(vencedor_menu, text="Confirmar", command=lambda: registrar_partida(partida_index, vencedor.get(), vencedor_menu))
    confirmar_button.pack(pady=5)

def registrar_partida(partida_index, vencedor, vencedor_menu):
    jogo_futebol.realizar_partida(partida_index, vencedor)
    vencedor_menu.destroy()

# Configuração da janela principal
window = tk.Tk()
window.title("Torneio de Futebol")

# Frame para adicionar jogadores
adicionar_jogador_frame = tk.Frame(window)
adicionar_jogador_frame.pack(pady=10)

tk.Label(adicionar_jogador_frame, text="Nome do Jogador:").grid(row=0, column=0)
nome_entry = tk.Entry(adicionar_jogador_frame)
nome_entry.grid(row=0, column=1)

adicionar_button = tk.Button(adicionar_jogador_frame, text="Adicionar", command=adicionar_jogador)
adicionar_button.grid(row=0, column=2)

# Frame para exibir jogadores
jogadores_frame = tk.Frame(window)
jogadores_frame.pack(pady=10)

tk.Label(jogadores_frame, text="Jogadores:").pack()

jogadores_listbox = tk.Listbox(jogadores_frame, width=30)
jogadores_listbox.pack()

# Frame para ações do jogo
acoes_frame = tk.Frame(window)
acoes_frame.pack(pady=10)

gerar_partidas_button = tk.Button(acoes_frame, text="Gerar Partidas", command=gerar_partidas)
gerar_partidas_button.grid(row=0, column=0, padx=10)

embaralhar_partidas_button = tk.Button(acoes_frame, text="Embaralhar Partidas", command=embaralhar_partidas)
embaralhar_partidas_button.grid(row=0, column=1, padx=10)

# Frame para exibir as partidas
partidas_frame = tk.Frame(window)
partidas_frame.pack(pady=10)

# Inicialização do objeto JogoFutebol
jogo_futebol = JogoFutebol()

# Exibir as partidas
exibir_partidas()

# Iniciar a janela principal
window.mainloop()
