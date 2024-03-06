# drawing - 0, test shader - 1, clock - 2, physics - 3, show-replay - 4, animation-maker - 5, pink-pong - 6, lakuar - 7
# roguelike(FIXME) - 8
# tech demo - 9(FIX), boids - 10, doors - 11, sand phys - 12, platformer - 13
prog = 13

match prog:
    case 0:
        import drawing
    case 1:
        import test
    case 2:
        import clock
    case 3:
        import pphysics
    case 4:
        import showreplay
    case 5:
        import anim
    case 6:
        import pong
    case 7:
        import lakuar
    case 8:
        import roguelike
    case 9:
        import tdemo
    case 10:
        import boids
    case 11:
        import doors
    case 12:
        import sandphys
    case 13:
        import platformer
    case _:
        raise ValueError
