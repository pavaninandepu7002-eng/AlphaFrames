from flask import Flask, render_template, request, redirect, url_for
from scriptoria.generator import generate

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def do_generate():
    idea = request.form.get('idea', '').strip()
    mode = request.form.get('mode', 'screenplay')
    if not idea:
        return redirect(url_for('index'))
    output = generate(idea, mode)
    return render_template('result.html', idea=idea, mode=mode, output=output)


if __name__ == '__main__':
    app.run(debug=True)
