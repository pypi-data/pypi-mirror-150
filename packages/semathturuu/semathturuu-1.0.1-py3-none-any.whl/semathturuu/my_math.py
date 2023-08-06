def bukhel(too):
    try:
        return int(too)
    except Exception as ex:
        print('aldaa garlaa ' + ex)


def nemekh(*list):
    sum = 0
    for too in list:
        sum = sum + too
    return sum
