from flask import Flask, render_template
from WebPy.paper import paper

app = Flask(__name__)

app.register_blueprint(paper)

@app.route('/')
def index():
    # 默认打开paper界面
    return render_template('index.html')
   
if __name__ == '__main__':
    app.run(debug=True)