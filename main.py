import sys
from PIL import Image
from flask import Flask, render_template, make_response
from flask import request
import time
import teseract
import commands
import string
import json

w = 572
h = 263
#img = Image.open(sys.argv[1])
#w1 = img.size[0]
#r = w1/float(w)

amount_coords = (430.92, 90.72, 559.062, 119.07)

date_coords = (417.311, 14.175, 559.062, 35.555)

day_coords = (422.3, 14.2, 458 , 36.9)
month_coords = (455, 14.2, 488.1, 36.9)
year_coords = (485.1, 14.2, 551.1, 36.9)

amt_words_coords = (69, 73, 509, 95)
date_coords = (417.311, 14.175, 559.062, 35.555)


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
	print request.files
        f = request.files['cheque']
        name = str(int(time.time()*1000)) + '.jpg'
	fpath = '/tmp/%s' % name
        f.save(fpath)
	img = Image.open(fpath)
	w1 = img.size[0]
	r = w1/float(w)
	amount_cropped, apath  = crop_amount(img, r)
	amount_words , wpath  = crop_amt_words(img, r)
	acc_no, accpath  = crop_acc_no(img, r)
	date , dpath  = crop_date(img, r)
	teseract.main(apath)
        name1 = str(int(time.time()*1000)) 

	s,o = commands.getstatusoutput("tesseract output.jpg %s" % (name1,))
	amt = None
	amt_words = None
	acc_no = None
	date = None
	if s:
	    print o
	else:
	    with open(name1 + '.txt', 'r') as f:
		for line in f:
			print line
			line1 = line.translate(None, string.ascii_letters + ' ' + string.punctuation).strip()
			print line1
			try:
				amt = int(line1)
			except:
				continue
			else:
				break
	teseract.main(wpath)
        name2 = str(int(time.time()*1000)) 
	s1, o1 = commands.getstatusoutput("tesseract output.jpg %s" % (name2,))
	if s1:
	    print o1
	else:
	    with open(name2 + '.txt', 'r') as f:
		amt_words = f.readlines()[0].strip()
	
	teseract.main(accpath)
        name3= str(int(time.time()*1000)) 
	s2, o2 = commands.getstatusoutput("tesseract output.jpg %s" % (name3,))
	if s1:
	    print o1
	else:
	    with open(name3+ '.txt', 'r') as f:
	        for line in f:
		    line1 = line.translate(None, string.ascii_letters + string.punctuation).strip()
		    try:
		        acc_no = int(line1)
		    except:
		        continue
		    else:
		        break
	teseract.main(dpath)
        name4 = str(int(time.time()*1000)) 
	s3, o3 = commands.getstatusoutput("tesseract output.jpg %s" % (name4,))
	if s3:
	    print o3
	else:
		with open(name4 + '.txt' ,'r') as f:
			date = f.readlines()[0].strip()
	data = {"amount": amt, "account_number": acc_no, "amount_words": amt_words}
	
    else:
        return render_template("index.html")
    return make_response(json.dumps(data))

def crop_amount(img, r):
    i2 = img.crop((430.92*r, 90.72*r, 559.062*r, 119.07*r))
    name = str(int(time.time()*1000)) + '.jpg'
    fpath = '/tmp/%s' % name
    i2.save(fpath)
    return i2,fpath

def crop_date(img, r):
    i3 = img.crop((417.311*r, 14.175*r, 559.062*r, 35.555*r))
    i3.save("/tmp/crop_date.jpg")
    return i3, "/tmp/crop_date.jpg"


def crop_acc_no(img, r):
    i3 = img.crop((62.37*r, 121.905*r, 181.1565*r, 147.13649999999998*r))
    i3.save("/tmp/crop_acc.jpg")
    return i3, "/tmp/crop_acc.jpg"

def crop_amt_words(img, r):
    t = tuple([x*r for x in amt_words_coords])
    i3 = img.crop(t)
    i3.save("/tmp/crop_amt_words.jpg")
    return i3, "/tmp/crop_amt_words.jpg"
    
