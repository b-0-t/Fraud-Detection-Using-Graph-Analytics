from collections import defaultdict
import numpy
import sys
import os
import subprocess

#network = sys.argv[1]


alpha1 = int(sys.argv[2])
alpha2 = int(sys.argv[3])

beta1 = int(sys.argv[4])
beta2 = int(sys.argv[5])

gamma1 = int(sys.argv[6])
gamma2 = int(sys.argv[7])
gamma3 = int(sys.argv[8])


f = open("../data/%s_gt.csv" % network,"r")
goodusers = set()
badusers = set()

for l in f:
    l = l.strip().split(",")
    if l[1] == "-1":
        badusers.add(l[0])
    else:
        goodusers.add(l[0])
f.close()
print(len(badusers), len(goodusers))


scores = defaultdict(list)
fnames = os.listdir("../results/")
for fname in fnames:
    if fname not in network:
        continue
    if "result" in fname:
        continue
    f = open("../results/%s/%s-fng-sorted-users-%s-%s-%s-%s-%s-%s-%s.csv" % (fname , fname,alpha1,alpha2,beta1,beta2,gamma1,gamma2,gamma3), "r")
    for l in f:
        l = l.strip().split(",")
        if l[1] == "nan":
                continue
        if l[2] == "nan":
                continue
        scores[l[0]].append(float(l[1]))


uniscores = {}
for score in scores:
    uniscores[score] = numpy.mean(scores[score])


import operator
sortedlist = sorted(uniscores.items(), key= lambda x: x[1])

fw = open("../results-combined/%s-mean-scores.csv" % network,"w")
for sl in sortedlist:
    fw.write("%s, %f\n" % (sl[0], float(sl[1]))) 
fw.close()


fnames = ["../results-combined/%s-mean-scores.csv" % (network)]
fww = open("../results-combined/%s-mean-scores-result.csv" % (network), "w")

for idx in range(len(fnames)):
    fname = fnames[idx]
    bashCommand = "wc -l %s" % fname
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    NLINES  = int(process.communicate()[0].decode().split(" ")[0])	#print fname
    Ys = []
    Ys2 = []
    X = []
    for NUSERS in range(1,250):
        i = -1
        f = open(fname,"r")

        c11 = 0
        c12 = 0
        c21 = 0
        c22 = 0
        x = 0
        for l in f:
            i +=1
            l = l.strip().split(",")
            if i < NUSERS:
                if l[0] in goodusers:
                    c11 += 1
                elif l[0] in badusers:
                    c12 += 1
            if i >= NLINES - NUSERS:
                x += 1
                if l[0] in goodusers:
                    c21 +=1
                elif l[0] in badusers:
                    c22 += 1
        f.close()
        print(c11, c12, c21, c22)
        X.append(c21+c22+1)
        Ys.append((c22+0.001)*1.0/(c21+c22+0.001))
        Ys2.append((c11+0.001)*1.0/(c11+c12+0.001))
    
    fww.write("%f, %f\n" % (float(numpy.mean(Ys)), float(numpy.mean(Ys2))))
    fww.close()

