def cmdParse(cmd:str):
    parts = cmd.split('>')
    tempoName = parts[0]
    tempoInts = parts[1]
    tempoSound = parts[2]
    tempoInts = tempoInts.split(":")
    tempoints = []
    for i in range(0,len(tempoInts)):
        tempoints.append(int(tempoInts[i]))

    ret = {'name': tempoName, 'temp':tempoints, 'sound':tempoSound}
    return ret 
