class ExpertSystem:
    def __init__(self, fuzzySystem1, fuzzySystem2, fuzzySystem3):
        self.__sys1 = fuzzySystem1
        self.__sys2 = fuzzySystem2
        self.__sys3 = fuzzySystem3
        self.__matriz = [   "AAA",
                            "ABA",
                            "ACB", 
                            "ADB",
                            "BAA",
                            "BBC",
                            "BCC",
                            "BDC", 
                            "CAB", 
                            "CBC", 
                            "CCD",
                            "CDD"]
        
    def getSegment(self, valueInSys1, valueInSys2):

        segment = []

        #Obtenemos los valores de pertenencia en dict
        sys1 = self.__sys1.getMembershipValues()
        sys2 = self.__sys2.getMembershipValues()

        #Creamos la lista de items del dict anterios [(A: [(0, 1), ...])]
        sys1 = list(sys1.items())
        sys2 = list(sys2.items())

        #obtenemos los sets a los que pertenencen los valores buscados 
        #tanto para el sistema 1 como para el sistema 2. Además de los valores 
        #de pertenencia 
        belong1, values1 = self.__lookBelongerSets(sys1, valueInSys1)
        belong2, values2 = self.__lookBelongerSets(sys2, valueInSys2)
        pairs1 = list(zip(belong1, values1))
        pairs2 = list(zip(belong2, values2))

        pairs1 = list(filter(lambda x: x[1] != 0, pairs1))
        pairs2 = list(filter(lambda x: x[1] != 0, pairs2))

        belong1 = list(map(lambda x: x[0], pairs1))
        values1 = list(map(lambda x: x[1], pairs1))

        belong2 = list(map(lambda x: x[0], pairs2))
        values2 = list(map(lambda x: x[0], pairs2))
        print(sys1)
        print(pairs1)
        print(sys2)
        print(pairs2)

        stdo = []
        #obtenemos los resultados en el sistema experto
        for b in belong1:
            for b2 in belong2:
                stdi = b + b2
                #print(list(filter(lambda x: x[:-1] == stdi, self.__matriz)))
                stdo += (list(filter(lambda x: x[:-1] == stdi, self.__matriz)))


        #print(stdo)

        #obtenemos los valores de resultado únicos arrojados por sistema experto.
        outputSets = list(set(map(lambda x: x[-1:], stdo)))
        outputSets = sorted(outputSets)
        #print(outputSets)
        
        for s in outputSets:
            sys1fors = []
            sys2fors = []
            rowSets = list(filter(lambda x: x[-1:] == s, stdo))
            rowSets = list(map(lambda x: x[:-1], rowSets))
            print(rowSets)
            for r in rowSets:
                characters = list(r)
                setSys1 = characters[0]
                setSys2 = characters[1]

                sys1fors += list(filter(lambda x: x[0] == setSys1, pairs1))
                sys2fors += list(filter(lambda x: x[0] == setSys2, pairs2))

            high = sys1fors + sys2fors
            high = list(map(lambda x: x[1], high))

            high = min(high)
            segment.append((s, high))

        #print(segment)

        segmentSets = list(map(lambda x: x[0], segment))
        highs = list(map(lambda x: x[1], segment))

        print(segmentSets)
        print(highs)
        
        return self.__sys3.newSegment(segmentSets, highs)


        
    def __lookBelongerSets(self, set1, value):
        belongs = []
        values = []
        for s in set1:
            if value in list(map(lambda x: x[0], s[1])):
                belongs.append(s[0])
                values.append(list(filter(lambda x: x[0] == value ,s[1]))[0][1])
        return belongs, values