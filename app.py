from flask import Flask, request, render_template, json, jsonify
import drs2box
import drs2tree
import sent2drs
from PIL import Image
import glob
import os
import base64
import cv2
import sys

app = Flask(__name__)

demo = sent2drs.Demo()

@app.before_first_request
def load():
	demo.load_model()

@app.route('/', methods=['GET', 'POST'])
def main_post():
	sent = ""
	msg = ""
	if request.method == 'POST':
		sent = request.form['sent']
		try:
			drs = demo.test(sent)
		except Exception as e:
			raise
		print drs
		filename = str(hash(drs.strip()))
		boxpath = "/disk/ocean/myuan/demos/drt/"+filename+".png"
		boxpdf = "/disl/ocean/myuan/demos/drt/"+filename+".pdf"
		treepath = "/disk/ocean/myuan/demos/drt/"+filename+"t.png"
		result = drs2box.drs2box(drs)
		if result == 0:
			msg += "Something went wrong when constructing the box graph! "
		try:
			timg = drs2tree.figure(5000,5000,drs2tree.refine(drs.split())) # cannot be used ion JSON yet
			cv2.imwrite(treepath,timg)
		except Exception as e:
			msg += "Something went wrong when constructing the tree graph! "
		if not os.path.isfile(boxpath):
			msg += "Something went wrong with the box graph path! "
			if not os.path.isfile(treepath):
				msg += "Something went wrong with the box graph path! "
				return jsonify({"sent":sent, "drs":drs, "boxpath":"error", "boxpdf":"error", "boxgraph":"error", "treepath": "error", "treegraph":"error", "msg":msg})
			with open(treepath,"rb") as imageFile:
				timg = base64.b64encode(imageFile.read())
			return jsonify({"sent":sent, "drs":drs, "boxpath":"error", "boxgraph":"error", "boxpdf":"error", "treepath": treepath, "treegraph":timg, "msg":msg})
		else:
			with open(boxpath, "rb") as imageFile:
				bimg = base64.b64encode(imageFile.read())
			if not os.path.isfile(treepath):
				return jsonify({"sent":sent, "drs":drs, "boxpath":boxpath, "boxpdf":boxpdf, "boxgraph":bimg, "treepath": "error", "treegraph":"error", "msg":msg})
			else: #everything works fine
				msg += "Successfully done! "
				with open(treepath, "rb") as imageFile:
					timg = base64.b64encode(imageFile.read())
				return jsonify({"sent":sent, "drs":drs, "boxpath":boxpath, "boxpdf":boxpdf, "boxgraph":bimg, "treepath": treepath, "treegraph":timg, "msg":msg})
	else:
		return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True, host='bollin.inf.ed.ac.uk', port='6123')
