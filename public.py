from flask import Flask,Blueprint,render_template,request,redirect,url_for,session
from database import *

public=Blueprint('public',__name__)


@public.route('/')
def home():
	return render_template('home.html')


@public.route('/login',methods=['get','post'])
def login():
	if 'login' in request.form:
		u_name=request.form['user']
		p_wd=request.form['password']
		print(u_name,p_wd)
		q="select * from login where Username='%s' and Password='%s'"%(u_name,p_wd)
		res=select(q)
		if res:
			session['Login_id']=res[0]['Login_id']
			lid=session['Login_id']
			if res[0]['Usertype']=="admin":
				return redirect(url_for('admin.adminhome'))
			elif res[0]['Usertype']=="user":
				return redirect(url_for('user.userhome'))
			elif res[0]['Usertype']=="station":
				q="select * from station where Login_id='%s'"%(lid)
				res1=select(q)
				if res1:
					session['Station_id']=res1[0]['Station_id']
					sid=session['Station_id']
					return redirect(url_for('station.station_home'))
	return render_template('login.html')

@public.route('/user_registration',methods=['get','post'])
def user_registration():
	if 'user' in request.form:
		fname=request.form['f_name']
		lname=request.form['l_name']
		Place=request.form['place']
		Phone=request.form['phone']
		mail=request.form['email']
		gender=request.form['g']
		u_name=request.form['user']
		p_wd=request.form['password']
		q="insert into login values(null,'%s','%s','user')"%(u_name,p_wd)
		id=insert(q)

		q1="insert into user values(null,'%s','%s','%s','%s','%s','%s','%s')"%(id,fname,lname,Place,Phone,mail,gender)
		insert(q1)
		print(q1)
		return redirect(url_for('user.userhome'))

	return render_template('user_registration.html')