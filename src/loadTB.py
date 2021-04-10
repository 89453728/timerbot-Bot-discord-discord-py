
def loadTimerbots(file_name):
    f = open(file_name,"r")
    bruteText = f.read()
    f.close()
    tmp = []
    
    if (len(tmp) > 1):
        tmp = bruteText.split("\n")
    else:
        tmp = []
    return tmp