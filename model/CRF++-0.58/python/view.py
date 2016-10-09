#!/usr/bin/python
#encoding=utf-8
import jieba
import jieba.posseg as pseg
import CRFPP
import sys

jieba.load_userdict("../../userdict.txt")

try:
    # -v 3: access deep information like alpha,beta,prob
    # -nN: enable nbest output. N should be >= 2
    tagger = CRFPP.Tagger("-m ../example/view/model_v1")

    # clear internal context
    tagger.clear()

    f2 = open("test.data","w")

    cars = []
    car_data = open("../../userdict.txt").read().split("\n")[:-1]
    for car in car_data:
        d = car.split(" ")
        if len(d) > 2:
            x = " ".join(d[:2])
        else:
            x = d[0]
        cars.append(x)

    # add context
    def test():
        with open("../../Test.csv") as f:
            data = f.read()
            data = data.split("\n")[1:-1]
            count = 1
            for d in data:
                id,content = d.split("\t")
                content = content.strip("\r")
                words = pseg.cut(content)
                for w in words:
                    tag = w.word.encode("utf-8") + " " + w.flag.encode("utf-8")
                    tagger.add(tag)
                tagger.parse()
                ysize = tagger.ysize()
                size = tagger.size()
                xsize = tagger.xsize()
                for i in range(size):
                    # if tagger.y2(i) == "Y":
                    # for j in range(xsize):
                    label = tagger.y2(i)
                    if label == "N":
                        if tagger.x(i,0) in cars:
                            label = "Y"
                            count += 1
                    f2.write(tagger.x(i,0) + " " + tagger.x(i,1) + " " + label + "\n")
                    #     print tagger.x(i, j) , " ",
                    # print tagger.y2(i) , "\n", 
                f2.write("===")
                # f2.write("\n")
                tagger.clear()
            print count

    test()
    f2.close()


except RuntimeError, e:
    print "RuntimeError: ", e,
