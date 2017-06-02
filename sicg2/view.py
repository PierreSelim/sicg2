import markdown
from flask import Flask, render_template, Markup

from database import SicgDB


db = SicgDB.get()
app = Flask(__name__)


def articles(limit=1000):
    last_update = db.lastupdate()
    articles_list = db.list(limit=limit)
    mdown = "Last update: {update}\n\n{articles}".format(
        update=last_update,
        articles=articles_list)
    return mdown.decode('utf-8')


@app.route('/')
def index():
    content = Markup(markdown.markdown(articles()))
    return render_template('index.html', content=content)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=6013
    )
