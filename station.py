from flask import Flask,Blueprint,render_template,session,request,redirect,url_for
from database import *
import uuid
station=Blueprint('station',__name__)

@station.route('/station_home')
def station_home():
	return render_template("station_home.html")

@station.route('/station_view_complaints',methods=['get','post'])
def station_view_complaints():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=='approve':
		q="update complaint set status='approve' where complaint_id='%s'"%(cid)
		update(q)
		
	if action=='reject':
		q="update complaint set status='reject' where complaint_id='%s'"%(cid)
		update(q)
		



	q="SELECT * FROM complaint INNER JOIN `user` USING (user_id) inner join station using (station_id)"
	res=select(q)
	data['complaint']=res
	return render_template("station_view_complaints.html",data=data)

@station.route('/station_view_evidence',methods=['get','post'])
def station_view_evidence():
	data={}
	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	

	q="select * from evidence inner join complaint using(complaint_id)"
	res=select(q)

	data['evidence']=res
	return render_template("station_view_evidence.html",data=data)

@station.route('/station_view_uploaded_file',methods=['get','post'])
def station_view_uploaded_file():
	data={}

	if 'action' in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

		

	q="select * from upload_file inner join complaint using(complaint_id) "
	res=select(q)
	data['upload_file']=res
	return render_template("station_view_uploaded_file.html",data=data)

@station.route('/station_manage_crime',methods=['get','post'])
def station_manage_crime():
	data={}
	q1="select * from crime"
	res=select(q1)
	data['crime']=res
	sid=session['Station_id']
	print(sid)


	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='update':
		q="select * from crime where Crime_id='%s'"%(cid)
		res=select(q)
		data['row']=res

	if 'up' in request.form:
		crime=request.form['crime']
		details=request.form['details']
		

		q="update crime set Crime='%s', Details='%s'where Crime_id='%s'"%(crime,details,cid)
		update(q)
		return redirect(url_for('station.station_manage_crime'))


	if action=='delete': 
		q="delete from crime where Crime_id='%s'"%(cid)
		delete(q)
		return redirect(url_for('station.station_manage_crime'))
			

	if 'view' in request.form:
		crime=request.form['crime']
		details=request.form['details']
	
		q="insert into crime values(null,'%s','%s','%s',curdate())"%(sid,crime,details)
		insert(q)

		print(q)

		return redirect(url_for('station.station_manage_crime'))



	return render_template("station_manage_crime.html",data=data)


@station.route('/station_manage_criminals',methods=['get','post'])
def station_manage_criminals():
	data={}
	q1="select * from criminals"
	res=select(q1)
	data['criminals']=res
	print(q1)

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='delete': 
		q="delete from criminals where Criminals_id='%s'"%(cid)
		delete(q)
		print(q)
		return redirect(url_for('station.station_manage_criminals'))

	if action=='update':
		q="select * from criminals where Criminals_id='%s'"%(cid)
		res=select(q)
		data['row']=res

	if 'up' in request.form:
		name=request.form['Name']
		details=request.form['Details']
		aadhar=request.form['Aadhar']
		passport=request.form['Passport']
		

		q="update criminals set Name='%s', Details='%s',Aadhar='%s',Passport='%s'where Criminals_id='%s'"%(name,details,aadhar,passport,cid)
		update(q)
		print(q)
		return redirect(url_for('station.station_manage_criminals'))


	
	if 'view' in request.form:
		cid=request.args['cid']
		name=request.form['Name']
		details=request.form['Details']
		aadhar=request.form['Aadhar']
		passport=request.form['Passport']
	
		q="insert into criminals values(null,'%s','%s','%s','%s','%s')"%(cid,name,details,aadhar,passport)
		insert(q)

		print(q)

		return redirect(url_for('station.station_manage_criminals'))



	return render_template("station_mange_criminals.html",data=data)

@station.route('/station_view_laws_and_order',methods=['get','post'])
def station_view_laws_and_order():
	data={}
	q="select * from lawandorder"
	res=select(q)
	data['lawandorder']=res
	return render_template("station_view_laws_and_order.html",data=data)

