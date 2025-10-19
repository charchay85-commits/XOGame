import maya.cmds as cmds
import xo5tool.xo5Core as core
import importlib
importlib.reload(core)

BOARD_SIZE = 5
buttons = []

def run():
    if cmds.window('xo5Game', exists=True):
        cmds.deleteUI('xo5Game')

    # ✅ เพิ่มการล็อกขนาดหน้าต่าง
    window = cmds.window(
        'xo5Game',
        title='XO 5x5 Game (vs AI)',
        widthHeight=(320, 360),
        sizeable=False,          # ❌ ปิดการย่อ/ขยาย
        minimizeButton=False,    # ❌ ปิดปุ่มย่อ
        maximizeButton=False     # ❌ ปิดปุ่มขยาย
    )

    cmds.columnLayout(adj=True)

    for r in range(BOARD_SIZE):
        cmds.rowLayout(numberOfColumns=BOARD_SIZE, adj=True)
        row_btns = []
        for c in range(BOARD_SIZE):
            b = cmds.button(
                label='-',
                w=50,
                h=50,
                command=lambda x, r=r, c=c: on_player_move(r, c)
            )
            row_btns.append(b)
        buttons.append(row_btns)
        cmds.setParent('..')

    cmds.separator(h=10, style='none')
    cmds.button(label='🔄 Reset', h=35, command=lambda x: reset_game())

    cmds.showWindow(window)

    core.reset_board(BOARD_SIZE)
    reset_scene()


def on_player_move(r, c):
    if not core.valid_move(r, c):
        return

    cmds.button(buttons[r][c], e=True, label='X', bgc=(0.9, 0.3, 0.3))
    core.place_piece(r, c, 'X')
    create_piece(r, c, 'X')

    if core.check_winner('X'):
        cmds.confirmDialog(title='Result', message='🎉 คุณชนะ!')
        clear_viewport()  # ลบ object ทั้งหมดบน viewport
        return

    ai_move()


def ai_move():
    move = core.smart_ai_move()
    if not move:
        cmds.confirmDialog(title='Result', message='😐 เสมอ!')
        clear_viewport()
        return

    r, c = move
    cmds.button(buttons[r][c], e=True, label='O', bgc=(0.3, 0.55, 1))
    core.place_piece(r, c, 'O')
    create_piece(r, c, 'O')

    if core.check_winner('O'):
        cmds.confirmDialog(title='Result', message='💀 AI ชนะ!')
        clear_viewport()



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

def clear_viewport():
    # ดึงทุก object transform ทั้งหมด
    all_objs = cmds.ls(type='transform')
    if all_objs:
        cmds.delete(all_objs)


def reset_game():
    core.reset_board(BOARD_SIZE)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cmds.button(buttons[r][c], e=True, label='-', bgc=(0.27, 0.27, 0.27))
    clear_viewport()  # ลบ object ทั้งหมดบน viewport

def reset_scene():
    for obj in cmds.ls('X_*', 'O_*'):
        cmds.delete(obj)
