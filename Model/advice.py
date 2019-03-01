def calculateScore(speed, stop_time, wrong_time, S):
    score = 0
    score = score + 50 - stop_time*2 - wrong_time
    score += (1 - abs(150 - speed)/170) * 25
    score += (25 - S * 2.2)
    return score