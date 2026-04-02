import os

def criar_tabuleiro():
    """Cria e retorna um tabuleiro vazio 6x7 (6 linhas, 7 colunas)."""
    # Cada célula é um espaço ' ' representando posição vazia
    return [[' ' for _ in range(7)] for _ in range(6)]

def exibir_tabuleiro(tabuleiro):
    """Exibe o tabuleiro no console com numeração das colunas."""
    # Limpa a tela para melhor visualização (opcional, comente se não quiser)
    # os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n  " + "=" * 29)  # linha superior decorativa
    for i, linha in enumerate(tabuleiro):
        print("  |", end=" ")
        for celula in linha:
            print(celula, end=" | ")
        print(f"\n  +" + "---+" * 7)
    
    # Numeração das colunas (1 a 7)
    print("    1   2   3   4   5   6   7\n")

def soltar_ficha(tabuleiro, coluna, simbolo):
    """
    Solta a ficha na coluna escolhida (0-indexada).
    Retorna a linha onde a ficha caiu, ou None se a coluna estiver cheia.
    """
    # Percorre as linhas de baixo para cima (índice 5 é a base)
    for linha in range(5, -1, -1):
        if tabuleiro[linha][coluna] == ' ':
            tabuleiro[linha][coluna] = simbolo
            return linha
    return None  # Coluna cheia

def coluna_valida(tabuleiro, coluna):
    """Verifica se a coluna (0-indexada) existe e ainda tem espaço."""
    if 0 <= coluna < 7:
        return tabuleiro[0][coluna] == ' '  # topo vazio → espaço disponível
    return False

def tabuleiro_cheio(tabuleiro):
    """Retorna True se não houver mais espaços vazios no tabuleiro."""
    return all(tabuleiro[0][col] != ' ' for col in range(7))

def verificar_vitoria(tabuleiro, linha, coluna, simbolo):
    """
    Verifica se a última jogada (linha, coluna) com o símbolo dado
    formou uma sequência de quatro símbolos iguais.
    """
    # Função auxiliar para contar peças consecutivas em uma direção (dl, dc)
    def contar_direcao(dl, dc):
        cont = 0
        r, c = linha + dl, coluna + dc
        while 0 <= r < 6 and 0 <= c < 7 and tabuleiro[r][c] == simbolo:
            cont += 1
            r += dl
            c += dc
        return cont

    # Verifica horizontal: esquerda + direita (+1 da própria peça)
    total = 1 + contar_direcao(0, 1) + contar_direcao(0, -1)
    if total >= 4:
        return True

    # Verifica vertical: cima + baixo
    total = 1 + contar_direcao(1, 0) + contar_direcao(-1, 0)
    if total >= 4:
        return True

    # Verifica diagonal principal (↘): noroeste + sudeste
    total = 1 + contar_direcao(1, 1) + contar_direcao(-1, -1)
    if total >= 4:
        return True

    # Verifica diagonal secundária (↙): nordeste + sudoeste
    total = 1 + contar_direcao(1, -1) + contar_direcao(-1, 1)
    if total >= 4:
        return True

    return False

def executar_jogo():
    """Função principal que controla o fluxo do jogo."""
    # Inicializa o tabuleiro e os jogadores
    tabuleiro = criar_tabuleiro()
    # Símbolos: Jogador 1 = '●', Jogador 2 = '○'
    jogadores = ['●', '○']
    jogador_atual = 0  # índice 0 = Jogador 1

    print("=" * 40)
    print("Bem-vindo ao Ligue‑4 (Connect Four)!")
    print("Jogador 1: ●   Jogador 2: ○")
    print("=" * 40)

    while True:
        exibir_tabuleiro(tabuleiro)
        simbolo = jogadores[jogador_atual]
        print(f"Vez do jogador {jogador_atual + 1} ({simbolo})")

        # Loop para obter uma coluna válida
        while True:
            try:
                coluna = int(input("Escolha uma coluna (1 a 7): ")) - 1
                if coluna_valida(tabuleiro, coluna):
                    break
                else:
                    print("Coluna inválida ou cheia. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número entre 1 e 7.")

        # Solta a ficha e obtém a linha onde caiu
        linha = soltar_ficha(tabuleiro, coluna, simbolo)

        # Verifica vitória
        if verificar_vitoria(tabuleiro, linha, coluna, simbolo):
            exibir_tabuleiro(tabuleiro)
            print(f"\n{'=' * 40}")
            print(f"🎉 PARABÉNS! Jogador {jogador_atual + 1} ({simbolo}) VENCEU! 🎉")
            print(f"{'=' * 40}")
            break

        # Verifica empate (tabuleiro completamente cheio)
        if tabuleiro_cheio(tabuleiro):
            exibir_tabuleiro(tabuleiro)
            print("\n" + "=" * 40)
            print("EMPATE! O tabuleiro está completamente preenchido.")
            print("=" * 40)
            break

        # Alterna o jogador
        jogador_atual = 1 - jogador_atual

if __name__ == "__main__":
    executar_jogo()