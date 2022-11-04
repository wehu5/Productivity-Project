from flask import Flask, render_template
import os
from pathlib import Path
parent_path = Path.cwd()
path_ = os.path.join(parent_path, "GazeTracking\\example.py")
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  file = open(path_, 'r').read()
  return exec(file)

if __name__ == '__main__':
  app.run(debug=True)