@station.route('/station_manage_judgement',methods=['get','post'])
def station_manage_judgement():
	data={}
	q="select * from judgement"
	res=select(q)
	data['judgement']=res
	print(q)

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=='delete':
		q="delete from judgement where Judgement_id='%s'"%(cid)
		delete(q)
		print(q)
		return redirect(url_for('station.station_manage_judgement'))

	if action=='update':
		q="select * from judgement where judgement_id='%s'"%(cid)
		res=select(q)
		data['row']=res

	if 'up' in request.form:
		judgement=request.form['Judgement']
		q="update judgement set Judgement='%s' where Judgement_id='%s'"%(judgement,cid)
		update(q)
		print(q)
		return redirect(url_for('station.station_manage_judgement'))

	if 'view' in request.form:
		cid=request.args['cid']
		judgement=request.form['Judgement']
		q="insert into judgement values(null,'%s','%s',curdate())"%(cid,judgement)
		insert(q)
		return redirect(url_for('station.station_manage_judgement',cid=cid))

	return render_template("station_manage_judgement.html",data=data)


@station.route('/station_manage_fir',methods=['get','post'])
def station_manage_fir():
	data={}
	q1="select * from fir"
	res=select(q1)
	data['fir']=res
	print(q1)

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='delete': 
		q="delete from fir where Fir_id='%s'"%(cid)
		delete(q)
		print(q)
		return redirect(url_for('station.station_manage_fir'))

	if action=='update':
		q="select * from fir where Fir_id='%s'"%(cid)
		res=select(q)
		data['row']=res

	if 'up' in request.form:
		fir_details=request.form['Firdetails']
		uploaded_file=request.files['Uploadedfile']
		

		q="update fir set Firdetails='%s', Uploadedfile='%s'where Fir_id='%s'"%(fir_details,uploaded_file,cid)
		update(q)
		print(q)
		return redirect(url_for('station.station_manage_fir'))


	
	if 'view' in request.form:
		cid=request.args['cid']
		name=request.form['Firdetails']
		details=request.files['Uploadedfile']
		path='static/'+str(uuid.uuid4())+details.filename
		details.save(path)
	
		q="insert into fir values(null,'%s','%s','%s')"%(cid,name,path)
		insert(q)

		print(q)

		return redirect(url_for('station.station_manage_fir'))



	return render_template("station_manage_fir.html",data=data)

@station.route('/station_issue_charge_sheet',methods=['get','post'])
def station_issue_charge_sheet():
	data={}
	q1="select * from chargesheet"
	res=select(q1)
	data['chargesheet']=res
	print(q1)
	
	if 'view' in request.form:
		cid=request.args['cid']
		name=request.files['Chargesheet']
		path='static/'+str(uuid.uuid4())+name.filename
		name.save(path)
	
		q="insert into chargesheet values(null,'%s','%s')"%(cid,path)
		insert(q)

		print(q)

		return redirect(url_for('station.station_issue_charge_sheet'))
	return render_template("station_issue_charge_sheet.html",data=data)


@station.route('/station_send_msg_to_user',methods=['get','post'])
def station_send_msg_to_user():
	data={}
	cid=request.args['cid']
	ld=session['Login_id']
	stid=request.args['stid']
	data['ld']=ld
	
	if 'send' in request.form:
		Message=request.form['msg']
		q1="insert into message values(null,'%s','%s','%s','%s',curdate())"%(cid,ld,stid,Message)
		insert(q1)
		return redirect(url_for('station.station_send_msg_to_user',cid=cid,stid=stid))

	q="SELECT * FROM message WHERE (Sender_id='%s' AND Receiver_id='%s') OR (Sender_id='%s' AND Receiver_id='%s')"%(ld,stid,stid,ld)
	res=select(q)
	data['message']=res
	return render_template("/station_send_msg_to_user.html",data=data)
