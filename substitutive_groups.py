# a group is: (generators, product func, inverse func, identity, equality func)
# we represent its elements as whatever format the group uses internally, or
# as strings over free group on a, b, c... with upper case versions as inverses

# a graph is just a list of edges, assume no isolated nodes
# actually, let's say a graph is two dicts

# we use these as names of labels

letters = "abcdefghijklmnopqrstuvwxyz"

infinity = 1000000000000000000000000

def substitute(sub, graph, same_label_identify = True):

    nodes = get_nodes(graph)    
    edges = graph
    
    G = sub[0]
    nG = get_nodes(G)
    # gammas (and their s's and t's) for different edge labels
    Gammas = sub[1:]
    
    new_edges = []
    
    # make completely new copies of the graphs for all edges
    for e in edges:
        Gamma, s, t = Gammas[letters.index(e[2])]
        for ee in Gamma:
            new_edges.append(((e,ee[0]), (e,ee[1]), ee[2]))

    eq_rel = trivial_partition(get_nodes(new_edges))
    for n in nodes:
        #print(eq_rel)
        #print("identifying for", n)
        # source identifications
        outgoings = list(outs(n, edges))
        if len(outgoings) > 0:
            #print("outgoing", outgoings)
            first = outgoings[0]
            Gamma1, s1, t1 = Gammas[letters.index(first[2])]
            for e in outgoings[1:]:
                Gamma, s, t = Gammas[letters.index(e[2])]
                for g in nG:
                    infirst = (first, s1(g))
                    ine = (e, s(g))
                    identify(eq_rel, infirst, ine)
        # target identifications
        incomings = list(ins(n, edges))
        if len(incomings) > 0:
            #print("incoming", incomings)
            first = incomings[0]
            Gamma1, s1, t1 = Gammas[letters.index(first[2])]
            for e in incomings[1:]:
                Gamma, s, t = Gammas[letters.index(e[2])]
                for g in nG:
                    infirst = (first, t1(g))
                    ine = (e, t(g))
                    #print("id", infirst, ine)
                    identify(eq_rel, infirst, ine)
        # sources and targets...
        for i in incomings:
            Gammai, si, ti = Gammas[letters.index(i[2])]
            for o in outgoings:
                Gammao, so, to = Gammas[letters.index(o[2])]
                for g in nG:
                    ini = (i, ti(g))
                    ino = (o, so(g))
                    #print("IDISDF", ini, ino)
                    identify(eq_rel, ini, ino)
                
    """
    actually = []
    for k in ret_edges:
        a, b, l = k
        #actually.append(((a, frozenset(eq_rel[a])), (b, frozenset(eq_rel[b])), l))
        actually.append((a, b, l))
    return actually
    """

    #print(eq_rel)

    # eq_rel indices are the new node names, compute them in dict form
    name_dict = {}
    for e in new_edges:
        for i,p in enumerate(eq_rel):
            if e[0] in p:
                name_dict[e[0]] = i
            if e[1] in p:
                name_dict[e[1]] = i

    ret_edges = []
    for e in new_edges:
        v0 = name_dict[e[0]]
        v1 = name_dict[e[1]]
        label = e[2]
        put = (v0, v1, label)
        if put in ret_edges:
            #raise Exception("Duplicate edge")
            continue
        ret_edges.append(put)
        
    final_nodes = get_nodes(ret_edges)
    
    #return ret_edges
    #  sanity check
    if not same_label_identify:
        
        for n in final_nodes:
            for o in outs(n, ret_edges):
                for p in outs(n, ret_edges):
                    if o[2] == p[2] and o != p:
                        raise Exception("Node %s has two outgoing edges with label %s" % (n, o[2]))
                        
            for o in ins(n, ret_edges):
                for p in ins(n, ret_edges):
                    if o[2] == p[2] and o != p:
                        raise Exception("Node %s has two incoming edges with label %s" % (n, o[2]))

    # keep identifying in ret_edges graph...
    else:
        final_rel = trivial_partition(final_nodes)
        for n in final_nodes:
            for o in outs(n, ret_edges):
                for p in outs(n, ret_edges):
                    if o[2] == p[2] and o != p:
                        identify(final_rel, o[1], p[1])
                        
            for o in ins(n, ret_edges):
                for p in ins(n, ret_edges):
                    if o[2] == p[2] and o != p:
                        identify(final_rel, o[0], p[0])

        name_dict = {}
        for e in ret_edges:
            for i,p in enumerate(final_rel):
                if e[0] in p:
                    name_dict[e[0]] = i
                if e[1] in p:
                    name_dict[e[1]] = i

        actual_ret_edges = []
        for e in ret_edges:
            v0 = name_dict[e[0]]
            v1 = name_dict[e[1]]
            label = e[2]
            put = (v0, v1, label)
            if put in actual_ret_edges:
                #raise Exception("Duplicate edge")
                continue
            actual_ret_edges.append(put)
        ret_edges = actual_ret_edges

    return ret_edges
                
    
