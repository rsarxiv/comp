#encoding=utf-8
import pymongo
import random

conn = pymongo.MongoClient('localhost',27017)
db = conn['competition']

classes = {"pos":"1","neg":"2","neu":"3"}
rev_classes = {"1":"pos","2":"neg","3":"neu"}

def build_data():
	#format: id,view,content,opnion
	train_file = file("train.data","w")
	valid_file = file("valid.data","w")
	T = db["T"]
	V = db["V"]
	train_data = T.find()
	test_data = V.find()
	for data in train_data:
		opinion = data["opinion"] # list
		view = data["view"] # list
		_content = data["content"] # tokenization done!
		content = [c.encode("utf-8") for c in _content]
		for index,op in enumerate(opinion):
			v = view[index]
			content = " ".join(content)
			train_file.write("__label__" + classes[op] + " , " + v.encode("utf-8") + " , " + content + "\n")
	for data in test_data:
		opinion = data["opinion"] # list
		view = data["view"] # list
		_content = data["content"] # tokenization done!
		content = [c.encode("utf-8") for c in _content]
		for index,op in enumerate(opinion):
			v = view[index]
			content = " ".join(content)
			valid_file.write("__label__" + classes[op] + " , " + v.encode("utf-8") + " , " + content + "\n")
	train_file.close()
	valid_file.close()

def build_train_data():
	#format: id,view,content,opnion
	train_file = file("train.data","w")
	TrainCol = db["train"]
	train_data = TrainCol.find()
	for data in train_data:
		opinion = data["opinion"] # list
		view = data["view"] # list
		_content = data["content"] # tokenization done!
		content = [c.encode("utf-8") for c in _content]
		for index,op in enumerate(opinion):
			v = view[index]
			content = " ".join(content)
			train_file.write("__label__" + classes[op] + " , " + v.encode("utf-8") + " , " + content + "\n")
	train_file.close()

import jieba
import jieba.posseg as pseg
import CRFPP

def processing():
	jieba.load_userdict("../../../data/userdict.txt")
	tagger = CRFPP.Tagger("-m ../../NER/train/model")
	TestCol = db["test"]
	data = TestCol.find()
	try:
		for d in data:
			view = []
			content = d["content"]
			# _content = []
			words = pseg.cut(content)
			for w in words:
				tag = w.word.encode("utf-8") + " " + w.flag.encode("utf-8")
				# _content.append(w.word)
				tagger.add(tag)
			tagger.parse()
			ysize = tagger.ysize()
			size = tagger.size()
			xsize = tagger.xsize()
			for i in range(size):
				if tagger.y2(i) == "Y":
					view.append(tagger.x(i,0))
			d["view"] = view
			# d["content"] = _content
			TestCol.save(d)
			tagger.clear()

	except RuntimeError, e:
		print "RuntimeError: ", e,

# build_train_data()

# processing()

def build_test_data():
	#format: id,view,content,opnion
	test_file = open("test.data","w") 
	TestCol = db["test"]
	test_data = TestCol.find()
	for data in test_data:
		view = data["view"] # list
		_content = data["content"] # tokenization done!
		content = [c.encode("utf-8") for c in _content]
		for index,v in enumerate(view):
			content = " ".join(content)
			test_file.write(v.encode("utf-8") + " , " + content + "\n")
	test_file.close()


def output():
	#format: id,view,opinion
	f = open("result.csv","w")
	classes_file = open("result.txt","r")
	_classes = classes_file.read().split("\n")[:-1]
	count = 0
	TestCol = db["test"]
	test_data = TestCol.find()
	for data in test_data:
		id = data["id"]
		view = data["view"]
		opinion = []
		for v in view:
			_class = rev_classes[_classes[count][-1]]
			opinion.append(_class)
			text = id.encode("utf-8") + "," + v.encode("utf-8") + "," + _class.encode("utf-8") + "\n"
			count += 1
			f.write(text)
		data["opinion"] = opinion
		TestCol.save(data)
	f.close()

def show():
	TestCol = db["test"]
	count = TestCol.find().count()
	randn = random.randint(0,count)
	result = TestCol.find().limit(-1).skip(randn).next()
	content = result["content"]
	view = result["view"]
	opinion = result["opinion"]
	print content
	for i,v in enumerate(view):
		print v,opinion[i]


# while True:
# 	show()
# 	raw_input()





