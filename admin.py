from flask import Flask,Blueprint,render_template,request,session,redirect,url_for
from database import *
admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
	return render_template("adminhome.html")

@admin.route('/admin_manage_station',methods=['get','post'])
def admin_manage_station():
	data={}
	if 'user' in request.form:
		station=request.form['station']
		place=request.form['place']
		phone=request.form['phone']
		mail=request.form['email']
		u_name=request.form['user']
		p_wd=request.form['password']
		q="insert into login values(null,'%s','%s','station')"%(u_name,p_wd)
		id=insert(q)
		q1="insert into station values(null,'%s','%s','%s','%s','%s')"%(id,station,place,phone,mail)
		insert(q1)
		print(q1)

	q="select * from station "
	res=select(q)
	data['station']=res

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='update':
		q="select * from station where Station_id='%s'"%(cid)
		res=select(q)
		data['row']=res

	if 'up' in request.form:
		station=request.form['Station']
		place=request.form['Place']
		phone=request.form['Phone']
		email=request.form['Email']
		

		q="update station set station='%s', place='%s',phone='%s', email='%s' where Station_id='%s'"%(station,place,phone,email,cid)
		update(q)
		return redirect(url_for('admin.admin_manage_station'))


	if action=='delete': 
		q="delete from Station where Station_id='%s'"%(cid)
		delete(q)
		return redirect(url_for('admin.admin_manage_station'))
	

	if 'view' in request.form:
		station=request.form['Station']
		place=request.form['Place']
		phone=request.form['Phone']
		email=request.form['Email']
	
		q="select * from station"

		print(q)

		return redirect(url_for('admin.admin_manage_law_and_order'))
	return render_template("admin_manage_station.html",data=data)

@admin.route('/admin_view_user',methods=['get','post'])
def admin_view_user():
	data={}
	q="select * from user"
	res=select(q)
	data['user']=res
	return render_template("admin_view_user.html",data=data)

@admin.route('/admin_view_evidence',methods=['get','post'])
def admin_view_evidence():
	data={}
	q="select * from evidence INNER JOIN complaint using (complaint_id)"
	res=select(q)
	data['evidence']=res
	return render_template("admin_view_evidence.html",data=data)
	
@admin.route('/admin_view_complaint',methods=['get','post'])
def admin_view_complaint():
	data={}
	q="SELECT * FROM complaint INNER JOIN `user` USING (user_id) inner join station using (station_id)"
	res=select(q)
	data['complaint']=res
	return render_template("admin_view_complaint.html",data=data)


@admin.route('/admin_view_uploaded_file',methods=['get','post'])
def admin_view_uploaded_file():
	cid=request.args['cid']
	data={}
	q="select * from upload_file inner join complaint using (Complaint_id)"
	res=select(q)
	data['uploaded']=res
	return render_template("admin_view_uploaded_file.html", data=data)

@admin.route('/admin_send_msg_to_user',methods=['get','post'])

def admin_send_msg_to_user():
	data={}
	cid=request.args['cid']
	ld=session['Login_id']
	uid=request.args['uid']
	data['ld']=ld
	
	if 'send' in request.form:
		Message=request.form['msg']
		q1="insert into message values(null,'%s','%s','%s','%s',curdate())"%(cid,ld,uid,Message)
		insert(q1)
		return redirect(url_for('admin.admin_send_msg_to_user',cid=cid,uid=uid))

	q="SELECT * FROM message WHERE (Sender_id='%s' AND Receiver_id='%s') OR (Sender_id='%s' AND Receiver_id='%s')"%(ld,uid,uid,ld)
	print(q)
	res=select(q)
	data['message']=res
	return render_template("/admin_send_msg_to_user.html",data=data,cid=cid,uid=uid)

@admin.route('/admin_view_crime',methods=['get','post'])
def admin_view_crime():
	data={}
	q="SELECT * FROM crime INNER JOIN station USING(Station_id)"
	print(q)
	res=select(q)
	data['cr']=res
	return render_template("admin_view_crime.html",data=data)

@admin.route('/admin_view_criminals',methods=['get','post'])
def admin_view_criminals():
	data={}
	q="select * from criminals inner join crime using (Crime_id)"
	res=select(q)
	data['criminals']=res

	return render_template("/admin_view_criminals.html",data=data)


@admin.route('/admin_manage_law_and_order',methods=['get','post'])
def admin_manage_law_and_order():
	data={}
	q="select * from lawandorder"
	res=select(q)
	data['lawandorder']=res

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='update':
		q="select * from lawandorder where Lawandorder_id='%s'"%(cid)
		res=select(q)
		data['row']=res

	if 'up' in request.form:
		lawandorder=request.form['Lawandorder']
		details=request.form['Details']
		

		q="update lawandorder set Lawandorders='%s', Details='%s'where Lawandorder_id='%s'"%(lawandorder,details,cid)
		update(q)
		return redirect(url_for('admin.admin_manage_law_and_order'))


	if action=='delete': 
		q="delete from lawandorder where Lawandorder_id='%s'"%(cid)
		delete(q)
		return redirect(url_for('admin.admin_manage_law_and_order'))
	

	if 'view' in request.form:
		lawandorder=request.form['Lawandorder']
		details=request.form['Details']
	
		q="insert into lawandorder values(null,'%s','%s',curdate())"%(lawandorder,details)
		insert(q)

		print(q)

		return redirect(url_for('admin.admin_manage_law_and_order'))

	return render_template("admin_manage_law_and_order.html",data=data)

@admin.route('/admin_view_fir',methods=['get','post'])
def admin_view_fir():
	cid=request.args['cid']
	data={}
	q="select * from fir inner join crime using (Crime_id)"
	res=select(q)
	data['fir']=res
	return render_template("/admin_view_fir.html",data=data)

@admin.route('/admin_view_judgment',methods=['get','post'])
def admin_view_judgement():
	cid=request.args['cid']
	data={}
	q="SELECT * FROM crime INNER JOIN judgement USING(Crime_id) where crime_id='%s'"%(cid)
	print(q)
	res=select(q)
	data['jud']=res
	return render_template('admin_view_judgment.html',data=data)
	
@admin.route('/admin_view_charge_sheet',methods=['get','post'])
def admin_view_charge_sheet():
	cid=request.args['cid']
	data={}
	q="select * from chargesheet inner join crime using(Crime_id)"
	print(q)
	res=select(q)
	data['charg']=res
	return render_template('admin_view_charge_sheet.html',data=data)

