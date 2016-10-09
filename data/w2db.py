#encoding=utf-8
import pymongo
import random

conn = pymongo.MongoClient('localhost',27017)
db = conn['competition']

def insert_label():
	LabelCol = db["label"]
	with open("Label.csv") as f:
		data = f.read()
		data = data.split("\n")[1:-1]
		for d in data:
			id,view,op = d.split("\t")
			op = op.strip("\r")
			LabelCol.insert({"id":id,"view":view,"opinion":op})
	f.close()

def insert_train():
	TrainCol = db["train"]
	with open("Train.csv") as f:
		data = f.read()
		data = data.split("\n")[1:-1]
		for d in data:
			id,content = d.split("\t")
			content = content.strip("\r")
			TrainCol.insert({"id":id,"content":content})
	f.close()

def insert_test():
	TestCol = db["test"]
	with open("Test.csv") as f:
		data = f.read()
		data = data.split("\n")[1:-1]
		for d in data:
			id,content = d.split("\t")
			content = content.strip("\r")
			TestCol.insert({"id":id,"content":content})
	f.close()

# car dict 
def insert_view():
	ViewCol = db["view"]
	with open("View.csv") as f:
		data = f.read()
		data = data.split("\n")[1:-1]
		for d in data:
			id,view = d.split("\t")
			view = view.strip("\r")
			ViewCol.insert({"id":id,"view":view})
	f.close()


# build a dict file for tokenization
def build_dict():
	result = []
	ViewCol = db["view"]
	data = ViewCol.find()
	for d in data:
		view = d["view"]
		result.append(view.encode("utf-8") + " 10\n")
	f = file("userdict.txt","w")
	f.writelines(result)
	f.close()

def split_data():
	idx = []
	factor = 9
	TrainCol = db["train"]
	data = TrainCol.find()
	for d in data:
		id = d["id"]
		idx.append(id)
	random.shuffle(idx)
	train,valid = idx[:int((1.0*factor/(factor+1))*len(idx))],idx[int((1.0*factor/(factor+1))*len(idx)):]
	return train,valid

def build_data():
	train,valid = split_data()
	T = db["T"]
	V = db["V"]
	TrainCol = db["train"]
	data = TrainCol.find()
	for d in data:
		id = d["id"]
		if id in train:
			T.insert(d)
		else:
			V.insert(d)
