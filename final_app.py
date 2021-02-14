from flask import Flask, render_template, request, redirect, session, jsonify
from firebase.firebase import FirebaseApplication
import courses_db
import os
import posenet
import main
import numpy as np
import segment

app=Flask(__name__)
app.secret_key='abc123'
s = 0
score=list()
fb = FirebaseApplication("https://edtutor-62c2b.firebaseio.com/")
cart1 = list()

@app.route('/')
def defaul():
	try:
		_=session['uname']
		return redirect('/landing')
	except:
		return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
	try:
		_=session['uname']
		return redirect('/landing')
	except:
		pass
	if request.method == 'POST':
		det = (request.form['uname'],request.form['pwd'])
		a = fb.get('/users/', det[0])
		if a==None:
			return render_template('login.html')
		else:
			if a['pwd']==det[1]:
				session['uname']=det[0]
				# session['cart']=list()
				return redirect('/landing')
			else:
				return render_template('login.html')
	else:
		return render_template('login.html')
		
@app.route('/signup', methods=['POST', 'GET'])
def signup():
	try:
		_=session['uname']
		return redirect('/landing')
	except:
		pass
	if request.method == 'POST':
		a = fb.get('/users/', request.form["uname"])
		if a!=None:
			return render_template("signup.html")
		else:
			payl = dict(request.form)
			payl["bio"] = ""
			payl["progress"] = [0 for _ in range(13)]
			payl["num"] = 0
			payl["sudenttutor"] = "student"
			fb.put('/users/', '%s'%request.form["uname"], payl)
			session["uname"]=payl["uname"]
			# session['cart']=list()
			return redirect('/landing')
	else:
		return render_template('signup.html')

@app.route('/profile', methods=['POST', 'GET'])
def prof():
	try:
		a=session["uname"]
	except KeyError:
		return redirect("/")
	a = fb.get('/users/', session["uname"])
	if request.method=="POST":
		a["name"]=request.form["name"]
		a["dob"]=request.form["dob"]
		a["email"]=request.form["email"]
		a["phno"]=request.form["phno"]
		a["bio"]=request.form["bio"]
		fb.put('/users/', session["uname"], a)
		return redirect("/profile")
	a.pop('pwd')
	acc = fb.get('/users/%s'%(session['uname']), 'progress')
	print(a)
	return render_template("profile.html", userdet=a, acc= acc, avg=round(sum(acc)/13.0, 2))

@app.route('/landing', methods=['POST', 'GET'])
def index():
	try:
		_=session['uname']
	except KeyError:
		return redirect('/')
	cname, course = courses_db.read_data(fb)
	categories = set([(course[i]['category']).title() for i in cname])
	return render_template('course.html', cname=cname, course=course, categories=categories)
	
@app.route('/logout', methods=['POST','GET'])
def logout():
	session.clear()
	global cart1
	cart1=list()
	return redirect('/')

@app.route('/warmup/<cname>', methods=['POST', 'GET'])
def warmer(cname):
	try:
		_=session['uname']
		courses = fb.get("/", "courses")
		f = False
		for i in courses.keys():
			if courses[i]["url"]==cname:
				course=courses[i]
				f = True
				fb.put('/courses/%s'%(course['name']), 'views', course['views']+1)
		if not f:
			return redirect('/landing')
		return render_template('warmup.html', course=course)
	except:
		return redirect('/login')

@app.route("/practice/<cname>", methods=['POST', 'GET'])
def prac(cname):
	try:
		a=session['uname']
		if request.method=="POST":
			print("post")
			f = request.files['myfile']
			f.save("recorded_video.mp4")
			return redirect('/loading1/%s'%(cname))
		courses = fb.get("/", "courses")
		f = False
		for i in courses.keys():
			if courses[i]["url"]==cname:
				course=courses[i]
				f = True
		if not f:
			return redirect('/landing')
		return render_template('vid.html', course=course)
	except KeyError:
		return redirect('/login')

@app.route("/loading1/<cname>", methods=["POST", "GET"])
def loader1(cname):
	return render_template("loading.html")

@app.route("/loading2/<cname>", methods=["POST", "GET"])
def loader2(cname):
	segment.segmentation()
	global s
	global score
	s, score = main.compare_ref_recorded()
	usr=fb.get('/users/', session['uname'])
	num = usr["num"]
	progress=[((i*num+j)/(num+1)) for i, j in zip(usr["progress"], score)]
	fb.put('/users/%s'%(session['uname']), 'progress', progress)
	fb.put('/users/%s'%(session['uname']), 'num', num+1)
	return redirect('/stats/%s'%(cname))

@app.route("/stats/<cname>", methods=['POST', 'GET'])
def statist(cname):
	try:
		_=session['uname']
		global s, score
		courses = fb.get("/", "courses")
		f = False
		for i in courses.keys():
			if courses[i]["url"]==cname:
				course=courses[i]
				f = True
		if not f:
			return redirect('/landing')
		avg = sum(score)/13.0
		prog = sum(fb.get('/users/%s'%(session['uname']), 'progress'))/13.0
		return render_template('plot.html', s=s, score=score, course=course, perform_diff=prog-avg)
	except KeyError:
		return redirect('/login')

@app.route('/gen_pickle', methods=['POST', 'GET'])
def generate_ref_pickle():
	posenet.get_video()
	return redirect("/")

@app.route('/recorded_video/', methods=['POST','GET'])
def check_both_video():
    if request.method == "POST":
        f = request.files['recorded_video']
        f.save("recorded_video.mp4")
        segment.segmentation()

        s, score = main.compare_ref_recorded()
        return jsonify({"verbal": s, "score": score})

    if request.method == 'GET':
        return "{\"empty\":\"empty\"}"
    else:
        return "Error"

@app.route('/delete_all/')
def delete():
    if os.path.exists('recorded_video.mp4'):
        os.remove('recorded_video.mp4')

    if os.path.exists('seg_output.avi'):
        os.remove('seg_output.avi')

    if os.path.exists('temp.pickle'):
        os.remove('temp.pickle')

# @app.route("/cart", methods=["POST", "GET"])
# def cart2():
# 	try:
# 		_=session['uname']
# 	except:
# 		return redirect('/login')
# 	global cart1
# 	if request.args.get("name")!=None and request.args.get("name") not in cart1:
# 		cart1.append(request.args.get("name"))
# 	return render_template("shopping.html", cart=cart1, courses = fb.get("/", "courses"))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__=="__main__":
	app.run(debug=True)
