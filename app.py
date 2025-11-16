from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Crear carpeta si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

uploads = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        category = request.form.get('category')
        reps = request.form.get('reps')
        progress = request.form.get('progress')

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploads.append({
                'filename': filename,
                'category': category,
                'reps': reps,
                'progress': progress
            })
        return redirect(url_for('index'))

    # Agrupar por categoría
    uploads_by_category = {}
    for item in uploads:
        uploads_by_category.setdefault(item['category'], []).append(item)

    return render_template('index.html', uploads_by_category=uploads_by_category)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    global uploads
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    uploads = [item for item in uploads if item['filename'] != filename]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
