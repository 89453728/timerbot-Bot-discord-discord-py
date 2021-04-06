
def loadTimerbots(file_name):
    f = open(file_name,"r")
    bruteText = f.read()
    f.close()
    
    tmp = bruteText.split("\n")
    return tmp