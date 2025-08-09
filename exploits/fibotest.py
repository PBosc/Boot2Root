def fun(i):
    if i < 2:
        ret = 1
    else:
        ret = fun(i - 1) + fun(i - 2)
    return ret

print(fun(9))