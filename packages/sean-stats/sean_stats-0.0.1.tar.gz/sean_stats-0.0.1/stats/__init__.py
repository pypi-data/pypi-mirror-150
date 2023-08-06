def avg(work):
    total = 0
    for i in range(len(work)):
        total += work[i]
    out = total / len(work)
    return out
