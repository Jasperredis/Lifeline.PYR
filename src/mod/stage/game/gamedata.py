# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from dataclasses import dataclass, field
from mod.core.save import save_data
from mod.stage.game import constants


@dataclass
class Game:
    start_tick: int
    initial_high: int
    mode: str
    plrx: int = 126
    plry: int = 64
    life: int = 5
    last_loss: int = 0
    enemies: list = field(default_factory=list)
    heals: list = field(default_factory=list)
    paused: bool = False
    sel: bool = 1
    lkpt: int = 0
    iframe: int = 0
    last_iframe_time: int = 0
    score: int = 0
    gameover: bool = False
    jumping: bool = False
    last_jump: int = -300
    velocity: float = 3
    velocity_y: float = 3
    falls: list = field(default_factory=list)
    dash: int = 106
    lasers: list = field(default_factory=list)
    shown_death_notif: bool = False


def init(tick, mode):
    global game
    constants.do_depend(mode)
    game = Game(tick, save_data["high"], mode)
    save_data["played"] += 1

    # my cat typed the garbled part of the line below
    # print("log init gdata78u9-06=4wsa6.789-0078-95644444444444444444444444444
    # 44444444444444444444x21q   ")
