#-*- coding: utf-8 -*-
import subprocess
from csv import reader
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import pygal
import webbrowser
from flask import Flask, render_template, request
from pygal.style import Style
import random

application = Flask(__name__)

@application.route('/')
def land():
		file = open("~/titanic.csv", 'rU')
		header = file.readline()
		columnList = header.split(",")
		return render_template("index.html", columnList=columnList)

@application.route('/index', methods=['POST'])
def index():
        k = int(request.form["count"])
        column1 = int(request.form["column1"])
        column2 = int(request.form["column2"])

        color = []
        r = lambda:random.randint(0, 255)
        for i in range(0,k+1):
                color.append('#%02X%02X%02X' % (r(), r(), r()))

        colorTuple = tuple(color)
        customStyle = Style(colors=colorTuple)

        file = open("~/titanic.csv", 'rU')
	file.readline()
        data = []

        for line in enumerate(reader(file)):
                if len(line[1][column1]) > 0 and len(line[1][column2]) > 0:
                        data.append([float(line[1][column1]), float(line[1][column2])])

        dataNew = array(data)

        centroids,_ = kmeans(dataNew,k)
        idx,_ = vq(data,centroids)

        clusterPointMap = {}

	for i in range(0, k):
		clusterPointMap[i] = []

	for i, datum in enumerate(idx):
        	clusterPointMap[datum].append(tuple(dataNew[i]))
        
        xy_chart = pygal.XY(stroke=False, style=customStyle)
        xy_chart.title = 'Scatter plot'

	for i in range(0, k):
		xy_chart.add(str(i), clusterPointMap[i])

        centroidTuple = []
	for i in range(0, k):
		centroidTuple.append(tuple(centroids[i]))
        xy_chart.add('Centroids', centroidTuple)
        xy_chart.render_to_file("templates/p3.svg")
        return render_template("display.html")

def main():
        application.debug = True
        application.run(host='0.0.0.0', port=3030)

if __name__=='__main__': main()