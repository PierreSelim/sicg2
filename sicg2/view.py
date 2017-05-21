import markdown
from flask import Flask, render_template, Markup

from database import SicgDB


db = SicgDB.get()
app = Flask(__name__)


def articles(limit=1000):
    return db.list(limit=limit).decode('utf-8')


@app.route('/')
def index():
    content = Markup(markdown.markdown(articles()))
    return render_template('index.html', content=content)


if __name__ == '__main__':
    app.run(debug=True)
