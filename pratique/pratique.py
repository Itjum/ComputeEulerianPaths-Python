import osmnx as ox
import networkx as nx


#PARTIE PRATIQUE
import math

def drone(city):
    M = ox.graph_from_place(city, network_type='drive', simplify=True).to_undirected()
    M = nx.convert_node_labels_to_integers(M)
    G = nx.eulerize(M)
    nodes = nx.eulerian_path(G

    textfile = open("pratique/output_drone.txt", "w")

    textfile.write("CIRCUIT DU DRONE ARETE PAR ARETE\n\n")
    for element in nodes:
        print(element)
        textfile.write(str(element) + "\n")
    
    print("ECRIT DANS LE FICHIER pratique/output_drone.txt")


def deneigeuse(n):
    M = ox.graph_from_place('Montréal,Canada', network_type='drive', simplify=True)
    M = nx.convert_node_labels_to_integers(M)
    graph = M
    graph = ox.utils_graph.get_largest_component(graph, strongly=True)
    List2Tuple = []

    for u,v,w in graph.edges(data=True):
        List2Tuple.append((u, v, w))

    eulerization_directed(List2Tuple, graph)
    List3Tuple = []
    for u,v,w in graph.edges(data=True):
        List3Tuple.append((u, v, w))

    nodes = eulerian_circuit(List3Tuple)
    edges = nodes_to_edges(nodes, List3Tuple)
    
    
    textfile = open("pratique/output_deneigeuse.txt", "w")

    textfile.write("CIRCUIT DES DENEIGEUSES NOEUD PAR NOEUD\n\n")
    for element in nodes:
        textfile.write(str(element) + "\n")
        
    textfile.write("\nCIRCUIT DES DENEIGEUSES ARRETE PAR ARRETE\n\n")
    for element in edges:
        textfile.write(str(element) + "\n")
    
    testlist = decoupe(edges, n)

    ox.plot_graph(graph, node_size=0)
    for i in range (n):
        couleur = couleurchemin(testlist[i], graph)
        ox.plot_graph(graph, edge_color=couleur, node_size=0)
        print(testlist[i])



def create_dict_edges_degrees(edges, lgt):
    res = {}
    i = 0
    while (i < lgt):
        cur_v = edges[i][0]
        begin = i
        while (i < lgt and cur_v == edges[i][0]):
            i += 1
        # Indice du début des arrêtes partant du sommet, nombre des dites arrêtes, degrées entrants en négatif (servira ensuite à eulerizer)
        res[cur_v] = [begin, i - begin, (i - begin)]
    
    i = 0
    # On ajoute tous les degrées sortant à chacun des noeuds correspondant
    while (i < lgt):
        res[edges[i][1]][2] -= 1
        i += 1

    # Pour chaque sommet, on a donc un nombre négatif s'il y a plus de degrées entrants (donc origines pour de nouvelles arrêtes)
    # et inversement : un nombre positif s'il y a plus de degrées sortants (donc destinations pour de nouvelles arrêtes)
    return res


def min(todo, dist):
    minval = math.inf
    min = None
    for i in todo:
        if (dist[i][0] < minval):
            minval = dist[i][0]
            min = i
    return min


def find_weight(frm, to, edges, dict):
    begin = dict[frm][0]
    size = dict[frm][1]
    i = begin
    while (i < begin + size):
        if (edges[i][1] == to):
            return edges[i][2]
        i += 1
    print("LE POIDS N'A PAS ETE TROUVE")
    return None
    
def my_find_weight(frm, to, edges):
    for a,b,c in edges:
        if (a == frm and b == to):
            return c["length"]
    return None
    

def djikstra_wparent(edges, frm, demanding, vertices, dict, graph):
    todo = [frm]
    dist = {frm: [0, None]}
    cur = frm
    while (True):
        cur = min(todo, dist)
        if (cur == None):
            print("Should not be None here")
            exit(1)
        todo.remove(cur)
        if (cur in demanding):
            dict[cur][2] -= 1
            if (dict[cur][2] == 0):
                demanding.remove(cur)
            path = [cur]
            tmp = dist[cur][1]
            while (tmp != frm):
                if (graph != None):
                    graph.add_edge(tmp, cur, weight=find_weight(tmp, cur, edges, dict))
                path.insert(0, tmp)
                cur = tmp
                tmp = dist[tmp][1]
            if (graph != None):
                graph.add_edge(frm, cur, weight=find_weight(frm, cur, edges, dict))
            path.insert(0, frm)
            return path

        infos = dict[cur]
        i = infos[0]
        while (i < infos[0] + infos[1]):
            to = edges[i][1]
            w = edges[i][2]["length"]
            if (to in dist):
                if (dist[to][0] > dist[cur][0] + w):
                    dist[to] = [dist[cur][0] + w, cur]
            else:
                todo.append(to)
                dist[to] = [dist[cur][0] + w, cur]
            i += 1


def eulerization_directed(edges, graph = None):
    paths_to_create = []
    lgt = len(edges)
    dict = create_dict_edges_degrees(edges, lgt)
    offering = []
    demanding = []
    vertices = []
    i = 0
    while (i < lgt):
        vert = edges[i][0]
        vertices.append(vert)
        cur = dict[vert]
        if (cur[2] < 0):
            offering.append(vert)
        elif (cur[2] > 0):
            demanding.append(vert)
        i += cur[1]

    while (len(offering)):
        paths_to_create.append(djikstra_wparent(edges, offering[0], demanding, vertices, dict,  graph))
        dict[offering[0]][2] += 1
        if (dict[offering[0]][2] == 0):
            offering.pop(0)

    return paths_to_create


def create_dict_edges(edges):
    res = {}
    i = 0
    lgt = len(edges)

    while (i < lgt):
        cur_v = edges[i][0]
        begin = i
        while (i < lgt and cur_v == edges[i][0]):
            i += 1
        res[cur_v] = [begin, i - begin]
    
    return res


# HIERHOLZER
def eulerian_circuit(edges):
    stack = []
    if (len(edges) > 0):
        stack.append(edges[0][0])
    top = edges[0][0]
    res = []
    dict = create_dict_edges(edges)
    marked_vert = [False for i in range(len(edges))]

    while(len(stack)):
        next = dict[top][0]
        cur_lgt = next + dict[top][1]
        while (next < cur_lgt and marked_vert[next] == True):
            next += 1
        
        if (next < cur_lgt):
            stack.append(edges[next][1])
            top = edges[next][1]
            marked_vert[next] = True
        else:
            res.insert(0, stack.pop())
            if (len(stack)):
                top = stack[len(stack) - 1]
    return res


def nodes_to_edges(nodes, l):
    edges = []
    dic = create_dict_edges(l)

    for i in range(len(nodes) - 1):
        edges.append((nodes[i], nodes[i+1], my_find_weight(nodes[i],nodes[i+1], l)))
    return edges


def isin(G, a, b, c):
    for x,y,z in G.edges(data=True):
        print(z)
        print(c)
        if (x,y,z) == (a,b,c):
            return True
    return False    


def nb_km(L):
    res = 0
    for a,b,poid in L:
        res += poid
    return res


def decoupe(edges, n):
    res = []
    for i in range(n):
        res.append([])
    tmp = 0
    nbkm = nb_km(edges)
    ind = 0
    for a,b,c in edges:
        if (tmp >= (nbkm / n)):
            tmp = 0
            if (ind < n - 1):
                ind += 1

        res[ind].append((a,b))
        tmp += c
    return res


def couleurchemin(L, G):
    res = 0
    couleur = ['#FFFFFF'] * G.number_of_edges()
    i = 0
    for a,b,c in G.edges(data=True):
        if ((a,b) in L):
            res += 1
            couleur[i] = '#E67E30'
        i += 1
    return couleur
