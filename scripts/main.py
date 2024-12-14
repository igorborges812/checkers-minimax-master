from typing import Optional, Union
import random
import os

import pygame
from pygame.event import EventType

from checkers import CheckerBoard, Player, PosType, BoardType
from minimax import Minimax


# Definindo o tamanho da janela e as cores usadas no jogo
WIN_SIZE = (WIDTH, HEIGHT) = (600, 600)
TILE_SIZE = (WIN_SIZE[0] // 10, WIN_SIZE[1] // 10)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
BOARD_COLOR = [WHITE, BLACK]
PLAYER_COLOR = [RED, BLUE]


def draw_board(surface: pygame.Surface, turn: int) -> None:
    surface.fill(BOARD_COLOR[0])  # Preenche toda a superfície da janela com branco
    for i in range(0, WIN_SIZE[0], 2 * TILE_SIZE[0]):
        for j in range(0, WIN_SIZE[1], 2 * TILE_SIZE[1]):
            pygame.draw.rect(
                surface, BOARD_COLOR[1],
                (i, j, TILE_SIZE[0], TILE_SIZE[1]),
            )
    for i in range(TILE_SIZE[0], WIN_SIZE[0], 2 * TILE_SIZE[0]):
        for j in range(TILE_SIZE[1], WIN_SIZE[1], 2 * TILE_SIZE[1]):
            pygame.draw.rect(
                surface, BOARD_COLOR[1],
                (i, j, TILE_SIZE[0], TILE_SIZE[1]),
            )
    pygame.draw.rect(surface, PLAYER_COLOR[turn - 1], ((0, 0), WIN_SIZE), 3)  # Desenha o contorno com a cor do jogador


def draw_selected(
    surface: pygame.Surface, posgrid: PosType, color: str
) -> None:
    pygame.draw.rect(
        surface,
        color,
        (
            posgrid[0] * TILE_SIZE[0], posgrid[1] * TILE_SIZE[1],
            TILE_SIZE[0], TILE_SIZE[1],
        ),
        3
    )


def draw_player(surface: pygame.Surface, player: Player) -> None:
    for i in range(10):
        for j in range(10):  # Para cada quadrado nas direções x e y
            if player.pos_pieces[i, j] == 1:  # Se a peça do jogador estiver no quadrado selecionado
                centre = (
                    round(i * TILE_SIZE[0] + (TILE_SIZE[0] / 2)),
                    round(j * TILE_SIZE[1] + (TILE_SIZE[1] / 2)),
                )
                radius = round(TILE_SIZE[0] / 2 * (9 / 10))
                pygame.draw.circle(surface, PLAYER_COLOR[player.ply - 1], centre, radius)
            elif player.pos_pieces[i, j] == 2:
                centre = (
                    round(i * TILE_SIZE[0] + (TILE_SIZE[0] / 2)),
                    round(j * TILE_SIZE[1] + (TILE_SIZE[1] / 2)),
                )
                radius = round(TILE_SIZE[0] / 2 * (9 / 10))
                pygame.draw.circle(surface, PLAYER_COLOR[player.ply - 1], centre, radius)
                invcol = (
                    255 - PLAYER_COLOR[player.ply - 1][0],
                    255 - PLAYER_COLOR[player.ply - 1][1],
                    255 - PLAYER_COLOR[player.ply - 1][2],
                )
                radius = round(TILE_SIZE[0] / 2 * (2 / 10))
                pygame.draw.circle(surface, invcol, centre, radius)
                pygame.draw.circle(
                    surface, invcol, (centre[0] + 10, centre[1]), radius
                )
                pygame.draw.circle(
                    surface, invcol, (centre[0], centre[1] + 10), radius
                )
                pygame.draw.circle(
                    surface, invcol, (centre[0] - 10, centre[1]), radius
                )
                pygame.draw.circle(
                    surface, invcol, (centre[0], centre[1] - 10), radius
                )


def select_piece(
    player: Player,
    selected: Optional[PosType],
    moveto: Optional[PosType],
    event: EventType
) -> Union[bool, PosType]:
    pos = event.dict["pos"]  # Extrai a posição do clique do mouse
    posgrid = (pos[0] // TILE_SIZE[0], pos[1] // TILE_SIZE[1])  # Calcula a posição no tabuleiro a partir do clique
    if (selected is None) and (moveto is None):  # Se nenhuma peça está selecionada e não há movimento pendente
        if player.pos_pieces[posgrid]:  # Se existe uma peça do jogador na posição clicada
            return posgrid
        return False
    if (selected is not None) and (moveto is None):
        return posgrid
    return False


def count_pieces(player: Player) -> tuple:
    pieces_left = 0
    pieces_eaten = 0
    queens = 0
    for i in range(10):
        for j in range(10):
            if player.pos_pieces[i, j] == 1:
                pieces_left += 1
            elif player.pos_pieces[i, j] == 2:
                pieces_left += 1
                queens += 1
    return pieces_left, pieces_eaten, queens


def copy_board(board: BoardType) -> BoardType:
    copy: BoardType = [[0 for _ in range(10)] for _ in range(10)]  # Cria uma nova matriz 10x10 com 0s
    for i in range(10):
        for j in range(10):
            copy[i][j] = board[i][j]  # Copia o conteúdo do tabuleiro original para o novo
    return copy  # Retorna o tabuleiro copiado


def clear() -> None:
    os.system("cls")  # Limpa o terminal


def print_score(ply1: Player, ply2: Player) -> None:
    ply1_pieces, ply1_eaten, ply1_queens = count_pieces(ply1)
    ply2_pieces, ply2_eaten, ply2_queens = count_pieces(ply2)

    score_str = "\n"
    score_str += "+------------------------------+\n"
    score_str += "|         SCOREBOARD          |\n"
    score_str += "|-----------------------------|\n"
    score_str += f"| Player 1 (Vermelho):         |\n"
    score_str += f"|  - Peças restantes: {ply1_pieces:>2}        |\n"
    score_str += f"|  - Peças comidas:   {ply1_eaten:>2}        |\n"
    score_str += f"|  - Rainhas:         {ply1_queens:>2}        |\n"
    score_str += "|-----------------------------|\n"
    score_str += f"| Player 2 (Azul):            |\n"
    score_str += f"|  - Peças restantes: {ply2_pieces:>2}        |\n"
    score_str += f"|  - Peças comidas:   {ply2_eaten:>2}        |\n"
    score_str += f"|  - Rainhas:         {ply2_queens:>2}        |\n"
    score_str += "|-----------------------------|\n"
    score_str += "+------------------------------+\n"
    print(score_str)
    if ply1_eaten == 15:
        print("PLAYER 1 (Vermelho) VENCEU!")
    elif ply2_eaten == 15:
        print("PLAYER 2 (Azul) VENCEU!")


if __name__ == "__main__":  # O código começa aqui

    pygame.display.init()  # Inicializa o módulo de exibição do Pygame
    pygame.display.set_caption("Checker Minimax")  # Define o título da janela
    surface = pygame.display.set_mode(WIN_SIZE)  # Cria a janela do jogo
    clock = pygame.time.Clock()

    gameboard = CheckerBoard()  # Cria a instância da classe CheckerBoard
    player1 = Player(1)  # Cria a instância do jogador 1 (vermelho)
    player2 = Player(2)  # Cria a instância do jogador 2 (azul)
    ai = Minimax(ply_num=1)  # Cria a instância do Minimax (IA)

    gameboard.update_board(player1.pos_pieces, player2.pos_pieces)  # Atualiza o tabuleiro com as peças
    board = gameboard.board

    clear()  # Limpa o terminal
    print(gameboard)  # Imprime o tabuleiro atual

    selected = None
    moveto = None
    movedfrom = (100, 100)
    lastmove = None
    taken = False
    turn = random.choice([1, 2])  # Define aleatoriamente quem começa

    print_score(player1, player2)
    print(f"Player{turn}'s turn\n. . . . . . . .")

    while True:  # Loop principal do jogo
        draw_board(surface, turn)  # Desenha o tabuleiro na superfície do Pygame
        draw_player(surface, player1)  # Desenha as peças do jogador 1
        draw_player(surface, player2)  # Desenha as peças do jogador 2
        player = player1 if (turn == 1) else player2  # Define o jogador atual

        if selected and player.pos_pieces[selected]:  # Se o jogador selecionou uma peça válida
            draw_selected(surface, selected, PLAYER_COLOR[player.ply - 1])  # Desenha o contorno em torno da peça selecionada
            for i in range(0, 10):
                for j in range(0, 10):
                    if player2.move(selected, (i, j), gameboard.board, taken, lastmove, movedfrom, False):
                        draw_selected(surface, (i, j), GRAY)

        # Detecta evento de clique do mouse
        for event in pygame.event.get():  # Itera sobre os eventos detectados
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected:
                    tmp = select_piece(player, selected, moveto, event)
                    if tmp != selected:
                        moveto = tmp  # Se a peça foi movida, atualiza a posição
                else:
                    selected = select_piece(player, selected, moveto, event)
                    movedfrom = selected  # A posição de origem é a peça selecionada

        # Turno da IA
        if player == player1:  # Se é o turno da IA
            board = copy_board(gameboard.board)  # Faz uma cópia do tabuleiro
            try:  # Tenta realizar o movimento da IA
                _, ai_move = ai.minimax(board, 100, True)  # Usa o minimax para encontrar o movimento da IA
                selected, moveto = ai_move
            except TypeError:
                selected = None
                moveto = None  # Reseta o movimento da IA se ocorrer erro

        if moveto is not None:  # Se há um movimento a ser feito
            if player == player1:
                check = "ply1"  # Turno do jogador 1
                tmp = player1.move(selected, moveto, gameboard.board, taken, lastmove, movedfrom, True)  # Realiza o movimento
                player2.update_dead(tmp)  # Atualiza peças comidas, se houver captura
            else:
                check = "ply2"  # Turno do jogador 2
                tmp = player2.move(selected, moveto, gameboard.board, taken, lastmove, movedfrom, True)  # Realiza o movimento
                player1.update_dead(tmp)  # Atualiza peças comidas, se houver captura

            # Atualiza a posição das peças do jogador
            forced_moves_before = player.check_forced_move(gameboard.board)
            gameboard.update_board(player1.pos_pieces, player2.pos_pieces)  # Atualiza o estado do tabuleiro

            if tmp is not False:  # Se o movimento for válido
                taken = True if abs(movedfrom[0] - moveto[0]) == 2 else False
                clear()  # Limpa o terminal
                old_turn = turn  # Armazena o turno anterior
                turn = 1 if (turn == 2) else 2  # Troca de turno
                if isinstance(tmp, tuple) and player.has_forced_moves(gameboard.board):  # Verifica se há movimentos forçados
                    for move in forced_moves_before:
                        if move[0] == moveto:
                            turn = old_turn  # Mantém o mesmo turno se houver movimento forçado
                            break
                taken = False if turn != old_turn else taken  # Reseta o flag de captura
                if old_turn != turn:
                    print(f"Player{turn}'s turn\n. . . . . . . .")
                    old_turn = turn
                print_score(player1, player2)

                lastmove = moveto  # Define a última posição de movimento

            moveto = None
            selected = None  # Prepara para o próximo turno

        pygame.display.flip()