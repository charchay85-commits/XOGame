import maya.cmds as cmds
import xo5tool.xo5Core as core
import importlib
importlib.reload(core)

BOARD_SIZE = 5
buttons = []

def run():
    if cmds.window('xo5Game', exists=True):
        cmds.deleteUI('xo5Game')

    cmds.window('xo5Game', title='XO 5x5 Game (vs AI)', widthHeight=(320, 360))
    cmds.columnLayout(adj=True)

    for r in range(BOARD_SIZE):
        cmds.rowLayout(numberOfColumns=BOARD_SIZE, adj=True)
        row_btns = []
        for c in range(BOARD_SIZE):
            b = cmds.button(label='-', w=50, h=50, command=lambda x, r=r, c=c: on_player_move(r, c))
            row_btns.append(b)
        buttons.append(row_btns)
        cmds.setParent('..')

    cmds.button(label='🔄 Reset', command=lambda x: reset_game())
    cmds.showWindow('xo5Game')

    core.reset_board(BOARD_SIZE)
    reset_scene()


def on_player_move(r, c):
    if not core.valid_move(r, c):
        return

    cmds.button(buttons[r][c], e=True, label='X', bgc=(1, 0.3, 0.3))
    core.place_piece(r, c, 'X')
    create_piece(r, c, 'X')

    if core.check_winner('X'):
        cmds.confirmDialog(title='Result', message='🎉 คุณชนะ!')
        return

    ai_move()


def ai_move():
    move = core.smart_ai_move()
    if not move:
        cmds.confirmDialog(title='Result', message='😐 เสมอ!')
        return

    r, c = move
    cmds.button(buttons[r][c], e=True, label='O', bgc=(0.4, 0.7, 1))
    core.place_piece(r, c, 'O')
    create_piece(r, c, 'O')

    if core.check_winner('O'):
        cmds.confirmDialog(title='Result', message='💀 AI ชนะ!')


def create_piece(r, c, symbol):
    x = c * 2
    z = -r * 2
    name = f"{symbol}_{r}_{c}"

    if symbol == 'X':
        obj = cmds.polyCube(name=name)[0]
    else:
        obj = cmds.polySphere(name=name)[0]

    cmds.setAttr(f"{obj}.translateX", x)
    cmds.setAttr(f"{obj}.translateZ", z)
    cmds.setAttr(f"{obj}.translateY", 0.5)
    cmds.setAttr(f"{obj}.scale", 0.8, 0.8, 0.8)


def reset_game():
    core.reset_board(BOARD_SIZE)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cmds.button(buttons[r][c], e=True, label='-', bgc=(0.9, 0.9, 0.9))
    reset_scene()


def reset_scene():
    for obj in cmds.ls('X_*', 'O_*'):
        cmds.delete(obj)