def trivial_partition(s):
    parts = []
    for a in s:
        parts.append(set([a]))
    return parts

def identify(rel, a, b):
    ai = None
    bi = None
    for i,s in enumerate(rel):
        if a in s:
            ai = i
        if b in s:
            bi = i
        if ai != None and bi != None:
            break
    if ai == None:
        raise Exception("Cannot identify %s with %s as former is not in the partition." % (a, b))
    if bi == None:
        raise Exception("Cannot identify %s with %s as latter is not in the partition." % (a, b))
    if ai == bi:
        return
    rel[ai].update(rel[bi])
    del rel[bi]

def outs(node, edges):
    for e in edges:
        if e[0] == node:
            yield e

def ins(node, edges):
    for e in edges:
        if e[1] == node:
            yield e
    
def get_nodes(edges):
    ns = set()
    for e in edges:
        ns.add(e[0])
        ns.add(e[1])
    return ns

def Zdprod(a, b):
    return tuple(i+j for (i,j) in zip(a,b))
def Zdinv(a):
    return tuple(-i for i in a)
def Zddid(d):
    return (0,)*d
def Zdeq(a, b):
    return a == b


import LL
ll =LL.from_word
#b = lamplighter.getniceLLbal(2)
#print(b)
#a = B
lampgens = [ll("a"), ll("b")]
lampprod = lambda a, b:LL.prod(a, b)
lampinv = LL.invert
lampid = ll("")
lampeq = lambda a, b: a == b ###LL.from_word(a) == LL.from_word(b) # probably unique reprs but anyway


#print(lampprod("aAbaB", ""))

def connected(graph):
    nodes = list(get_nodes(graph))
    n = nodes[0]
    founds = set([n])
    frontier = set([n])
    while frontier:
        newfrontier = set()
        for f in frontier:
            for e in graph:
                if f == e[0] and e[1] not in founds:
                    newfrontier.add(e[1])
                    founds.add(e[1])
                if f == e[1] and e[0] not in founds:
                    newfrontier.add(e[0])
                    founds.add(e[0])
        frontier = newfrontier
    if len(founds) < len(nodes):
        return False
    return True

# stupid upper bound on diameter of connected graph
def diameter_from(origin, graph):
    nodes = get_nodes(graph)
    founds = set([origin])
    frontier = set([origin])
    diameter = -1
    while frontier:
        newfrontier = set()
        for f in frontier:
            for e in graph:
                if f == e[0] and e[1] not in founds:
                    newfrontier.add(e[1])
                    founds.add(e[1])
                if f == e[1] and e[0] not in founds:
                    newfrontier.add(e[0])
                    founds.add(e[0])
        frontier = newfrontier
        diameter += 1
    return diameter

def maxdepth(graph, outdeg, indeg = None):
    if indeg == None:
        indeg = outdeg
    depths = get_depths(graph, outdeg, indeg)
    return max(depths.values())
        
def get_depths(graph, outdeg, indeg = None):
    if indeg == None:
        indeg = outdeg
    nodes = get_nodes(graph)
    depths = {n:infinity for n in nodes}
    while True:
        changed = False
        for n in nodes:
            if depths[n] == 0:
                continue

            put = infinity
            
            if len(list(outs(n, graph))) < outdeg:
                put = 0
            if len(list(ins(n, graph))) < indeg:
                put = 0
            
            if depths[n] > put:
                depths[n] = put
                changed = True
                continue

            for o in outs(n, graph):
                fol = o[1]
                put = min(put, depths[fol] + 1)

            for i in ins(n, graph):
                pre = i[0]
                put = min(put, depths[pre] + 1)

            if depths[n] > put:
                depths[n] = put
                changed = True

        if not changed:
            break
    return depths

# return ball as iterable of generator strings and elements
def ball_graph(group, diam):
    gens, prod, inv, ide, eq = group
    #yield ("", ide)
    reprs = {ide : ""}
    #if diam == 0:
    #    yield ide
    #    return
    knowns = set([ide])
    frontier = [ide]
    for i in range(diam):
        newfrontier = []
        for f in frontier:
            for a in letters[:len(gens)]:
                symi = letters.index(a)
                for (s, g) in [(letters[symi], gens[symi]), (letters[symi].upper(), inv(gens[symi]))]:
                    new = prod(f, g)
                    if new in knowns:
                        continue
                    knowns.add(new)
                    newfrontier.append(new)
                    reprs[new] = reprs[f] + s
        frontier = newfrontier
    for f in reprs:
        yield reprs[f], f

