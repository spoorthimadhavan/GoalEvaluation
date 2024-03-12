# GoalEvaluation

## Description
The Goal Evaluation System is a web application built with Flask, a Python web framework, and MariaDB, a relational database management system. This system allows users to create, view, edit, and evaluate goals, as well as visualize goal evaluation data in graphical form.

## Features
- Goal management: Users can create new goals, view details of existing goals, and edit goal information.
- Evaluation history: Tracks the history of goal evaluations, including previous status, change description, changed by, and change date.
- Graphical visualization: Provides visual representation of goal evaluation data using  bar charts.
- Responsive design: Ensures the application is accessible and usable across various devices and screen sizes.

## Technologies Used
- Flask: A lightweight Python web framework for building web applications.
- MariaDB: A relational database management system compatible with MySQL, used for storing and managing data.
- SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library for interacting with databases.
- Chart.js: A JavaScript library for creating interactive and customizable charts.
- HTML/CSS: Used for structuring and styling the user interface of the web application.
- JavaScript: Used for client-side scripting to enhance interactivity and functionality.

## Installation
1. Clone the repository to your local machine:

`git clone https://github.com/spoorthimadhavan/GoalEvaluation.git`

2. Navigate to the project directory:
`cd GoalEvaluation`

3. Install the required dependencies:
`pip install -r requirements.txt`

4. Set up the MariaDB database:
- Create a new MariaDB database named `goal_evaluation`.
- Update the database connection URL in `app.py` to match your MariaDB configuration.

5. Run the application

6. Access the application in your web browser at `http://localhost:5000`.

## Usage
1. Create new goals by providing relevant information such as department, statement, status, etc.
2. View the details of existing goals and evaluate their performance over time.
3. Edit goal information.
4. Visualize goal evaluation data using the graphical view feature to gain insights into performance trends.


## Developed by
- Developed by [Spoorthi Madhavan](https://github.com/spoorthimadhavan).


