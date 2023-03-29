import matplotlib.pyplot as plt
import random

class FuzzySets:

    def __init__(self, kernels, supports, title, high=[1]):

        #Título general del sistema difuso
        self.__title = title 
        
        # Lista de valores de los núcleos (cresta) del fuzzy set 
        self.__kernels = kernels    

        # Lista de los valores desde donde nace una línea que conforma una 
        # arista del Fuzzy set    
        self.__supports = supports  

        # Las alturas de cada uno de los sets, por defecto [1] pero puedes especificar 
        # la altura para cada uno de los sets del sistema por separado  [1, 0.5, 0.3]
        self.__high = high    

        # Diccionario que almacena los puntos cartesianos necesarios 
        # para dibujar el FuzzySet {'set': [(x, y), (x, y)...]}         
        self.__sets = {}    

        # Diccionario que almacena los valores de pertenencia de cada uno de los 
        # miembros para cada set que conforma el sistema 
        # {'set':[ (m, value),(m, value)...] }            
        self.__memebershipValues = {}

        # Diccionario que almacena los colores con los que se ilustraron los 
        # sets en formato hexadecimal {'set': '#FFFFFF'}
        self.__colors = {}

        # Diccionario que almacena todas la intersecciones que existen en el sistema
        # difuso {'A∩B': [(m, value), (m, value) ...]}
        self.__intersections = {}

        # Diccionario que almacena los puntos necesarios para dibujar las 
        # intersecciones sobre el sistema difuso original {'A∩B': [(x, y), (x, y) ...]}
        self.__drawIntersections = {}

        # Diccionario que almacena los valores de todas las uniones válidas solicitadas 
        # anteriormente por el usuario {'A∪B': [(m, value), (m, value) ...]}
        self.__unions = {}

        # Diccionario que almacena los puntos necesarios para dibujar las 
        # uniones sobre el sistema difuso original {'A∩B': [(x, y), (x, y) ...]}
        self.__drawUnions = {}

        # Diccionario que almacena todos valores necesarios para dibujar el set
        # de complemento de cada set {"A'": [(x, y), (x, y), ...]}
        self.__complements = {}

        # Diccionario que almacena todos valores de complemento de cada set
        # {"A'": [(m, value), ...]}
        self.__complementValues = {}

        self.__createFuzzySet()

    def __createFuzzySet(self):
        self.__createSets()
        self.__getAllMemberValues()
        self.__getComplements()
        self.__getAllInstersections()

    def __createSets (self):

        kernels = self.__kernels
        supports = self.__supports
        high = self.__high

        memebershipSets = {}    # Guarda los valores de pertenecia de cada miembro 
                                # por fuzzy set

        fuzzySets = {}          # Guarda el orden bien definido de los puntos 
                                # necesarios para dibujar cada fuzzy set

        colors = {}             # Guarda el código hex de cada fuzzy set

        fuzzySets, colors = self.__fromKStoSet(kernels, supports, high)
        
        #almacenamos los sets y colores obtenidos como un atributo de la clase
        self.__sets = fuzzySets
        self.__colors = colors

        #Dibujamos los sets obtenidos 
        ax = self.__drawFuzzySystem()

        # Colocamos título a al sistema difuso
        ax.set_title(self.__title)
        ax.legend() #hacemos visible el atributo label en nuestra figura final
        plt.show()  #mostramos la figura
        

    def __drawFuzzySystem(self, fuzzyList=1, ax=0, color=0, id=0, fill=0, linestyle="-"):
        if not ax:  
            _, ax = plt.subplots()

        if fuzzyList == 1:
            #Dibuja todo el sistema(se dibuja a sí mismo)
            items = list(self.__sets.values())
            keys = list(self.__sets.keys())
        else:
            #Dibuja un sistema dado una lista de puntos
            items = fuzzyList
            if not id:
                keys = [chr(96 + x) for x in range(len(fuzzyList))]
            else:
                keys = id

        for i in range(len(items)):
            k = keys[i]
            if color == 0:
                colorline = self.__colors[k] if fuzzyList == 1 else self.__getRandomColor()
            else:
                if len(color) > i:
                    colorline = color[i]
            fset = items[i]
            for i in range(len(fset)-1):
                if i == len(fset)-2:
                    ax.plot([fset[i][0], fset[i+1][0]],  [fset[i][1], fset[i+1][1]], linestyle , c=colorline, label=k)
                    if fill:
                        ax.fill_between([fset[i][0], fset[i+1][0]],  [fset[i][1], fset[i+1][1]], color=fill)
                else:
                    ax.plot([fset[i][0], fset[i+1][0]],  [fset[i][1], fset[i+1][1]], linestyle, c=colorline)
                    if fill:
                        ax.fill_between([fset[i][0], fset[i+1][0]],  [fset[i][1], fset[i+1][1]], color=fill)
        return ax
    
    def __drawMembershipValues(self, values, ax):
        for v in values:
            ax.plot([v[0], v[0]], [0, v[1]], "--", c="#000")
        return ax
    
    def __fromSettoKS(self, sets):
        high = []
        kernels = []
        supports = []
        
        high.append(sets[1][1])
        drawset = list(map(lambda x: x[0], sets))
        supports.append(drawset[0])
        supports.append(drawset[3])
        kernels.append(drawset[1])
        kernels.append(drawset[2])

        return kernels, supports, high

    def __fromKStoSet(self, kernels, supports, high=[1]):
        fuzzySets = {}          # Guarda el orden bien definido de los puntos 
                                # necesarios para dibujar cada fuzzy set

        colors = {}             # Guarda el código hex de cada fuzzy set

        count = 0               # Variable que ayuda a determinar el id de cada fuzzyset
        counthigh = 0           # Variable que ayuda a iterar las alturas en caso de 
                                # que exista más de 1 

        for x in range (0, len(kernels), 2):

            #Define el color para cada fuzzy set de forma aleatoria
            color = self.__getRandomColor()

            #define el identificador de cada fuzzyset
            labelid = chr(65 + count)

            #almacenamos los puntos trazados por cada fuzzyset  [(x,y),(x,y),...]
            fuzzySetsItem = [
                                    (supports[x], 0), 
                                    (kernels[x], high[counthigh]), 
                                    (kernels[x + 1], high[counthigh]), 
                                    (supports[x + 1], 0)
                                ]
            
            #almacenamos una lista con los puntos necesarios para trazar cada fuzzy set 
            fuzzySets[labelid] = fuzzySetsItem
            
            #almacenamos el color usado para cada fuzzyset {'A' : "#3265EF"}
            colors[labelid] = color

            count += 1
            if counthigh < len(high)-1:
                counthigh+=1

        return fuzzySets, colors
    
    def __getAllMemberValues(self):
        fuzzySets = self.__sets
        memebershipSets = {}
        for f in list(fuzzySets.items()):
            labelid = f[0]
            fuzzySetsItem = f[1]
            missingValues = self.__getMemberValues(fuzzySetsItem)
            memebershipSets[labelid] = sorted(list(set(fuzzySetsItem)) + list(set(missingValues)), key=lambda x: (x[0], x[1]))

        self.__memebershipValues = memebershipSets
        print(memebershipSets)
    

    def __getMemberValues(self, item):
        points = sorted(list(set(item)), key=lambda x: (x[0], x[1]))    #creamos una lista(list) de puntos únicos sin repetición(set) ordenada 
                                                                        #ASC(sorted) del fuzzy set dado(item). Ejemplo:
                                                                        # item = [(7, 0), (8,1), (8,1), (10, 0)] -> [(7, 0), (8,1), (10, 0)]
        if len(points) == 4 and item == list(self.__sets.values())[-1]:
            points[2:] = sorted(points[2:], key = lambda x : x[1], reverse=True)


        
            
        membersrange =  list(map(lambda x: x[0], 
                                filter(lambda x: x[1] == 0, points)))   #basada en la lista anterior (points), creamos una segunda lista que nos indique 
                                                                        #el rango de valores que abarca el fuzzy set dado(item) Ej. 
                                                                        # points = [(7, 0), (8,1), (10, 0)] -> [7, 10]

        members = self.__getMembersInRange(membersrange)                #basada en la lista anterior (membersrange), creamos una lista con todos los 
                                                                        #miembros que contiene el fuzzy set dado Ej. 
                                                                        # membersrange = [7, 10] -> [7, 8, 9, 10]

        givenMembers = list(set(map(lambda x: x[0], points)))           #basada en la lista points, creamos una lista de los valores en x que posee, 
                                                                        #puesto que estos equivalen a los miembros que ya tienen valor de pertenencia. Ej
                                                                        # points = [(7, 0), (8,1), (10, 0)] -> [7, 8, 10]

        valores = []    #Esta lista almacenará los valores de pertenencia encontrados a los miembros que no lo poseen del fuzzy set dado
        #Loop para encontrar aquellos miembros que no poseen valor de pertenencia
        for m in members:
        #Si el miembro no existe en la lista de miembros con valor de pertenencia...
            if not(m in givenMembers):
        #...entonces tenemos que buscar debajo de qué linea del fuzzy set se encuentra este miembro para así poder determinar su valor de pertenencia
        #a través de resolver un sistema de ecuaciones lineales. Para ello, hay que buscar qué pareja de valores (será tomada como un rango [memberRang]) 
        #en la lista points puede contener al miembro. Este análisis se basa en los valores en x Ej. 
        # (points = [(7, 0), (8,1), (10, 0)], m = 9) -> 8,10
                for x in range(len(points)-1):
                    # Si m se encuentra entre el valor en x del presente punto y el siguiente
                    if points[x][0] <= m and points[x+1][0] >= m:
                    #Entonces tomamos dicho par de puntos y los almacenamos como el rango en el que se encuentra el miembro de quien queremos conocer su 
                    #valor de pertenencia. Visto gráficamente, memberRange refiere a la linea que pasa por encima de dicho miembro. 
                        memberRange = [points[x], points[x+1]]
                        break
                line1 = [(m, 0), (m, 1)] #Es la línea recta que representa el punto que buscamos
                punto = self.__getLineIntersection(line1, memberRange)  #teniendo el miembro del cual queremos conocer su valor de pertenencia y el rango en el 
                                                                    #que se encuentra, podemos proceder a buscar el valor de pertenencia mediante este 
                                                                    # método

                valores.append(punto) #almacenamos el valor de pertenencia del miembro. Punto = (miembro, valor) o (x, y)

        return valores
    
    def __getLineIntersection (self, line1, line2):
        # line: refiere a un miembro sin valor de pertenencia representado como línea vertical
        # range: refiere al rango de valores en el que se encuentra member. Debe ser visto como la línea que pasa por encima de dicho punto
        #Este método pretende el punto de intersección entre ambas lineas, esto es equivalente a hallar el valor de pertenencia de member

        #line equivale a la línea1 con la que va a intersectarse
        x1_1 = line1[0][0]
        x1_2 = line1[1][0] 
        y1_1 = line1[0][1]
        y1_2 = line1[1][1]

        #El rango equivale a los dos puntos que forman la recta con la que se va instersectar la linea que representa a nuestro miembro
        x2_1 = line2[0][0]
        x2_2 = line2[1][0] 
        y2_1 = line2[0][1]
        y2_2 = line2[1][1]

        #Casos en los que se busca la intersección de un punto en x con respecto a una línea
        #Por ejemplo, cuando buscamos valores de pertenencia.

        if x1_1 == x1_2:
            x = x1_1
            y = y2_1 if y2_1 == y2_2 else self.__findy(x, line2)
            return (x, y)
        elif x2_1 == x2_2:
            x = x2_1
            y = y1_1 if y1_1 == y1_2 else self.__findy(x, line1)
            return (x, y)
        
        #Casos en los que se busca la intersección de un punto en y con respecto a una línea
        if y1_1 == y1_2:
            y = y1_1
            x = x2_1 if x2_1 == x2_2 else self.__findx(y, line2)
            return (x, y)
        elif x2_1 == x2_2:
            y = y2_1
            x = x1_1 if x1_1 == x1_2 else self.__findx(y, line1)
            return (x, y)
        
        eq1 = self.__geteqline(line1)
        eq2 = self.__geteqline(line2)

        x = -(eq2[1] - eq1[1])/(eq2[0] - eq1[0])
        y = (eq1[0] * x) + eq1[1]

        y = round(y, 2)                     # dejamos 2 dígitos después del 0 para y
        x = round(x, 2)                     # dejamos 2 dígitos después del 0 para y

        y = self.__validateRound(y)
        x = self.__validateRound(x)

        return (x, y)
    
    def __validateRound(self, x):
        afterz = str(x).split(".")
        if int(afterz[1]) > 95:
            return round(x)
        else:
            return x
    
    def __geteqline(self, line):
        #Dada una línea, obtiene la ecuación de esta.
        x1 = line[0][0] 
        x2 = line[1][0]
        y1 = line[0][1]
        y2 = line[1][1]

        #pendiente
        m = (y2 - y1) / float(x2 - x1) 

        #(m + (m*-x1)x + y1)
        eq = [m, (m * -(x1)) + y1]
        return eq
    
    def __findy(self, member, range):
        #Esta función se encarga de resolver la ecución para encontrar el valor de y dado x.
        # member: miembro del que buscamos valor de pertenencia. Tiene que ser tomado como x.
        # range: equivale a los dos puntos de la linea con la que member se va a intersectar. [(x1, y1), (x2, y2)]

        x1 = range[0][0] 
        x2 = range[1][0] 
        y1 = range[0][1]
        y2 = range[1][1]
    
        m = (y2 - y1) / float(x2 - x1)      #obtener pendiente
        y = m*member + (m * -(x1)) + y1    #resolver y-y1 = m(x-x1) -> y = m(x - x1) + y1
        y = round(y, 2)                     # dejamos 2 dígitos después del 0 para y
        self.__validateRound(y)

        return y
    
    def __findx(self, member, range):
        #Esta función se encarga de resolver la ecución para encontrar el valor de x dado y.
        # member: miembro del que buscamos valor de pertenencia. Tiene que ser tomado como y.
        # range: equivale a los dos puntos de la linea con la que member se va a intersectar. [(x1, y1), (x2, y2)]
        x1 = range[0][0] 
        x2 = range[1][0] 
        y1 = range[0][1]
        y2 = range[1][1]

        m = (y2 - y1) / float(x2 - x1)
        y = member
        x = (y - y1 + (m * x1))/m
        x = round(x, 2)                     # dejamos 2 dígitos después del 0 para y
        self.__validateRound(x)

        return x
    
    def __getComplements(self):
        sets = list(self.__sets.items())
        complements = {}

        memberValues = list(self.__memebershipValues.items())
        complementValues = {}

        complement = lambda x: (x[0], (-1 * x[1]) + 1)

        for s in sets:
            complements[f"{s[0]}'"] = list(map(lambda x: complement(x), s[1]))

        for v in memberValues:
            complementValues[f"{v[0]}'"] = list(map(lambda x: complement(x), v[1]))

        self.__complements = complements #Almacena los valores necesarios para dibujar 
                                        #los sets de complemento
        self.__complementValues = complementValues #Almacena los valores de pertenencia 
                                                    #de los sets de complemento

    def __getAllInstersections(self):
        sets = list(self.__sets.keys())
        for i in range(len(sets)-1):
            for j in range(i + 1, len(sets)):
                self.__getIntersection(sets[i], sets[j])

    def __getIntersection(self, set1, set2):
        set1 = set1.upper()
        set2 = set2.upper()

        if set1 == set2:
            return None

        sortedsets = sorted([set1, set2])
        set1 = sortedsets[0]
        set2 = sortedsets[1]

        fset1 = self.__sets[set1]
        fset2 = self.__sets[set2]

        if fset1[-1][0] > fset2[0][0] and fset1[-1][0] <= fset2[-1][0]:
            
            line1 = [fset1[-2], fset1[-1]]
            line2 = [fset2[0], fset2[1]]

            kernel = self.__getLineIntersection(line1, line2)

            support2 = line1[1]
            support1 = line2[0]

            self.__drawIntersections[f"{set1}∩{set2}"] = [support1, kernel, kernel, support2]

            missingmembers = self.__getMemberValues(self.__drawIntersections[f"{set1}∩{set2}"])

            self.__intersections[f"{set1}∩{set2}"] = sorted(missingmembers + self.__drawIntersections[f"{set1}∩{set2}"], 
                                                            key=lambda x: (x[0], x[1]))
            
            #print(f"{set1}∩{set2} = ", self.__intersections[f"{set1}∩{set2}"])
            return self.__intersections[f"{set1}∩{set2}"]
        else:
            #print(f"No existe intersección entre el conjunto {set1} y el conjunto {set2}")
            return None
        
    def showAllIntersections(self, clear=0):
        sectionColor = "#fc03e8"
        intersections = self.__drawIntersections
        if not clear:
            ax = self.__drawFuzzySystem()
            ax = self.__drawFuzzySystem(list(intersections.values()), 
                                        ax, 
                                        [sectionColor], 
                                        list(intersections.keys()), 
                                        sectionColor)
        else:
            _, ax = plt.subplots()
            ax = self.__drawFuzzySystem(list(intersections.values()), 
                                        ax, 
                                        [sectionColor], 
                                        list(intersections.keys()))
            
        ax.set_title(f"Intersecciones")
        ax.legend()
        plt.show
        return self.__intersections
    
    def showIntersection(self, set1, set2):
        set1 = set1.upper()
        set2 = set2.upper()

        sortedsets = sorted([set1, set2])

        set1 = sortedsets[0]
        set2 = sortedsets[1]

        intersections = self.__drawIntersections

        title = f"{set1}∩{set2}"

        if not title in intersections:
            print(f"No existe la intersección {title}")
            return None

        sectionColor = "#fc03e8"
        intersection = intersections[title]

        ax = self.__drawFuzzySystem()
        ax = self.__drawFuzzySystem([intersection], 
                                    ax, 
                                    [sectionColor], 
                                    [title], 
                                    sectionColor)
        
        ax.set_title(f"Intersección: {title}")
        ax.legend()
        plt.show
        
        print(f"{title}: {self.__intersections[title]}")
        return self.__intersections[title]
    
    def showAllComplements(self, clear=0):
        complements = self.__complements
        items = list(complements.values())
        keys = list(complements.keys())

        if clear:
            _, ax = plt.subplots()
            color = list(self.__colors.values())
        else:
            ax = self.__drawFuzzySystem()
            color = ["#000"]

        ax = self.__drawFuzzySystem(items, ax, color, keys, 0, "--")
        ax.set_title(f"Complementos")
        ax.legend()
        plt.show

        return self.__complementValues
    
    def showComplement(self, set1, clear=0):
        requested = set1.upper() + "'"
        complements = self.__complements

        if not requested in complements:
            print(f"No existe el conjunto: {requested}")
            return None

        complement = complements[requested]
        
        if clear:
            _, ax = plt.subplots()
            color = list(self.__colors.values())
        else:
            ax=self.__drawFuzzySystem()
            color = ["#000"]

        ax = self.__drawFuzzySystem([complement], 
                                    ax, color, 
                                    [requested], 0, "--")

        ax.set_title(requested)
        ax.legend()
        plt.show
        print(f"{requested}: {self.__complementValues[requested]}")
        return self.__complementValues[requested]
    
    def showMembershipValues(self, set1):
        set1 = set1.upper()
        memberValues = self.__memebershipValues[set1]
        ax = self.__drawFuzzySystem()
        self.__drawMembershipValues(memberValues, ax)

        ax.set_title(self.__title + f": {set1}")
        plt.show()
        print(f"{set1}: {memberValues}")
        return memberValues
    
    def showAllMembershipValues(self):
        sets = list(self.__memebershipValues.values())
        ax = self.__drawFuzzySystem()
        ax.set_title(self.__title + ": Valores de Pertenencia")
        for s in sets:
            self.__drawMembershipValues(s, ax)
        plt.show()
        print(self.__title, ": " ,self.__memebershipValues)
        return self.__memebershipValues
    
    def getUnion(self, set1, set2, clear=0):
        set1 = set1.upper()
        set2 = set2.upper()

        if (set1 == set2) or (set1 not in self.__sets) or (set2 not in self.__sets):
            print("Ingresa sets válidos")
            return None
        drawingSets = self.__sets
        valuesSets = self.__memebershipValues
        intersections = self.__intersections
        firstset = min(set1, set2)
        secondset = set2 if set1 == firstset else set1

        titleUnion = f"{firstset}∪{secondset}"
        titleIntersection=f"{firstset}∩{secondset}"

        if clear:
            _, ax = plt.subplots()
        else:
            ax = self.__drawFuzzySystem()

        if titleUnion in self.__unions:
            self.__drawFuzzySystem([self.__drawUnions[titleUnion]], 
                                    ax, ["#3DFF0F"], [titleUnion], ["#3DFF0F"], "--")
            ax.legend()
            plt.show()
            return self.__unions[titleUnion]

        if titleIntersection in intersections:
            intersection = self.__drawIntersections[titleIntersection]
        else:
            intersection = 0
        
        drawSet1 = drawingSets[firstset]
        drawSet2 = drawingSets[secondset]


        if intersection:
            drawSetUnion = self.__joinIntersectedSets(intersection, drawSet1, drawSet2)
            self.__drawFuzzySystem([drawSetUnion], ax, ["#3DFF0F"], [titleUnion], ["#3DFF0F"], "--")
            missingvalues = self.__getMemberValues(drawSetUnion)
            values = sorted(set(drawSetUnion + missingvalues), key=lambda x: (x[0], x[1]))
        else:
            drawSetUnion = drawSet1 + drawSet2
            self.__drawFuzzySystem([drawSetUnion], ax, ["#3DFF0F"], [titleUnion], ["#3DFF0F"], "--")
            values = valuesSets[firstset] + valuesSets[secondset]

        self.__drawUnions[titleUnion] = drawSetUnion
        self.__unions[titleUnion] = values
        
        ax.legend()
        plt.show()
        return values
    
    def getMembershipValues(self):
        return self.__memebershipValues
    
    def getSetMembershipValues(self, set1):
        if set1 in self.__memebershipValues:
            return self.__memebershipValues[set1]
        
    def newSegment (self, sets, high):
        kernels = []
        supports = []
        for s in zip(sets, high):
            newtop = []
            selectedSet = self.__sets[s[0]]
            highSet = s[1]
            line2 = [(0, highSet), (1000, highSet)]

            line1 = selectedSet[:-2]
            newtop.append(self.__getLineIntersection(line1, line2))

            line1 = selectedSet[2:]
            newtop.append(self.__getLineIntersection(line1, line2))

            newset = [selectedSet[0]] + newtop + [selectedSet[-1]]
            aux1, aux2, _ = self.__fromSettoKS(newset)

            kernels += aux1
            supports += aux2

        return FuzzySets(kernels, supports, f"Segmento: {sets}", high)
    
    def defuzzyFOM(self):
        sets = list(self.__memebershipValues.values())
        allsets = []
        for s in sets:
            allsets += s
        values = list(map(lambda x: x[1], allsets))
        maxvalue = max(values)
        maxmembers = list(filter(lambda x: x[1] == maxvalue, allsets))
        maxmember = sorted(maxmembers, key=lambda x: x[1])
        return maxmember[0][0]
    
    def defuzzyLOM(self):
        sets = list(self.__memebershipValues.values())
        allsets = []
        for s in sets:
            allsets += s
        allsets = sorted(allsets, key=lambda x: (x[1], x[0]))
        #print(allsets[-1][0])
        return allsets[-1][0]
    
    def defuzzyWA(self):
        sets = list(self.__memebershipValues.values())
        allsets = []
        numerador = 0
        denominador = 0
        for s in sets:
            allsets += s

        allsets = list(filter(lambda x: x[1] != 0, allsets))
        for a in allsets:
            numerador += a[0]*a[1]
            denominador += a[1]

        return numerador/denominador

    def defuzzyCOG(self):
        areas = []
        centroids = []
        numerador = 0
        denominador = 0

        sets = list(self.__sets.values())
        for s in sets:
            a, c = self.__getSetCentroidArea(s)
            areas += a
            centroids += c

        print(areas)
        print(centroids)
        for area, centroid in zip(areas, centroids):
            numerador += area*centroid
            denominador += area
        return numerador / denominador
        
    def __getSetCentroidArea(self, newfuzzyset):
        print(newfuzzyset)
        areas = []
        centroids = []
        if newfuzzyset[0][0] == newfuzzyset[1][0]:
            if newfuzzyset[2][0] == newfuzzyset[3][0]:
                #Caso en el que todo el segmento forme un rectángulo
                point1 = newfuzzyset[1][0]
                point2 = newfuzzyset[3][0]
                base = point2 - point1
                high = newfuzzyset[1][1]
                area = self.__getrectangleArea(base, high)
                centroid = self.__getrectangleCentroid(point1, point2)
                areas.append(area)
                centroids.append(centroid)
            else:
                #Caso en el que el segmento esté formado por un rectángulo y un triángulo (en ese orden)
                print("Caso en el que el segmento esté formado por un rectángulo y un triángulo (en ese orden)")
                #Para el rectángulo
                print("Rectángulo") 
                point1 = newfuzzyset[0][0]
                point2 = newfuzzyset[2][0]
                base = point2 - point1
                print("Base", base)
                high = newfuzzyset[1][1]
                print("Altura", high)
                subarea1 = self.__getrectangleArea(base, high)
                subarea1_centroid = self.__getrectangleCentroid(point1, point2)
                subarea1 = round(subarea1, 2)
                subarea1_centroid = round(subarea1_centroid, 2)
                print("Area: ", subarea1)
                print("centroide: ", subarea1_centroid)
                areas.append(subarea1)
                centroids.append(subarea1_centroid)
                #Para el Triangulo
                print("Triángulo") 
                point1 = newfuzzyset[2][0]
                point2 = newfuzzyset[2][0]
                point3 = newfuzzyset[3][0]
                base = point3 - point2
                print("Base", base)
                high = newfuzzyset[1][1]
                print("Altura", high)
                subarea2 = self.__getTriangleArea(base, high)
                subarea2_centroid = self.__getTriangleCentroid(point1, point2, point3)
                subarea2 = round(subarea2, 2)
                subarea2_centroid = round(subarea2_centroid, 2)

                print("Area: ", subarea2)
                print("centroide: ", subarea2_centroid)
                areas.append(subarea2)
                centroids.append(subarea2_centroid)
        else:
            if newfuzzyset[2][0] == newfuzzyset[3][0]:
                #Caso en el que el segmento sea un triángulo seguido de un rectángulo
                print("Caso en el que el segmento sea un triángulo seguido de un rectángulo")
                #Para el Triangulo
                point1 = newfuzzyset[0][0]
                point2 = newfuzzyset[1][0]
                point3 = newfuzzyset[1][0]
                base = point2 - point1
                high = newfuzzyset[1][1]
                subarea1 = self.__getTriangleArea(base, high)
                subarea1_centroid = self.__getTriangleCentroid(point1, point2, point3)
                areas.append(subarea1)
                centroids.append(subarea1_centroid)
                #Para el rectángulo 
                point1 = newfuzzyset[1][0]
                point2 = newfuzzyset[2][0]
                base = point2 - point1
                high = newfuzzyset[1][1]
                subarea2 = self.__getrectangleArea(base, high)
                subarea2_centroid = self.__getrectangleArea(point1, point2)
                areas.append(subarea2)
                centroids.append(subarea2_centroid)
            
            else:
                #Para el caso en el que el segmento sea un rectángulo entre dos triangulos
                #Para el Triangulo1
                print("Caso en el que el segmento sea un trapecio chido")
                print("Triángulo 1") 
                point1 = newfuzzyset[0][0]
                point2 = newfuzzyset[1][0]
                point3 = newfuzzyset[1][0]
                base = point2 - point1
                high = newfuzzyset[1][1]
                print("Base", base)
                print("Altura", high)
                subarea1 = self.__getTriangleArea(base, high)
                subarea1_centroid = self.__getTriangleCentroid(point1, point2, point3)
                subarea1 = round(subarea1, 2)
                subarea1_centroid = round(subarea1_centroid, 2)
                print("Area: ", subarea1)
                print("Centroide: ", subarea1_centroid)
                areas.append(subarea1)
                centroids.append(subarea1_centroid)
                #Para el rectángulo 
                print("Rectángulo")
                point1 = newfuzzyset[1][0]
                point2 = newfuzzyset[2][0]
                base = point2 - point1
                high = newfuzzyset[1][1]
                print("Base", base)
                print("Altura", high)
                subarea2 = self.__getrectangleArea(base, high)
                subarea2_centroid = self.__getrectangleCentroid(point1, point2)
                subarea2 = round(subarea2, 2)
                subarea2_centroid = round(subarea2_centroid, 2)
                print("Area: ", subarea2)
                print("Centroide: ", subarea2_centroid)
                areas.append(subarea2)
                centroids.append(subarea2_centroid)
                #Para el Triangulo2
                print("Triangulo 2")
                point1 = newfuzzyset[2][0]
                point2 = newfuzzyset[2][0]
                point3 = newfuzzyset[3][0]
                base = point3 - point2
                high = newfuzzyset[1][1]
                print("Base", base)
                print("Altura", high)
                subarea3 = self.__getTriangleArea(base, high)
                subarea3_centroid = self.__getTriangleCentroid(point1, point2, point3)
                subarea3 = round(subarea3, 2)
                subarea3_centroid = round(subarea3_centroid, 2)
                print("Area: ", subarea3)
                print("Centroide: ", subarea3_centroid)
                areas.append(subarea3)
                centroids.append(subarea3_centroid)
        return areas, centroids
    

    def __getrectangleArea(self, base, high):
        return base*high
    
    def __getTriangleArea(self, base, high):
        return (base*high)/2
    
    def __getrectangleCentroid(self, point1, point2):
        return (point1 + point2)/2
    
    def __getTriangleCentroid(self, point1, point2, point3):
        return (point1 + point2 + point3)/3
    
    def __joinIntersectedSets(self, setIntersection, set1, set2):
        intersectionpoint = setIntersection[1]
        drawset1 = self.__cutSetForJoin(intersectionpoint, set1)
        drawset2 = self.__cutSetForJoin(intersectionpoint, list(reversed(set2)))
        return drawset1 + list(reversed(drawset2))


    def __cutSetForJoin(self, point, set1):
        drawSet = set1[:-1]
        drawSet.append(point)
        return drawSet

    def __getMembersInRange(self, membersrange):
        return [x for x in range(membersrange[0], membersrange[1]+1)]

    def __getRandomColor(self):
        return "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])