# follow labeled path in graph
def follow(gen_str, origin, graph):
    curr = origin
    for a in gen_str:
        curr = step(curr, a, graph)
        if curr == None:
            break
    return curr

def step(curr, a, graph):
    if a.islower():
        for o in outs(curr, graph):
            if o[2] == a:
                return o[1]
    if a.isupper():
        for i in ins(curr, graph):
            if i[2] == a.lower():
                return i[0]
    return None                    

def contains(group, graph):
    gens, prod, inv, id, eq = group
    if not connected(graph):
        return False
    
    nodes = list(get_nodes(graph))
    origin = nodes[0]

    diam = diameter_from(origin, graph)
    ball = ball_graph(group, diam)

    # pretend origin is origin of group, and see if we have a subgraph
    elems = {}
    used = set()
    for b in ball:
        gen_str, elem = b
        nod = follow(gen_str, origin, graph)
        if nod == None:
            continue
        elems[nod] = elem
        if elem in used:
            raise Exception("Elem in used")
        used.add(elem)

    for e in graph:
        s, t, l = e
        if l.islower():
            gen = gens[letters.index(l)]
        else:
            gen = inv(gens[letters.index(l.lower())])
        #try:
        if s not in elems or t not in elems: #assert s in elems
            return False
        tshould = prod(elems[s], gen)
            #print (elems[s], gen)
        #except:
        #    prod (elems[s], gen)
        #    raise Exception("awh")
        if not eq(tshould, elems[t]):
            raise Exception("%s should be %s" % (tshould, elems[t]))

    # now compute
    return True

def has_doubles(graph):
    nodes = get_nodes(graph)
    for n in nodes:
        for o in outs(n, graph):
            for p in outs(n, graph):
                if o[2] == p[2]:
                    if o != p:
                        return True
        for o in ins(n, graph):
            for p in ins(n, graph):
                if o[2] == p[2]:
                    if o != p:
                        return True
    return False

# to two-dict format
def td(edges):
    return edges
    forws = {}
    backs = {}
    for e in edges:
        if e[0] in forws[e[2]]:
            assert forws[e[2]][e[0]] == e[1]
        forws[e[2]][e[0]] = e[1]
        if e[1] in backs[e[2]]:
            assert backs[e[2]][e[0]] == e[1]
        forws[e[2]][e[0]] = e[1]
# Z2 example...
"""
Z2 = ([(1,0), (0,1)], Zdprod, Zdinv, (0,0), Zdeq)
G = [((0,0), (1,0), "a"),
     ((0,0), (0,1), "b"),
     ((1,0), (1,1), "b"),
     ((0,1), (1,1), "a")]
Gamma_a = [((0,0), (1,0), "a"),
     ((0,0), (0,1), "b"),
     ((1,0), (1,1), "b"),
     ((0,1), (1,1), "a"),
     ((2,0), (2,1), "b"),
     ((1,0), (2,0), "a"),
     ((1,1), (2,1), "a")]
Gamma_b = [((0,0), (1,0), "a"),
     ((0,0), (0,1), "b"),
     ((1,0), (1,1), "b"),
     ((0,1), (1,1), "a"),
     ((0,2), (1,2), "a"),
     ((0,1), (0,2), "b"),
     ((1,1), (1,2), "b")]
s_a = lambda x:x
s_b = lambda x:x
t_a = lambda x:Zdprod(x, (1,0))
t_b = lambda x:Zdprod(x, (0,1))
sub = (G, (Gamma_a, s_a, t_a), (Gamma_b, s_b, t_b))
"""

def as_graph(group, Gset):
    generators = group[0]
    prod = group[1]
    eq = group[4]
    edges = []
    for g in Gset:
        for h in Gset:
            for i,gen in enumerate(generators):
                #print("g",g,"h", h, prod(g, gen))
                if eq(prod(g, gen), h):
                    edges.append((g, h, letters[i]))
    #a = bbb
    return edges

# lamplighter example
group = (lampgens, lampprod, lampinv, lampid, lampeq)
"""
G = [(ll(""), ll("a"), "a"),
     (ll(""), ll("b"), "b"),
     (ll("aB"), ll("b"), "a"),
     (ll("aB"), ll("a"), "b")]
"""
Gset = set(ll(g) for g in ["", "a", "b", "aB"])
print(Gset)
G = as_graph(group, Gset)
#print(G)
#a = bbb

