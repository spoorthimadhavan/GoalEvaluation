from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#  Database connection configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/goal_evaluation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# DB models
class Goal(db.Model):
    __tablename__ = 'goals'
    goal_id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(255))
    statement = db.Column(db.Text)
    status = db.Column(db.Integer)
    determination_method = db.Column(db.Text)
    last_change_comment = db.Column(db.Text)
    last_date = db.Column(db.Date)
    other_info = db.Column(db.Text)
    current_status = db.Column(db.Integer)


class EvaluationHistory(db.Model):
    __tablename__ = 'Evaluations_History'
    history_id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))
    previous_status = db.Column(db.Integer)
    change_description = db.Column(db.Text)
    changed_by = db.Column(db.String(255))
    change_date = db.Column(db.Date)


@app.route('/')
def index():
    return render_template('index.html')


# Route for goal listing
@app.route('/goals')
def list_goals():
    goals = Goal.query.all()
    return render_template('goals.html', goals=goals)


@app.route('/goal/<int:goal_id>')
def view_goal(goal_id):
    # Fetch the specific goal  using its ID
    goal = Goal.query.get_or_404(goal_id)
    return render_template('goal_details.html', goal=goal)


@app.route('/edit_goal/<int:goal_id>', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    if request.method == 'POST':
        goal.department = request.form['department']
        goal.statement = request.form['statement']
        goal.status = request.form['status']
        goal.determination_method = request.form['determination_method']
        goal.last_change_comment = request.form['last_change_comment']
        goal.last_date = request.form['last_date']
        goal.other_info = request.form['other_info']

        db.session.commit()
        log_history(goal_id, int(request.form['status']), "Goal updated", "Admin")

        return redirect(url_for('view_goal', goal_id=goal.goal_id))

    return render_template('edit_goal.html', goal=goal)


# Route create_goal
@app.route('/create_goal', methods=['GET', 'POST'])
def create_goal():
    if request.method == 'POST':
        department = request.form['department']
        statement = request.form['statement']
        status = int(request.form['status'])
        determination_method = request.form['determination_method']
        last_change_comment = request.form['last_change_comment']
        last_date = request.form['last_date']
        other_info = request.form['other_info']

        # Check if status is between 1 and 10
        if status < 1 or status > 10:
            return "Status must be between 1 and 10"

        new_goal = Goal(department=department, statement=statement, status=status,
                        determination_method=determination_method, last_change_comment=last_change_comment,
                        last_date=last_date, other_info=other_info, current_status=status)

        db.session.add(new_goal)
        db.session.commit()
        log_history(new_goal.goal_id, status, "Goal created", "Admin")

        return redirect(url_for('list_goals'))
    return render_template('create_goal.html')


def log_history(goal_id, status, change_description, changed_by):
    history_entry = EvaluationHistory(goal_id=goal_id, previous_status=status,
                                      change_description=change_description,
                                      changed_by=changed_by, change_date=datetime.now())
    db.session.add(history_entry)
    db.session.commit()


# Routes for  evaluations
@app.route('/evaluations')
def view_evaluations():
    evaluations = EvaluationHistory.query.all()
    return render_template('evaluations.html', evaluations=evaluations)


@app.route('/evaluations/<int:goal_id>')
def evaluations(goal_id):
    history = EvaluationHistory.query.filter_by(goal_id=goal_id).order_by(EvaluationHistory.change_date.desc()).all()

    return render_template('evaluations.html', evaluations=history)


@app.route('/graphical_view')
def graphical_view():
    # Fetch goals with their corresponding evaluation history
    goals_with_evaluations = db.session.query(Goal, EvaluationHistory).\
        filter(Goal.goal_id == EvaluationHistory.goal_id).all()

    goal_ids = []
    statuses = []
    previous_statuses = []

    for goal, evaluation in goals_with_evaluations:
        goal_ids.append(goal.goal_id)
        statuses.append(goal.status)
        previous_statuses.append(evaluation.previous_status)

    return render_template('graphical_view.html', goal_ids=goal_ids, statuses=statuses,
                           previous_statuses=previous_statuses)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
