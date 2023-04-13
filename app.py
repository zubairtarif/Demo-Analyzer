from flask import Flask, render_template, request, flash
import pandas as pd
import numpy as np
import csv

app = Flask(__name__)
app.secret_key = "abc"

@app.route("/")
@app.route("/Analyzer")
def index():
	key_list = ['x', 'y']
	X, Y = [0],[0]
	datadict =  [dict(zip(key_list, (a,b))) for a,b in zip(X, Y)]
	datasend = str(datadict).replace("'","")
	xticksend = str(X).replace(" ",",")
	print(xticksend)
	print(datasend)
	print("Default is finished.")
	color_string = "3cba9f"
	return render_template("index.html", points=datasend, xticks=xticksend, colour=color_string) #because we saved an index file udner templates folder, flask will be able to find it

@app.route('/dummy')
def dummy():
	return '<h1>This is a dummy page</h1>'


@app.route('/load', methods=['POST'])
def load_data():
	if request.method == 'POST':
		csv_file = request.files['csv-file']

	load_datasend, load_xticksend = Process(csv_file)
	
	print("Starting Open File Tick")
	print(load_xticksend)
	print("Starting Open Data Send")
	print(load_datasend)
	return render_template("index.html", points=load_datasend, xticks=load_xticksend, colour="3cba9f") #because we saved an index file udner templates folder, flask will be able to find it


@app.route('/detect', methods=['POST'])
def detect():
	if request.method == 'POST':
		csv_file = request.files['csv-file']

	load_datasend, load_xticksend = Process(csv_file)
	
	print("Starting Open File Tick")
	print(load_xticksend)
	print("Starting Open Data Send")
	print(load_datasend)
	return render_template("index.html", points=load_datasend, xticks=load_xticksend, colour="3cba9f") #because we saved an index file udner templates folder, flask will be able to find it






def Process(filename):

	key_list = ['x', 'y']
	df = pd.DataFrame(filename)
	print("Dataframe Loaded")
	X, Y = makeXY(df)
	print("XY made")
	datadict =  [dict(zip(key_list, (a,b))) for a,b in zip(X, Y)]

	return_datasend = str(datadict).replace("'","")
	return_xticksend = str(X).replace("'","")

	return return_datasend, return_xticksend 

def makeXY(df_input):
	list_df = df_input.values.tolist()

	item_list =[str(s).replace("[b'","") for s in list_df]
	item_list =[str(s).replace("']","") for s in item_list]
	item_list =[s.replace('r','') for s in item_list]
	item_list =[s.replace('n','') for s in item_list]
	item_list =[s.replace('\\','') for s in item_list]

	newlist =[]
	for word in item_list:
		word = word.split(",")
		newlist.append(word)

	time = [z[0] for z in newlist]
	signal = [z[1] for z in newlist]
	#### cache this above data
	time = resize(time)
	signal = resize(signal)

	return time, signal


def resize(stream):
	length = len(stream)
	blocksize= 15
	block = int(length/blocksize)+1
	print("No. of Blocks:", block)
	newstream = []
	tempstream=[]
	for i in range(0, len(stream)-blocksize, blocksize):
		tempstream = [stream[i+c] for c in range(blocksize)]
		high = max(tempstream)
		newstream.extend([high])

	print(len(newstream))
	return newstream

if __name__ == "__main__":
	print("**** Flask server is starting. This message is shown in terminal. ****\n")
	app.run(port=7500)