G = td(G)
ll = LL.from_word
"""
Gamma_a = [(ll(""), ll("a"), "a"),
           (ll(""), ll("b"), "b"),
           (ll("aB"), ll("b"), "a"),
           (ll("aB"), ll("a"), "b"),
           (ll("a"), ll("aa"), "a"),
           (ll("a"), ll("ab"), "b"),
           (ll("aaB"), ll("aa"), "b"),
           (ll("aaB"), ll("ab"), "a")]
"""
Gamma_a_set = set(Gset)
Gamma_a_set.update(set(lampprod(ll("a"), g) for g in Gset))
#Gamma_a_set = set(ll(g) for g in Gamma_a_set)#["", "a", "b", "aB", "aa", "aaB", "ab"])
Gamma_a = as_graph(group, Gamma_a_set)    
#Gamma_a = td(Gamma_a)

"""
Gamma_b = [(ll(""), ll("a"), "a"),
           (ll(""), ll("b"), "b"),
           (ll("aB"), ll("b"), "a"),
           (ll("aB"), ll("a"), "b"),
           (ll("b"), ll("ba"), "a"),
           (ll("b"), ll("bb"), "b"),
           (ll("baB"), ll("ba"), "b"),
           (ll("baB"), ll("bb"), "a")]
Gamma_b = td(Gamma_b)
"""
Gamma_b_set = set(Gset)
Gamma_b_set.update(lampprod(ll("baB"), g) for g in Gset)
#Gamma_b_set = set(ll(g) for g in Gamma_b_set) #["", "a", "b", "aB", "ba", "baB", "bb"])
Gamma_b = as_graph(group, Gamma_b_set)
s_a = lambda x:x
s_b = lambda x:x
t_a = lambda x:lampprod(LL.from_word("a"), x)
t_b = lambda x:lampprod(LL.from_word("baB"), x)

"""
# bs example 
#group = (bsgens, bsprod, bsinv, lampid, lampeq)
G = [("", "a", "a"),
     ("a", "aa", "a"),
     ("aa", "aaa", "a"),
     ("", "b", "b"),
     ("b", "ba", "a"),
     ("a", "ab", "b"),
     ("ab", "aba", "a"),
     ("aa", "ba", "b"),
     ("aaa", "aba", "b")]

Gamma_a = [("", "a", "a"),
     ("a", "aa", "a"),
     ("aa", "aaa", "a"),
     ("", "b", "b"),
     ("b", "ba", "a"),
     ("a", "ab", "b"),
     ("ab", "aba", "a"),
     ("aa", "ba", "b"),
     ("aaa", "aba", "b"),
           
     ("aaa", "aaaa", "a"),
     ("ba", "baa", "a"),
     ("aaaa", "baa", "b")]

s_a = lambda x:x
t_a = lambda a:{"":"a", "a":"aa", "aa":"aaa", "aaa":"aaaa",
                "b":"ab", "ab":"ba", "ba":"aba", "aba":"baa"}[a]

Gamma_b = [("", "a", "a"),
     ("a", "aa", "a"),
     ("aa", "aaa", "a"),
     ("", "b", "b"),
     ("b", "ba", "a"),
     ("a", "ab", "b"),
     ("ab", "aba", "a"),
     ("aa", "ba", "b"),
     ("aaa", "aba", "b"),
           
     ("b", "bb", "b"),
     ("bb", "bba", "a"),
     ("ba", "bab", "b"),
     ("bab", "baba", "a"),
     ("baa", "bba", "b"),
     ("ba", "baa", "a"),
     ("baa", "baaa", "a"),
     ("baaa", "baba", "b")]

s_b = lambda x:x
t_b = lambda a:{"":"b", "a":"ba", "aa":"baa", "aaa":"baaa",
                "b":"bb", "ab":"bab", "ba":"bba", "aba":"baba"}[a]
"""

curr = G
sub = (G, (Gamma_a, s_a, t_a), (Gamma_b, s_b, t_b))
for i in range(7):
    curr = substitute(sub, curr, True)
    print(len(curr))
    print(has_doubles(curr))
    print("Group contains the graph:", contains(group, curr))
    print(maxdepth(curr, 2))
    print()
    #print(has_double_edges(curr))
#for c in curr:
#    print(c)
    #ab = Bbb
    #print("Group contains the graph:", contains(group, curr))
    #print("Maximal depth of a node:", maxdepth(curr, 2))





