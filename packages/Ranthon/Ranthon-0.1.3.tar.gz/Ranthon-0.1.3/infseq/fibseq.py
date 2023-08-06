from filelog import Writer
def calfib(loop, log):
    n = 1
    x = 0
    p = x
    if log == True:
        for i in range(loop):
            x = n
            n = (n + p)
            Writer('current', False) >> n
            p = x
            Writer('previos', False) >> p
    else:
        for i in range(loop):
            x = n
            n = (n + p)
            p = x
    return n

def calfiblon():
    n = 1
    x = 0
    p = x
    while True:
        x = n
        n = (n + p)
        Writer('current', False) >> n
        p = x
        Writer('previos', False) >> p
