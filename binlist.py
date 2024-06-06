import cli
cli.init()
cache = {}

while True:  # 0000 0000 0000
    for y in range(cli.size.lines):
        if y not in cache:
            cache[y] = bin(y)[2:]
            cache[y] = "0"*(12 - len(cache[y])) + cache[y]
        b = cache[y]
        for i, c in enumerate(b):
            cli.blit_text(i, y, '█', ((255, 0, 0) if c == '0' else (0, 255, 0)))
        cli.blit_text(12, y, str(y))
    cli.update()
    cli.draw()
