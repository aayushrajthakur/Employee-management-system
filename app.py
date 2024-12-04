from flask import Flask, render_template, request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Megatron113.#@localhost/employee_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    eno = db.Column(db.Integer, unique = True, nullable = False)
    ename = db.Column(db.String(100), nullable = False)
    edesign = db.Column(db.String(100), nullable = False)
    esalary = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return f'<Employee {self.eno}>'


@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees = employees)

@app.route('/employee/create', methods = ['GET','POST'])
def create_employee():
    if request.method == 'POST':
        new_employee = Employee(eno = request.form['eno'], ename = request.form['ename'], edesign = request.form['edesign'], esalary = request.form['esalary'])
        db.session.add(new_employee)
        db.session.commit()
        return redirect('/')
    return render_template('create.html')

@app.route('/employee/update/<int:id>', methods = ['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get(id)
    if request.method == 'POST':
        # Update employee logic here
        # For example:
        employee.eno = request.form['eno']
        employee.ename = request.form['ename']
        employee.edesign = request.form['edesign']
        employee.esalary = request.form['esalary']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', employee=employee)

@app.route('/employee/delete/<int:id>', methods = ['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect('/')

if __name__== '__main__':
    with app.app_context():
        try:
            db.create_all()  # Create tables
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True)
