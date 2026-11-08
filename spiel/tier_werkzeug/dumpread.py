import numpy as np
def m16(line):
    v=[float(x) for x in line.split()]
    return np.array(v).reshape(4,4)
def lese(pfad):
    L=open(pfad).read().split("\n")
    i=0
    n=int(L[0].split()[1]); i=1
    names=[];par=[]
    for k in range(n):
        a,b=L[i].split(); names.append(a); par.append(int(b)); i+=1
    assert L[i]=="OFFSET"; i+=1
    off=[m16(L[i+k]) for k in range(n)]; i+=n
    assert L[i]=="BIND"; i+=1
    bind=[m16(L[i+k]) for k in range(n)]; i+=n
    clips={}
    verts=None
    el=None
    while i<len(L) and L[i]:
        if L[i].startswith("CLIP"):
            _,nm,dur,cnt=L[i].split(); i+=1
            nok=L[i].split()[1:]; i+=1
            T=[];M=[];LOC=[]
            for c in range(int(cnt)):
                T.append(float(L[i].split()[1])); i+=1
                ms=np.zeros((n,4,4)); lo={}
                for b in range(n):
                    if L[i].startswith("L "):
                        p=L[i].split(); lo[int(p[1])]=[float(x) for x in p[2:]]; i+=1
                    ms[b]=m16(L[i]); i+=1
                M.append(ms); LOC.append(lo)
            clips[nm]=dict(dur=float(dur),T=np.array(T),M=np.array(M),L=LOC,nokeys=nok)
        elif L[i].startswith("ELEMENTS"):
            i+=1
            el=np.array([int(x) for x in L[i].split()]); i+=1
        elif L[i].startswith("VERTS"):
            nv=int(L[i].split()[1]); i+=1
            verts=np.array([[float(x) for x in L[i+k].split()] for k in range(nv)]); i+=nv
        else:
            i+=1
    return dict(names=names,par=par,off=np.array(off),bind=np.array(bind),clips=clips,verts=verts,el=el,idx={n_:k for k,n_ in enumerate(names)})
