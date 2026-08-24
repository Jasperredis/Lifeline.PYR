# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev
# This is FREE SOFTWARE. See the LICENSE-GPL file for more information.

from mod.core.save import save_data
import mod.etc.magicvars as mgv
from mod.stage.game.ui import draw_ui, draw_ui_before_entities
from mod.stage.game.spawns import do_spawns
from mod.stage.game.core_updates import do_updates
from mod.stage.game.inputx import take_input
from mod.stage.game.pause import do_pause
from mod.stage.game import gamedata as gd
from mod.stage.game import player

started = False


def act(mode, rsurface, keys, tick, mx, my, mb):
    global started

    # Initialise gamedata
    if not started:
        gd.init(tick, mode)
        started = True

    # Act
    rsurface.blit(mgv.bgs[str(save_data['bg'])], (0, 0))
    draw_ui_before_entities(mode, rsurface)
    player.make_player(rsurface, gd.game, tick, keys)
    draw_ui(rsurface, gd.game, tick, keys)
    gd.game = do_spawns(rsurface, player.plr, gd.game, tick)

    # inputx
    inputx_result = take_input(mode, gd.game, keys, tick, mx, my, mb)
    gd.game = inputx_result[0]
    if inputx_result[1] == "restart":
        gd.init(tick, mode)

    gd.game = do_updates(rsurface, tick, gd.game)

    # Pause and determine return
    if not gd.game.paused:
        return None

    final_return = do_pause(rsurface, keys, tick, gd.game, mx, my, mb)

    if isinstance(final_return, gd.Game):
        gd.game = final_return
        return None
    elif final_return == "restart":
        gd.init(tick, mode)
        return None
    elif final_return == "game":
        return None
    else:
        started = False
        return final_return
