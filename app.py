from flask import Flask, render_template, redirect, url_for
import os
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/runtodoapp', methods=['POST'])
def run_todo_app():
    print("Button clicked - Endpoint hit")  # Debugging print
    threading.Thread(target=run_todo_list_app).start()
    return redirect(url_for('index'))

def run_todo_list_app():
    print("Running Task1.py")  # Debugging print
    os.system('python Task1.py')

if __name__ == '__main__':
    app.run(debug=True)
