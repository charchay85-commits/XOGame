import maya.cmds as cmds
import xo5tool.xo5Core as core
import importlib
import os, random
importlib.reload(core)

BOARD_SIZE = 5
buttons = []
header_img = None

# 🖼 Path รูปภาพ
ICON_PATH = os.path.join(cmds.internalVar(userScriptDir=True), "xo5tool/icons")
IMG_X = os.path.join(ICON_PATH, "x_icon.png")
IMG_O = os.path.join(ICON_PATH, "o_icon.png")
IMG_BLANK = os.path.join(ICON_PATH, "empty_icon.png")

# Header images
HEADER_START = os.path.join(ICON_PATH, "header_start.png")
HEADER_PLAY = os.path.join(ICON_PATH, "header_play.png")
HEADER_WIN = os.path.join(ICON_PATH, "header_win.png")
HEADER_LOSE = os.path.join(ICON_PATH, "header_lose.png")

def run():
    global buttons, header_img
    buttons = []

    if cmds.window('xo5Game', exists=True):
        cmds.deleteUI('xo5Game')

    window = cmds.window(
        'xo5Game',
        title='XO 5x5 Game (vs AI)',
        sizeable=False,
        minimizeButton=False,
        maximizeButton=False,
        backgroundColor=(1, 1, 1)
    )

    cmds.columnLayout(adj=True, bgc=(1, 1, 1))
    header_img = cmds.image(image=HEADER_START, w=288, h=160)

    # 🎮 กระดาน
    for r in range(BOARD_SIZE):
        cmds.rowLayout(numberOfColumns=BOARD_SIZE, bgc=(1, 1, 1))
        row_btns = []
        for c in range(BOARD_SIZE):
            b = cmds.iconTextButton(
                style='iconOnly',
                image1=IMG_BLANK,
                w=55, h=55,
                bgc=(0.9, 0.9, 0.9),
                command=lambda *args, r=r, c=c: on_player_move(r, c)
            )
            row_btns.append(b)
        buttons.append(row_btns)
        cmds.setParent('..')

    cmds.separator(h=10, style='none')
    cmds.button(label='🔄 Reset Game', h=40, bgc=(0.95, 0.8, 0.25), command=lambda *args: reset_game())

    cmds.showWindow(window)
    cmds.window(window, e=True, widthHeight=(288, 500))

    core.reset_board(BOARD_SIZE)


def on_player_move(r, c):
    if not core.valid_move(r, c):
        return

    cmds.image(header_img, e=True, image=HEADER_PLAY)
    cmds.refresh(force=True)

    cmds.iconTextButton(buttons[r][c], e=True, image1=IMG_X)
    core.place_piece(r, c, 'X')

    if core.check_winner('X'):
        safe_update_header(HEADER_WIN, '🎉 คุณชนะ!')
        return

    ai_move()


def ai_move():
    if random.random() < 0.8:
        move = random_ai_move()
    else:
        move = core.smart_ai_move()

    if not move:
        safe_update_header(HEADER_WIN, '🎉 คุณชนะ!')
        return

    r, c = move
    cmds.iconTextButton(buttons[r][c], e=True, image1=IMG_O)
    core.place_piece(r, c, 'O')

    if core.check_winner('O'):
        safe_update_header(HEADER_LOSE, '💀 AI ชนะ!')


def random_ai_move():
    empty_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if core.valid_move(r, c)]
    return random.choice(empty_cells) if empty_cells else None


# 🪄 อัปเดต header แล้วดีเลย์ให้ Maya วาดจริง ก่อนขึ้น dialog
def safe_update_header(header_path, message):
    cmds.image(header_img, e=True, image=header_path)
    cmds.refresh(force=True)
    # ✅ หน่วงนิดหนึ่งให้ Maya ได้ render ภาพจริงก่อน
    cmds.evalDeferred(lambda: show_result_dialog(message), lowestPriority=True)


def show_result_dialog(message):
    cmds.refresh(force=True)
    result = cmds.confirmDialog(title='Result', message=message, button=['ตกลง'])
    if result == 'ตกลง':
        reset_game()


def reset_game():
    core.reset_board(BOARD_SIZE)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cmds.iconTextButton(buttons[r][c], e=True, image1=IMG_BLANK)
    cmds.image(header_img, e=True, image=HEADER_START)
    cmds.refresh(force=True)

