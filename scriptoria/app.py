from flask import Flask, render_template, request, redirect, url_for, jsonify
from scriptoria.generator import generate
from scriptoria.storage import append_entry, read_history

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def do_generate():
    # Backwards-compatible form POST route (keeps original behavior)
    idea = request.form.get('idea', '').strip()
    mode = request.form.get('mode', 'screenplay')
    if not idea:
        return redirect(url_for('index'))
    output = generate(idea, mode)
    append_entry({'idea': idea, 'mode': mode, 'output': output})
    return render_template('result.html', idea=idea, mode=mode, output=output)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json() or {}
    idea = (data.get('idea') or '').strip()
    mode = data.get('mode', 'screenplay')
    temperature = data.get('temperature', 0.8)
    max_tokens = data.get('max_tokens', 800)
    project = data.get('project') or 'default'
    if not idea:
        return jsonify({'error': 'idea is required'}), 400
    output = generate(idea, mode, temperature=temperature, max_tokens=max_tokens)
    entry = {'project': project, 'idea': idea, 'mode': mode, 'output': output, 'temperature': temperature, 'max_tokens': max_tokens}
    append_entry(entry)
    return jsonify({'output': output, 'entry': entry})


@app.route('/api/history', methods=['GET'])
def api_history():
    return jsonify(read_history())


@app.route('/api/history/clear', methods=['POST'])
def api_history_clear():
    from scriptoria.storage import clear_history
    clear_history()
    return jsonify({'ok': True})


@app.route('/api/history/<int:index>', methods=['DELETE'])
def api_history_delete(index):
    from scriptoria.storage import delete_entry
    delete_entry(index)
    return jsonify({'ok': True})


if __name__ == '__main__':
    app.run(debug=True)
