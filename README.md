DGPS mittels Thingstream Service - sollte Kompass ersetzen und Koordinate von Schacht verifizieren

#
            clientcompass.publish("/CS1/Orientierung", str(round(180-angle,2)))
            clientcompass.publish("/CS1/Baseline", str(int(basislänge*100)))
            clientcompass.publish("/CS1/GK", str(CSRW)+' '+ str(CSHW))
