import copy

# taszk osztály
class Task:
    def __init__(self, x , y = []):
        self.name = x   # a taszk neve
        self.utasitasok = y    # a taszkhoz tartozó utasítások tömbje
        self.holtart = 0
        self.kesz = False


def isCyclicUtil(graph, v, visited, recStack):
 
    # meg kell jelölni az aktuális pontot, hogy el lett érve
    # berakni a recStack-be
    
    visited.append(v)
    recStack.append(v)
 
    # rekurzió minden szomszédra:
    # ha egy szomszéd szerepel a bejárt élek között
    # és benne van a recStack-ben is, akkor van kör
    for neighbour in graph[v]:
        if neighbour not in visited:
            # rekurzió
            if isCyclicUtil(graph, neighbour, visited, recStack) == True:
                return True
        elif neighbour in recStack:
            return True
 
    # a recStak-ből töröljük a kezdőélt, mert
    # ezzel a bejárással nem lett kör vele
    recStack.remove(v)
    return False


def isCyclic(graph, start, end):

    # a gráf másolatát vizsgáljuk a plusz éllel
    g = copy.deepcopy(graph)
    g[start].append(end)
    
    visited = []
    recStack = []

    for key in graph.keys():
        if key not in visited:
            # minden be nem járt pontra megnézzük, hogy belőle kiindulva lesz-e kör
            if isCyclicUtil(g,key,visited,recStack)== True:
                return True

    return False

def main():

    #beolvasás
    
    tasks=[]
    graph = {}
    eroforrasok = {}

    while True:
        try:
            oneTask = input()
            
            if oneTask=="":
                break
            
            oneTask = oneTask.split(",")
            tasks.append(Task(oneTask[0], oneTask[1:]))

        except EOFError:
            break

    # erőforrások foglalásának nézése

    for t in tasks:
        for u in t.utasitasok:
            if u == "0":
                continue
            # a FIFO-t valósítja meg
            # tömb első eleme, aki épp foglalja, a többi aki várakozik rá
            eroforrasok[u[1:]] = [] 

    # csúcspontok hozzáadása és üres gráf

    for t in tasks:
        graph[t.name] = []
        for u in t.utasitasok:
            if u == "0":
                continue
            graph[u[1:]] = []

    # élek hozzáadása ha nincs kör

    on = True

    while(on):

        for t in tasks:

            for x in tasks:
                if x.holtart>len(x.utasitasok)-1:
                    x.kesz = True
                    

            kesz = 0
            for t2 in tasks:
                if t2.kesz == True:
                    kesz += 1
            if kesz == len(tasks):
                on = False
                break

            if t.kesz:
                
                tomb = {}
                for key, value in eroforrasok.items():
                    if len(eroforrasok[key])>0 and value[0]==t.name:
                        tomb[key]=-1
                
                for key, value in tomb.items():
                    for y in range(len(t.utasitasok)-1,-1,-1):
                        st = "+"+str(key)
                        
                        if t.utasitasok[y]==st:
                            tomb[key]=y


                # minimum érték megkeresése:

                min = -1

                for key, value in tomb.items():
                    if min == -1:
                        min=value
                    elif value<min:
                        min=value

                # kitörölni a gráfból, az erőforrásokból és a helyére érkezőnél nézni, hogy kör-e
                temp = None
                
                for key, value in graph.items():
                    if len(value)>0 and key==t.utasitasok[min][1:] and value[0]==t.name:
                        temp = key
                        graph[key]=[]
                        

                if temp is not None and len(eroforrasok[temp])>0 and eroforrasok[temp][0]==t.name:
                    eroforrasok[temp].pop(0)
                    
                    fut = True
                    if len(eroforrasok[temp])>0:

                        for key, value in graph.items():
                            if key==eroforrasok[temp][0]:
                                graph[key]=[]
                                break

                        while(fut):
                            if not isCyclic(graph, temp, eroforrasok[temp][0]):
                                
                                graph[temp].append(eroforrasok[temp][0])
                                            
                                for r in tasks:
                                    if r.name==eroforrasok[temp][0]:
                                        r.holtart +=1
                                
                                fut = False
                                
                            else:
                                for i in tasks:
                                    if len(eroforrasok[temp])>0 and eroforrasok[temp][0] == i.name:
                                        print("jajjne",i.name, i.holtart, temp, sep=",", end="\n")
                                        eroforrasok[temp].pop(0)

                            if not len(eroforrasok[temp])>0:
                                break
                t.holtart+=1

                continue
            
            if t.utasitasok[t.holtart] == "0":
                t.holtart += 1
              
                continue

            elif t.utasitasok[t.holtart][0] == "+":

                # ha szabad az erőforrás lefoglalja
                if eroforrasok[t.utasitasok[t.holtart][1:]] == []:
                    graph[t.utasitasok[t.holtart][1:]].append(t.name)
                    eroforrasok[t.utasitasok[t.holtart][1:]].append(t.name)
                    t.holtart += 1

                # ha foglalt az erőforrás várakozik, és hozzáadja a várakozókhoz a 
                else:
                     
                    if not isCyclic(graph, t.name, t.utasitasok[t.holtart][1:]):
                        if t.utasitasok[t.holtart][1:] not in graph[t.name]:
                            graph[t.name].append(t.utasitasok[t.holtart][1:])
                            if t.name not in eroforrasok[t.utasitasok[t.holtart][1:]]:
                                eroforrasok[t.utasitasok[t.holtart][1:]].append(t.name)
                    else:
                        print(t.name, t.holtart+1, t.utasitasok[t.holtart][1:], sep=",", end="\n")
                        t.holtart += 1

            elif t.utasitasok[t.holtart][0] == "-":

                # törlés a gráfból
                torolt = None
                
                for key, value in graph.items():
                    if len(value)>0 and value[0] == t.name and key==t.utasitasok[t.holtart][1:]:
                        graph[key]=[]
                        torolt = key                

                # törlés a FIFO-ból és új kérés -> vizsgálni kör van-e benne
                if torolt is not None and len(eroforrasok[torolt])>0 and eroforrasok[torolt][0]==t.name:
                    eroforrasok[torolt].pop(0)
                    
                    fut = True
                    if len(eroforrasok[torolt])>0:

                        for key, value in graph.items():
                            if key==eroforrasok[torolt][0]:
                                graph[key]=[]
                                break

                        while(fut):
                            if not isCyclic(graph, torolt, eroforrasok[torolt][0]):
                                
                                graph[torolt].append(eroforrasok[torolt][0])
                                            
                                for r in tasks:
                                    if r.name==eroforrasok[torolt][0]:
                                        r.holtart +=1
                                
                                fut = False
                                
                            else:
                                for i in tasks:
                                    if len(eroforrasok[torolt])>0 and eroforrasok[torolt][0] == i.name:
                                        print("baj",i.name, i.holtart, torolt, sep=",", end="\n")
                                        eroforrasok[torolt].pop(0)

                            if not len(eroforrasok[torolt])>0:
                                break
                t.holtart+=1
            

main()

