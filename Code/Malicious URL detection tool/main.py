import pandas as pd
import numpy as np
import sklearn

import random
from tkinter import *
from tkinter import ttk 
import time

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

boolean= False
to_ret=[]


def getTkns(input):
	tknsBySlash= str(input.encode('utf-8')).split('/')
	allTkns= []
	for i in tknsBySlash:
		 tkns= str(i).split('-')
		 tknsByDot= []
		 for j in range(0, len(tkns)):
			 tempTkns= tkns[j].split('.')
			 tknsByDot= tknsByDot + tempTkns
		 allTkns= allTkns+tkns+tknsByDot
	 allTkns= list(set(allTkns))
	 # Since .com is most common domain, we actually don't need it.
	 if 'com' in allTkns:
		 allTkns.remove('com')
	 return allTkns


def trainer():
	global to_ret
	global txt

	# ONE TIME EXECUTION STARTS HERE
	csv= pd.read_csv("data.csv", error_bad_lines= False)
	data= pd.DataFrame(csv)
	```
	data= np.array(data)
	random.shuffle(data)

	y= [d[1] for d in data]
	corp= [d[0] for d in data]

	count_vectorizer= CountVectorizer(tokenizer= getTkns)
	tf_vectorizer= TfidfVectorizer(tokenizer= getTkns)

	X1= count_vectorizer.fit_transform(corp)
	X2= tf_vectorizer.fit_transform(corp)

	# Fit the Logistic Regression Model
	X1_train, X1_test, y1_train, y1_test= train_test_split(X1, y, test_size= 0.2, random_state= 42)
	X2_train, X2_test, y2_train, y2_test= train_test_split(X2, y, test_size= 0.2, random_state= 42)
	lgs_count= LogisticRegression()
	lgs_tf   = LogisticRegression()
	lgs_count.fit(X1_train, y1_train)
	lgs_tf.fit(X2_train,y2_train)

	out1= "The accuracy of Model with Count Vectorizer is "+str(lgs_count.score(X1_test, y1_test))+"\n"
	out2= "The accuracy of Model with TFIDF Vectorizer is "+str(lgs_tf.score(X2_test, y2_test))+"\n"
	txt.insert(0.0,out1)
	txt.insert(1.0,out2)


	to_ret.append(count_vectorizer)
	to_ret.append(tf_vectorizer)
	to_ret.append(lgs_count)
	to_ret.append(lgs_tf)
	return to_ret


     

def callback():

	global boolean
	global to_ret
	global txt
	global choice

	txtname= entry.get()
	if txtname=="":
		txt.insert(0.0,"Enter valid URL\n")
		return
	Choice= choice.get()
	if Choice == "":
		txt.insert(0.0,"Please choose any one of the two options.\n")
		return


	X_predict= [txtname]
    	if Choice=="CV":        
		X_predict= to_ret[0].transform(X_predict)
		y_predict= to_ret[2].predict(X_predict)
		out= str(txtname)+" is found "+str(y_predict)+"\n"
		txt.insert(0.0, out)
    	if Choice=="TF":        
		X_predict= to_ret[1].transform(X_predict)
		y_predict= to_ret[3].predict(X_predict)
		out= str(txtname)+" is found "+str(y_predict)+"\n"
		txt.insert(0.0, out)

  	return
    	


root= Tk()
choice= StringVar()
frame= ttk.Frame(root)
frame.pack()
frame.config(height= 600, width= 800)
frame.config(relief= RAISED)

label= ttk.Label(frame, text="Malicious URL Detection Tool")
label.config(foreground='#1aaedb',background='#dbbf23')
label.config(justify=CENTER)
label.config(font=('segoe',18,'bold'))
label.pack()

label2= ttk.Label(frame, text='\n\n')
label2.pack()

ttk.Radiobutton(frame,text='Use Count Vectorizer',variable=choice,value='CV').pack(anchor='w')
label3= ttk.Label(frame, text='\n')
label3.pack()

ttk.Radiobutton(frame,text='Use Tf-Idf Vectorizer',variable=choice,value='TF').pack(anchor='w')
label4= ttk.Label(frame, text='\n')
label4.pack()

label5= ttk.Label(frame, text='Enter any valid URL to Check')
label5.pack()

to_check= StringVar()
entry= ttk.Entry(frame,textvariable=to_check,width=60)
entry.pack()



label5= ttk.Label(frame, text='\n')
label5.pack()

progressbar= ttk.Progressbar(frame,orient= HORIZONTAL,length=200)
progressbar.pack()
progressbar.config(mode= 'indeterminate')


button= ttk.Button(frame,text='Check',command=callback).pack()


txt= Text(frame,height=10, wrap= WORD)
txt.pack()
trainer()
root.mainloop()
