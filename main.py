import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# إعدادات مجلد الرفع
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# أسعار المواد الافتراضية
MATERIAL_PRICES = {
    'PLA': 0.15,
    'ABS': 0.18,
    'PETG': 0.20,
    'Resin': 0.35
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate-cost', methods=['POST'])
def calculate_cost():
    # تقدير مبدئي للوزن بالجرام أو حسب حجم الملف المرفوع
    file_size = 10240  # قيمة افتراضية لو مافيش ملف
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_size = os.path.getsize(filepath)

    weight_grams = round(max(10.0, (file_size / 1024)), 2)
    
    if 'weight' in request.form:
        try:
            weight_grams = float(request.form.get('weight'))
        except ValueError:
            pass

    material = request.form.get('material', 'PLA')
    resolution = request.form.get('resolution', 'Standard')

    price_per_gram = MATERIAL_PRICES.get(material, 0.15)
    base_cost = weight_grams * price_per_gram

    multiplier = 1.25 if resolution == 'High' else 1.0
    total_cost = base_cost * multiplier + 5.0

    return jsonify({
        "material": material,
        "weight_grams": weight_grams,
        "resolution": resolution,
        "estimated_cost": round(total_cost, 2),
        "currency": "LYD"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)