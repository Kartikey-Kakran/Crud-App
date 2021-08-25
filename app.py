from flask import Flask, render_template,request,redirect
from modules import db,StudentModel

app = Flask(__name__)

# configuring database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# forming table 
@app.before_first_request
def create_table():
    db.create_all()

# forming route 

@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
    
    if request.method == 'POST':
        roll_no = request.form['roll']
        name = request.form['name']
        class1 = request.form['class']
        status = request.form['status']
        student = StudentModel(Roll_No=roll_no, Name=name, Class=class1, Status=status)
        db.session.add(student)
        db.session.commit()
        return redirect('/data')


# To see data on live tab  
@app.route('/')       
@app.route('/data')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalistt.html', stud = students)



@app.route('/data/<int:id>')
def RetrieveStudent(id):
    student = StudentModel.query.filter_by(Roll_No=id).first()
    if student:
        return render_template('data.html', student = student) 
    return f"Student with id ={id} Dosen't exist"
   
@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(Roll_No=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            roll_no = request.form['roll']
            name = request.form['name']
            class1 = request.form['class']
            status = request.form['status']
            student = StudentModel(Roll_No=roll_no, Name=name, Class=class1, Status=status)
            db.session.add(student)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Student with id = {id} Doesn't exist"
    return render_template('update.html', student = student) 

@app.route('/delete/<int:id>')
def delete(id):
    student = StudentModel.query.filter_by(Roll_No=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/data")

app.run(debug=True)





    
