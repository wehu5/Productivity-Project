from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  file = open(r'/Users/jwong1209qaz/Desktop/IEEE/Productivity-Project/GazeTracking/example.py', 'r').read()
  return exec(file)

if __name__ == '__main__':
  app.run(debug=True)