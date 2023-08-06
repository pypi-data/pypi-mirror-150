def integer(n):
    try:
        return int(n)
    except:
        print('sadge')
def add(*list):
    sum = 0
    for n in list:
        sum += n
    return sum