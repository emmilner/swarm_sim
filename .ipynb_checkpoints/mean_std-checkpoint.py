import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
graphs = 2
task = 2
if graphs == 1:
	fig, ax = plt.subplots()
	df =  pd.read_csv('stand_dev_and_mean.csv')
	a = np.linspace(1,600,100)
	b = np.linspace(1,50,100)
	ax.plot(b,a,'red')
	#x1 = df.plot.area(x="150box", y=["task2","Min2","Max2"]#,kind="line"
	#			 ,subplots=False)
	#x1 =  df.plot(x="150box", y=["task2","Min2"],kind="line" ,subplots=True)
	#x1.fill_between(x1[0],x1[1])
	#sns.relplot(x="boxNum", y="time", col="task",hue="bias", kind="line", 
	#			ci=None, data=df)
	plt.fill_between(df['boxNum'],df['Min1'],df['Max1'],facecolor="blue",alpha=0.2)
	ax.plot(df['150box'],df['t1avg'],color="blue")

	#plt.fill_between(df['boxNum'],df['Min2b'],df['Max2b'],facecolor="green",alpha=0.2)
	#ax.plot(df['150box'],df['t2bavg'],color="green")
	ax.grid(True)
	plt.title("Ordered task",fontsize=15)
	plt.xlabel("Box number",fontsize=15)
	plt.ylabel("Time (s)",fontsize=15)
	plt.legend(["Amazon estimate","Mean time", "All results"],loc='upper left')

if graphs == 2:
	fig, ax = plt.subplots(nrows=1,ncols=2)#,sharex=True,sharey=True)
	df =  pd.read_csv('stand_dev_and_mean.csv')
	if task == 1:
		fill =ax[0].fill_between(df['boxNum'],df['Min1'],df['Max1'],facecolor="black",alpha=0.2)
		ax[0].plot(df['150box'],df['t1avg'],color="black")
		ax[1].fill_between(df['boxNum'],df['Min1b'],df['Max1b'],facecolor="black",alpha=0.2)
		ax[1].plot(df['150box'],df['t1bavg'],color="black")
		ax[1].set_title('Unordered task with bias')
		ax[0].set_title('Unordered task')
		a = np.linspace(1,600,100)
		b = np.linspace(1,50,100)
	if task == 2:
		fill=ax[0].fill_between(df['boxNum'],df['Min2'],df['Max2'],facecolor="black",alpha=0.2)
		ax[0].plot(df['150box'],df['t2avg'],color="black")
		ax[1].fill_between(df['boxNum'],df['Min2b'],df['Max2b'],facecolor="black",alpha=0.2)
		ax[1].plot(df['150box'],df['t2bavg'],color="black")
		ax[1].set_title('Ordered task with bias')
		ax[0].set_title('Ordered task')
		a = np.linspace(900,900,100)
		b = np.linspace(1,50,100)
	#ax[0].plot(b,a,'red',linestyle='dashed')
	#ax[1].plot(b,a,'red',linestyle='dashed')
	ax[0].set_xlabel('Box number')
	ax[1].set_xlabel('Box number')
	ax[0].set_ylabel('Time taken (s)')
	#ax[1].set_ylabel('Time taken (s)')
	ax[0].grid(True)
	ax[1].grid(True)
	ax[0].legend(["Mean time",
				  #"Amazon estimate",
				  "All results"],
				 loc='upper left')
	#ax[1].legend(["Amazon estimate","Mean time", "All results"],ncol=3,loc='best')


plt.show()