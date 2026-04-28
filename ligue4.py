import os
import time

# -------------------------- Ranking Functions --------------------------
SCORE_FILE = "ranking.txt"

def load_scores():
    """Load scores from file into a dictionary {short_name: wins}."""
    scores = {}
    if not os.path.exists(SCORE_FILE):
        return scores
    with open(SCORE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    name, wins = line.rsplit(":", 1)
                    scores[name] = int(wins)
                except ValueError:
                    continue
    return scores

def save_scores(scores):
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        for name, wins in scores.items():
            f.write(f"{name}:{wins}\n")

def update_score(short_name, increment=1):
    scores = load_scores()
    scores[short_name] = scores.get(short_name, 0) + increment
    save_scores(scores)

def display_ranking():
    """Show ranking with short names (max 3 chars each)."""
    scores = load_scores()
    if not scores:
        print("\n📭 Nenhuma pontuação registrada ainda.\n")
        return

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print("\n" + "=" * 40)
    print("         🏆 RANKING DE JOGADORES 🏆")
    print("=" * 40)
    for i, (name, wins) in enumerate(sorted_scores, 1):
        # name já é o apelido curto (ex: "A", "JOA", "B")
        print(f"  {i}. {name:3s} → {wins} vitória(s)")
    print("=" * 40 + "\n")

# -------------------------- Game Core --------------------------
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
    return 0 <= coluna < 7 and tabuleiro[0][coluna] == ' '

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

    for dl, dc in [(0,1), (1,0), (1,1), (1,-1)]:
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
        print("      Jogador 1: ●   Jogador 2: ○")
        print("=" * 40)
        exibir_tabuleiro(tabuleiro)
        if linha_atual < linha_destino:
            time.sleep(0.1)
            tabuleiro[linha_atual][coluna] = ' '
    return linha_destino

def executar_jogo(short1, short2, simbolos):
    """Runs one game. short1, short2 are short names (e.g., 'A', 'B')."""
    tabuleiro = criar_tabuleiro()
    jogador_atual = 0  # 0 -> player1, 1 -> player2

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("      LIGUE-4 (CONNECT FOUR)")
        # Mostra os apelidos curtos na tela de jogo
        print(f"  {short1}: ●          {short2}: ○")
        print("=" * 40)
        exibir_tabuleiro(tabuleiro)

        nome_curto = short1 if jogador_atual == 0 else short2
        simbolo = simbolos[jogador_atual]
        print(f"Vez de {nome_curto} ({simbolo})")

        while True:
            try:
                coluna = int(input("Coluna (1 a 7): ")) - 1
                if coluna_valida(tabuleiro, coluna):
                    break
                print("⚠️ Coluna inválida ou cheia!")
            except ValueError:
                print("⚠️ Digite um número entre 1 e 7.")

        linha = animar_ficha(tabuleiro, coluna, simbolo)

        if verificar_vitoria(tabuleiro, linha, coluna, simbolo):
            print(f"\n{'=' * 40}")
            print(f"🎉 PARABÉNS! {nome_curto} VENCEU! 🎉")
            print(f"{'=' * 40}")
            update_score(nome_curto)   # salva ranking com apelido curto
            input("\nPressione ENTER para continuar...")
            break

        if tabuleiro_cheio(tabuleiro):
            print("\n🤝 EMPATE! Ninguém ganha pontos.")
            input("\nPressione ENTER para continuar...")
            break

        jogador_atual = 1 - jogador_atual

# -------------------------- Main Menu --------------------------
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("       CONNECT FOUR - LIGUE-4")
        print("=" * 40)
        print("  1. Jogar")
        print("  2. Ver Ranking")
        print("  3. Sair")
        print("=" * 40)
        opcao = input("Escolha: ")

        if opcao == "1":
            print("\n--- NOVO JOGO (estilo fliperama) ---")
            # Pede apelidos curtos (máx 3 caracteres)
            short1 = input("Apelido Jogador 1 (●) [max 3 letras]: ").strip().upper()
            while len(short1) == 0 or len(short1) > 3:
                short1 = input("Máximo 3 caracteres. Digite novamente: ").strip().upper()
            short2 = input("Apelido Jogador 2 (○) [max 3 letras]: ").strip().upper()
            while len(short2) == 0 or len(short2) > 3:
                short2 = input("Máximo 3 caracteres. Digite novamente: ").strip().upper()

            simbolos = ['●', '○']
            executar_jogo(short1, short2, simbolos)

        elif opcao == "2":
            display_ranking()
            input("Pressione ENTER para voltar...")

        elif opcao == "3":
            print("Até logo!")
            break
        else:
            print("Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    main()