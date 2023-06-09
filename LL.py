def to_word(CC):
    if type(CC) == str:
        #a = bbb
        return CC
    cl, cr, t = CC
    # move head to correct place
    if t >= 0:
        w = "a"*t
    else:
        w = "A"*(-t)
    for d in reversed(cl):
        if d == 0:
            w += "B"
        else:
            w += "A"
    w += "b"*len(cl)
    for d in cr:
        if d == 0:
            w += "b"
        else:
            w += "a"
    w += "B"*len(cr)
    return w

# IN THE LAMPLIGHTER, THIS IS HOW YOU GET NEIGHBORS
# lamplighter, moving head model; and head is between things
# cl = word to the left of the head, cr to the right
# t is position of head
# s = "a" or "b"
# d = direction, 1 or -1
# we always use words of minimal length so representation is uniq
def right_LLH(s, d, CC):
    cl, cr, t = CC
    if d == 1:
        if len(cr) == 0:
            cr = (0,)
        if s == "b":
            cl = cl + (1-cr[0],)
            cr = cr[1:]
        if s == "a":
            cl = cl + (cr[0],)
            cr = cr[1:]
        if cl == (0,):
            cl = ()
    if d == -1:
        if len(cl) == 0:
            cl = (0,)
        if s == "b":
            cr = (1 - cl[-1],) + cr
            cl = cl[:-1]
        if s == "a":
            cr = (cl[-1],) + cr
            cl = cl[:-1]
        if cr == (0,):
            cr = ()
    t += d
    return (cl, cr, t)

def from_word(w):
    #print(w)
    e = ((),(),0)
    for c in w:
        if c == "b":
            s = "b"
            d = 1
        if c == "B":
            s = "b"
            d = -1
        if c == "a":
            s = "a"
            d = 1
        if c == "A":
            s = "a"
            d = -1
        e = right_LLH(s,d,e)
    return e

# most ridiculous product for lamplighter group
def prod(a,b):
    w = to_word(a) + to_word(b)
    return from_word(w)

# sum two binary vectors, right-padded with zeroes
def rightplus(v1, v2):
    v1 = list(v1)
    v2 = list(v2)
    while len(v1) < len(v2):
        v1.append(0)
    while len(v2) < len(v1):
        v2.append(0)
    v = list(map(lambda AA:(AA[0]+AA[1])%2, zip(v1, v2)))
    while len(v) > 0 and v[-1] == 0:
        v = v[:-1]
    return tuple(v)

def leftplus(v1,v2):
    return tuple(reversed(rightplus(reversed(v1), reversed(v2))))

# this is the left action, if the right cayley
# graph is drawn as the above commented out thing
def LLH(s, d, CC):
    cl, cr, t = CC

    #start = ((), (), 0)
    #start = right_LLH(s, d, start)
    
    if s == "b" and d == 1:
        start = [[0]*abs(t)+[1], [0]*abs(t), 1]
    elif s == "a" and d == 1:
        start = [[0]*abs(t), [0]*abs(t), 1]
    elif s == "b" and d == -1:
        start = [[0]*abs(t), [1]+[0]*abs(t), -1]
    elif s == "a" and d == -1:
        start = [[0]*abs(t), [0]*abs(t), -1]

    if t > 0:
        for i in range(t):
            start[0] = start[0] + [start[1][0]]
            start[1] = start[1][1:]
    if t < 0:
        for i in range(-t):
            start[1] = [start[0][-1]] + start[1]
            start[0] = start[0][:-1]

    newl = leftplus(cl, start[0])
    newr = rightplus(cr, start[1])
    newt = start[2] + t

    return (newl, newr, newt)

def invert_as_word(w):
    #w = to_word(b)
    ret = ""
    for a in reversed(w):
        if a.isupper():
            ret += a.lower()
        else:
            ret += a.upper()
    return ret

def invert(g):
    return from_word(invert_as_word(to_word(g)))
	
LLHo = ((),(),0)


def getniceLLbal(size):
    ems = {LLHo: ""}
    for i in range(size):
        newems = {}
        for a in ems:
            newems[a] = ems[a]
        for elem in ems:
            for d in ["a","b","A","B"]:
                ab = d.lower()
                dr = d in "ab" and 1 or -1
                nxt = right_LLH(ab, dr, elem)
                if nxt not in newems: # or len(newems[nxt]) > len(name+d):
                    newems[nxt] = ems[elem] + d
        ems = newems
    return ems
	
	
	
	
