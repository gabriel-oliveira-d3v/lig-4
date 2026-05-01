import os
import time
import random

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

def get_drop_row(tabuleiro, coluna):
    """Retorna a linha onde a peça cairia na coluna, ou None se cheia."""
    for linha in range(5, -1, -1):
        if tabuleiro[linha][coluna] == ' ':
            return linha
    return None

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

# -------------------------- AI do Bot --------------------------
def bot_move_ganha(tabuleiro, coluna, simbolo):
    """Testa se colocar `simbolo` na `coluna` resulta em vitória."""
    linha = get_drop_row(tabuleiro, coluna)
    if linha is None:
        return False
    # Simula temporariamente
    tabuleiro[linha][coluna] = simbolo
    venceu = verificar_vitoria(tabuleiro, linha, coluna, simbolo)
    tabuleiro[linha][coluna] = ' '
    return venceu

def get_bot_move(tabuleiro, bot_simbolo, humano_simbolo):
    """Escolhe a melhor jogada para o bot:
       1. Se pode vencer imediatamente, joga.
       2. Se pode bloquear vitória do humano, joga.
       3. Caso contrário, escolhe uma coluna válida aleatória (com leve preferência ao centro).
    """
    valid_cols = [c for c in range(7) if coluna_valida(tabuleiro, c)]
    if not valid_cols:
        return None

    # 1. Vitória imediata do bot
    for col in valid_cols:
        if bot_move_ganha(tabuleiro, col, bot_simbolo):
            return col

    # 2. Bloquear vitória do humano
    for col in valid_cols:
        if bot_move_ganha(tabuleiro, col, humano_simbolo):
            return col

    # 3. Jogada aleatória (centro tem mais chances de construir combos)
    #    Atribui pesos: colunas 3,2,4,1,5,0,6 (centro > laterais)
    pesos = [1, 2, 3, 4, 3, 2, 1]  # col 0..6
    opcoes = []
    for col in valid_cols:
        opcoes.extend([col] * pesos[col])
    return random.choice(opcoes) if opcoes else random.choice(valid_cols)

# -------------------------- Modo de Jogo: 2 Jogadores --------------------------
def executar_jogo(short1, short2, simbolos):
    """Runs one game for two human players."""
    tabuleiro = criar_tabuleiro()
    jogador_atual = 0  # 0 -> player1, 1 -> player2

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("      LIGUE-4 (CONNECT FOUR)")
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
            update_score(nome_curto)
            input("\nPressione ENTER para continuar...")
            break

        if tabuleiro_cheio(tabuleiro):
            print("\n🤝 EMPATE! Ninguém ganha pontos.")
            input("\nPressione ENTER para continuar...")
            break

        jogador_atual = 1 - jogador_atual

# -------------------------- Modo de Jogo: Humano vs Bot --------------------------
def executar_jogo_bot(humano_apelido, humano_simbolo, bot_simbolo):
    """Runs one game: Human vs Bot. Bot's wins are NOT added to ranking."""
    tabuleiro = criar_tabuleiro()
    jogador_atual = 0  # 0 = humano, 1 = bot
    nome_bot = "🤖 BOT"

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("      LIGUE-4 (CONNECT FOUR)")
        print(f"  {humano_apelido}: ●          {nome_bot}: ○")
        print("=" * 40)
        exibir_tabuleiro(tabuleiro)

        if jogador_atual == 0:  # Humano
            print(f"Vez de {humano_apelido} ({humano_simbolo})")
            while True:
                try:
                    coluna = int(input("Coluna (1 a 7): ")) - 1
                    if coluna_valida(tabuleiro, coluna):
                        break
                    print("⚠️ Coluna inválida ou cheia!")
                except ValueError:
                    print("⚠️ Digite um número entre 1 e 7.")
            linha = animar_ficha(tabuleiro, coluna, humano_simbolo)

            if verificar_vitoria(tabuleiro, linha, coluna, humano_simbolo):
                print(f"\n{'=' * 40}")
                print(f"🎉 PARABÉNS! {humano_apelido} VENCEU! 🎉")
                print(f"{'=' * 40}")
                update_score(humano_apelido)   # só humano ganha pontos
                input("\nPressione ENTER para continuar...")
                break
        else:  # Bot
            print(f"🤖 {nome_bot} está pensando...")
            time.sleep(0.8)  # pausa para dar sensação de "pensamento"
            coluna = get_bot_move(tabuleiro, bot_simbolo, humano_simbolo)
            if coluna is None:
                # não deveria acontecer se houver jogadas válidas
                print("⚠️ Bot não encontrou jogada!")
                break
            linha = animar_ficha(tabuleiro, coluna, bot_simbolo)

            if verificar_vitoria(tabuleiro, linha, coluna, bot_simbolo):
                print(f"\n{'=' * 40}")
                print(f"💀 {nome_bot} VENCEU! Que pena... 💀")
                print(f"{'=' * 40}")
                print("(O bot NÃO entra no ranking.)")
                input("\nPressione ENTER para continuar...")
                break

        if tabuleiro_cheio(tabuleiro):
            print("\n🤝 EMPATE! Ninguém ganha pontos.")
            input("\nPressione ENTER para continuar...")
            break

        jogador_atual = 1 - jogador_atual

# -------------------------- Menu Principal --------------------------
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print("       CONNECT FOUR - LIGUE-4")
        print("=" * 40)
        print("  1. Jogar (2 jogadores)")
        print("  2. Jogar contra o Bot")
        print("  3. Ver Ranking")
        print("  4. Sair")
        print("=" * 40)
        opcao = input("Escolha: ")

        if opcao == "1":
            print("\n--- NOVO JOGO (2 JOGADORES) ---")
            short1 = input("Apelido Jogador 1 (●) [max 3 letras]: ").strip().upper()
            while len(short1) == 0 or len(short1) > 3:
                short1 = input("Máximo 3 caracteres. Digite novamente: ").strip().upper()
            short2 = input("Apelido Jogador 2 (○) [max 3 letras]: ").strip().upper()
            while len(short2) == 0 or len(short2) > 3:
                short2 = input("Máximo 3 caracteres. Digite novamente: ").strip().upper()

            simbolos = ['●', '○']
            executar_jogo(short1, short2, simbolos)

        elif opcao == "2":
            print("\n--- MODO CONTRA O BOT ---")
            humano = input("Seu apelido (max 3 letras): ").strip().upper()
            while len(humano) == 0 or len(humano) > 3:
                humano = input("Máximo 3 caracteres. Digite novamente: ").strip().upper()
            print("\nVocê joga com ● . O bot joga com ○ .")
            input("Pressione ENTER para iniciar...")
            # Humano sempre começa com ●, bot com ○
            executar_jogo_bot(humano, '●', '○')

        elif opcao == "3":
            display_ranking()
            input("Pressione ENTER para voltar...")

        elif opcao == "4":
            print("Até logo!")
            break
        else:
            print("Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    main()