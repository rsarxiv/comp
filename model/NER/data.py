#encoding=utf-8
import pymongo
import jieba
import jieba.posseg as pseg

conn = pymongo.MongoClient('localhost',27017)
db = conn['competition']

def build_crf_data(filename="T.data",_type="T"):
	# format: word/pos/label
	jieba.load_userdict("../../data/userdict.txt")
	f = open(filename,"w")
	T = db[_type]
	LabelCol = db["label"]
	data = T.find()
	for d in data:
		id = d["id"]
		content = d["content"].strip("\r")
		words = pseg.cut(content)
		labels = LabelCol.find({"id":id})
		views = []
		if labels:
			for label in labels:
				views.append(label["view"])
			for w in words:
				if w.word in views:
					f.write(w.word.encode('utf-8')+" "+w.flag.encode("utf-8")+" Y\n")
				else:
					f.write(w.word.encode('utf-8')+" "+w.flag.encode("utf-8")+" N\n")
	f.close()

build_crf_data("V.data",_type="V")