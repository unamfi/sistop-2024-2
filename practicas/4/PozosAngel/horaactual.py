import datetime

def decir_la_hora():
    ahora = datetime.datetime.now()
    print("La hora actual es: ", ahora.strftime("%H:%M:%S"))

decir_la_hora()
