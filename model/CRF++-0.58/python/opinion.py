#!/usr/bin/python
#encoding=utf-8
import jieba
import jieba.posseg as pseg
import CRFPP
import sys

jieba.load_userdict("../../userdict.txt")

result = file("result-3.csv","w")

try:
    # -v 3: access deep information like alpha,beta,prob
    # -nN: enable nbest output. N should be >= 2
    tagger = CRFPP.Tagger("-m ../example/view/model_v2")

    # clear internal context
    tagger.clear()

    f1 = open("../../Test.csv")
    data = f1.read()
    data = data.split("\n")[1:-1]
    ids = []
    for d in data:
        id,_ = d.split("\t")
        ids.append(id)
    f1.close()

    # add context
    labels = ["pos","neg","neu"]
    def test():
        with open("test.data") as f:
            data = f.read()
            data = data.split("===")[:-1]
            count = 0
            for dd in data:
                ds = dd.split("\n")
                for d in ds:
                    tagger.add(d)
                tagger.parse()
                ysize = tagger.ysize()
                size = tagger.size()
                xsize = tagger.xsize()
                for i in range(0, (size - 1)):
                    if tagger.y2(i) in labels:
                        print ids[count],tagger.x(i,0),tagger.y2(i)
                        result.write(ids[count] + "," + tagger.x(i,0)+","+tagger.y2(i)+"\n")
                count += 1
                tagger.clear()
        result.write("\n")

    test()

except RuntimeError, e:
    print "RuntimeError: ", e,
