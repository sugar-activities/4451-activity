#load_save.py
import g

loaded=[] # list of strings

def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except:
        pass

def save(f):
    for ind in range(12):
        f.write(str(g.best[ind])+'\n')

# note need for rstrip() on strings
def retrieve():
    global loaded
    if len(loaded)>0:
        for ind in range(12):
            g.best[ind]=int(loaded[ind])


    
