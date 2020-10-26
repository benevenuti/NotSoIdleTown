k = ['K', 'M', 'B', 'T', 'Q', 'S', 'D', 'U', 'O', 'I', 'N', 'F', 'Y',
     'C', 'V', 'L', 'J', 'W', 'P', 'R', '?', 'Z', 'A', 'E', 'G', 'H', 'X', ]
x = ['', '^', 'x']

u = [{v: pow(10, 3 * (e + 1))} for e, v in enumerate([i + d for d in x for i in k])]
