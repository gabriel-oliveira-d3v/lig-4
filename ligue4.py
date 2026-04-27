import os
import time

def criar_tabuleiro():
    return [[' ' for _ in range(7)] for _ in range(6)]

def exibir_tabuleiro(tabuleiro):
    print("\n  " + "=" * 29)
    for i, linha in enumerate(tabuleiro):
        print("  |", end=" ")
        for celula in linha:
            print(celula, end=" | ")
        print(f"\n  +" + "---+" * 7)
    print("    1   2   3   4   5   6   7\n")

def coluna_valida(tabuleiro, coluna):
    if 0 <= coluna < 7:
        return tabuleiro[0][coluna] == ' '
    return False

def tabuleiro_cheio(tabuleiro):
    return all(tabuleiro[0][col] != ' ' for col in range(7))

def verificar_vitoria(tabuleiro, linha, coluna, simbolo):
    def contar_direcao(dl, dc):
        cont = 0
        r, c = linha + dl, coluna + dc
        while 0 <= r < 6 and 0 <= c < 7 and tabuleiro[r][c] == simbolo:
            cont += 1
            r += dl
            c += dc
        return cont

    direcoes = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dl, dc in direcoes:
        if 1 + contar_direcao(dl, dc) + contar_direcao(-dl, -dc) >= 4:
            return True
    return False

def animar_ficha(tabuleiro, coluna, simbolo):
    linha_destino = -1
    for l in range(5, -1, -1):
        if tabuleiro[l][coluna] == ' ':
            linha_destino = l
            break

    if linha_destino == -1:
        return None

    for linha_atual in range(linha_destino + 1):
        tabuleiro[linha_atual][coluna] = simbolo

        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("      LIGUE-4 (CONNECT FOUR)")
        print(f"      Jogador 1: ●   Jogador 2: ○")
        print("=" * 40)
        exibir_tabuleiro(tabuleiro)

        if linha_atual < linha_destino:
            time.sleep(0.1)
            tabuleiro[linha_atual][coluna] = ' '

    return linha_destino

def executar_jogo():
    tabuleiro = criar_tabuleiro()
    jogadores = ['●', '○']
    jogador_atual = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("=" * 40)
        print("      LIGUE-4 (CONNECT FOUR)")
        print(f"      Jogador 1: ●   Jogador 2: ○")
        print("=" * 40)

        exibir_tabuleiro(tabuleiro)
        simbolo = jogadores[jogador_atual]
        print(f"Vez do jogador {jogador_atual + 1} ({simbolo})")

        while True:
            try:
                entrada = input("Escolha uma coluna (1 a 7): ")
                coluna = int(entrada) - 1
                if coluna_valida(tabuleiro, coluna):
                    break
                else:
                    print("⚠️ Coluna inválida ou cheia!")
            except ValueError:
                print("⚠️ Digite um número válido entre 1 e 7.")

        linha = animar_ficha(tabuleiro, coluna, simbolo)

        if verificar_vitoria(tabuleiro, linha, coluna, simbolo):
            print(f"\n{'=' * 40}")
            print(f"🎉 PARABÉNS! Jogador {jogador_atual + 1} ({simbolo}) VENCEU! 🎉")
            print(f"{'=' * 40}")
            input("\nPressione ENTER para sair...")
            break

        if tabuleiro_cheio(tabuleiro):
            print("\n🤝 EMPATE! O tabuleiro está cheio.")
            input("\nPressione ENTER para sair...")
            break

        jogador_atual = 1 - jogador_atual

if __name__ == "__main__":
    executar_jogo()