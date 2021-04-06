from timeout import timerbot


def funcion3(text:str):
    print("hola cada "+text)


tbot1 = timerbot()
tbot1.add_interval(3,funcion3,"3 minutos","tempo 1")
tbot1.add_interval(10,funcion3,"10 minutos","tempo 2")
tbot1.add_timeout(5,funcion3,"5 minutos","tempo 3")

tbot1.enableInterval("tempo 1")
tbot1.enableInterval("tempo 2")
tbot1.enableTimeout("tempo 3")

tbot1.steamOFF()

print("datos de tempo 1: ")
print("================")
print("funcion: " + str(tbot1.getFuncInterval("tempo 1")))
print("cuenta: " + str(tbot1.getCountInterval("tempo 1")))
print("final cuenta: " + str(tbot1.getTimeInterval("tempo 1")))
print("nombre: " + str(tbot1.getNameInterval("tempo 1")))

print("\n\ndatos de tempo 2: ")
print("================")
print("funcion: " + str(tbot1.getFuncInterval("tempo 2")))
print("cuenta: " + str(tbot1.getCountInterval("tempo 2")))
print("final cuenta: " + str(tbot1.getTimeInterval("tempo 2")))
print("nombre: " + str(tbot1.getNameInterval("tempo 2")))

print("\n\ndatos de tempo 3: ")
print("================")
print("funcion: " + str(tbot1.getFuncTimeout("tempo 3")))
print("cuenta: " + str(tbot1.getCountTimeout("tempo 3")))
print("final cuenta: " + str(tbot1.getTimeTimeout("tempo 3")))
print("nombre: " + str(tbot1.getNameTimeout("tempo 3")))

tbot1.steamON()