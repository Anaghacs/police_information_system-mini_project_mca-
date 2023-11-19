from flask import *
from database import *
user=Blueprint('user',__name__)
import uuid

@user.route('/userhome')
def userhome():
	return render_template('userhome.html')

@user.route('/user_view_crimes',methods=['get','post'])
def user_view_crimes():
	data={}
	q="SELECT * FROM crime INNER JOIN station USING(Station_id)"
	print(q)
	res=select(q)
	data['cr']=res
	return render_template("user_view_crimes.html",data=data)

@user.route('/user_view_criminals',methods=['get','post'])
def user_view_criminals():
	data={}
	q="SELECT * FROM criminals INNER JOIN crime USING(Crime_id)"
	print(q)
	res=select(q)
	data['criminals']=res
	return render_template("user_view_criminals.html",data=data)

@user.route('/user_view_judgement',methods=['get','post'])
def user_view_judgement():
	data={}
	q="SELECT * FROM judgement INNER JOIN crime USING(Crime_id)"
	print(q)
	res=select(q)
	data['jud']=res
	return render_template("user_view_judgement.html",data=data)

@user.route('/user_view_law_and_order',methods=['get','post'])
def user_view_law_and_order():
	data={}
	q="SELECT * FROM lawandorder"
	print(q)
	res=select(q)
	data['lawandorder']=res
	return render_template("user_view_law_and_order.html",data=data)

@user.route('/user_view_search_station',methods=['get','post'])
def user_view_search_station():
	data={}
	if 'station' in request.form:
		msg=request.form['station']+'%'
		print(msg)
		q="SELECT * FROM station where Station like '%s'"%(msg)
	else:
		q="SELECT * FROM station"

	res=select(q)
	data['station']=res
		
	return render_template("user_view_search_station.html",data=data)

@user.route('/user_send_complaint',methods=['get','post'])
def user_send_complaint():
	data={}
	lid=session['Login_id']
	q1="SELECT * from station "
	res=select(q1)
	data['station']=res

	if 'send' in request.form:
		msg=request.form['msg']
		station=request.form['station']
		print(msg)
		q="insert into complaint values(null,'%s','%s','%s',curdate(),'pending')"%(lid,station,msg)
		id=insert(q)
		return redirect(url_for('user.user_send_complaint'))
		

	q="select * from complaint inner join station using (Station_id) inner join login using (Login_id)"
	res=select(q)
	data['complaint']=res
	return render_template("user_send_complaint.html",data=data)

@user.route('/user_mange_evidence',methods=['get','post'])
def user_mange_evidence():
	data={}
	cid=request.args['cid']
	q1="select * from evidence"
	res=select(q1)
	data['evidence']=res

	if 'manage' in request.form:
		print("*************")
		details=request.form['detals']
		file=request.files['file1']
		path='static/'+str(uuid.uuid4())+file.filename
		file.save(path)

		q="insert into evidence values(null,'%s','%s','%s',curdate())"%(cid,details,path)
		insert(q)

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='update':
		q="select * from evidence where Evidence_id='%s'"%(cid)
		res=select(q)
		print(res)
		print(q)
		data['upp']=res

	if 'up' in request.form:
		details=request.form['detals']
		file=request.files['file1']
		path='static/'+str(uuid.uuid4())+file.filename
		file.save(path)
		

		q="update evidence set Evidence='%s',Details='%s' where Evidence_id='%s'"%(details,path,cid)
		update(q)
		return redirect(url_for('user.user_mange_evidence',cid=cid))


	if action=="delete": 
		q="delete from evidence where Evidence_id='%s'"%(cid)
		delete(q)
		return redirect(url_for('user.user_mange_evidence',cid=cid))

	q="select * from evidence inner join complaint using(Complaint_id)"
	res=select(q)
	data['evidence']=res
	return render_template("user_mange_evidence.html",data=data)

@user.route('/user_send_msg_to_police',methods=['get','post'])
def user_send_msg_to_police():
	data={}
	cid=request.args['cid']
	ld=session['Login_id']
	stid=request.args['stid']
	data['ld']=ld
	
	if 'send' in request.form:
		Message=request.form['msg']
		q1="insert into message values(null,'%s','%s','%s','%s',curdate())"%(cid,ld,stid,Message)
		insert(q1)
		return redirect(url_for('user.user_send_msg_to_police',cid=cid,stid=stid))

	q="SELECT * FROM message WHERE (Sender_id='%s' AND Receiver_id='%s') OR (Sender_id='%s' AND Receiver_id='%s')"%(ld,stid,stid,ld)
	res=select(q)
	data['message']=res
	return render_template("/user_send_msg_to_police.html",data=data)

@user.route('/user_mange_files',methods=['get','post'])
def user_mange_files():
	data={}
	cid=request.args['cid']
	q1="select * from upload_file"
	res=select(q1)
	data['upload_file']=res

	if 'manage' in request.form:
		print("*************")
		
		cid=request.args['cid']
		file=request.files['file1']
		path='static/'+str(uuid.uuid4())+file.filename
		file.save(path)

		q="insert into upload_file values(null,'%s','%s',curdate())"%(cid,path)
		insert(q)
		# return redirect(url_for('user.user_manage_files',cid=cid))

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']

	else:
		action=None

	if action=='delete': 
		q="delete from upload_file where Uploadfile_id='%s'"%(cid)
		delete(q)
		# return redirect(url_for('user.user_manage_files'))


	if action=='update':
		q="select * from upload_file where Uploadfile_id='%s'"%(cid)
		res=select(q)
		print(res)
		print(q)
		data['upp']=res

	if 'up' in request.form:
		
		file=request.files['file1']
		path='static/'+str(uuid.uuid4())+file.filename
		file.save(path)
		

		q="update upload_file set File='%s' where Uploadfile_id='%s'"%(path,cid)
		update(q)
		# return redirect(url_for('user.user_manage_files',cid=cid))

	if 'action'=='accept':
		q=""
	

	q="select * from upload_file inner join complaint using(Complaint_id)"
	res=select(q)
	data['uploadfile']=res
	print(res)
	print(q)
	return render_template("user_manage_files.html",data=data)