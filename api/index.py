from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

products = [
    {"name": "ATTA", "category": "GRAINS", "qty": 100, "price": 50},
]

def get_status(qty):
    if qty <= 0:
        return "Out of Stock"
    elif qty <= 5:
        return "Low Stock"
    else:
        return "Available"

# ── HOME / TABLE ──────────────────────────────────────
@app.route('/')
def table():
    headings = ["#", "NAME", "CATEGORY", "QUANTITY", "STATUS", "ACTIONS"]
    q = request.args.get('q', '').strip().lower()

    data = []
    for i, p in enumerate(products):
        if q in p["name"].lower() or q in p["category"].lower():
            data.append((i + 1, p["name"], p["category"],
                         p["qty"], get_status(p["qty"]), i))

    stats = {
        "total":     len(products),
        "in_stock":  sum(1 for p in products if p["qty"] > 5),
        "out_stock": sum(1 for p in products if p["qty"] <= 0),
        "low_stock": sum(1 for p in products if 0 < p["qty"] <= 5),
    }

    return render_template('invowner.html',
                           headings=headings, data=data, q=q, stats=stats)

# ── ADD ───────────────────────────────────────────────
@app.route('/add', methods=['POST'])
def add_product():
    info = request.get_json()
    name = info.get('name', '').strip()
    if name:
        products.append({
            "name":     info.get('name').upper(),
            "category": info.get('category', '').upper(),
            "qty":      int(info.get('qty', 0)),
            "price":    float(info.get('price', 0)),
        })
        return jsonify({"success": True})
    return jsonify({"success": False})

# ── GET ONE (pre-fill edit form) ──────────────────────
@app.route('/get/<int:idx>')
def get_product(idx):
    if 0 <= idx < len(products):
        return jsonify({"success": True, "product": products[idx]})
    return jsonify({"success": False})

# ── EDIT ──────────────────────────────────────────────
@app.route('/edit/<int:idx>', methods=['POST'])
def edit_product(idx):
    if 0 <= idx < len(products):
        info = request.get_json()
        products[idx]["name"]     = info.get('name', '').upper()
        products[idx]["category"] = info.get('category', '').upper()
        products[idx]["qty"]      = int(info.get('qty', 0))
        products[idx]["price"]    = float(info.get('price', 0))
        return jsonify({"success": True})
    return jsonify({"success": False})

# ── DELETE ────────────────────────────────────────────
@app.route('/delete/<int:idx>', methods=['POST'])
def delete_product(idx):
    if 0 <= idx < len(products):
        products.pop(idx)
        return jsonify({"success": True})
    return jsonify({"success": False})

# ── STATS API ─────────────────────────────────────────
@app.route('/api/stock-counts')
def get_stock_counts():
    return jsonify({
        'stat-total': len(products),
        'stat-in':    sum(1 for p in products if p["qty"] > 5),
        'stat-out':   sum(1 for p in products if p["qty"] <= 0),
        'stat-low':   sum(1 for p in products if 0 < p["qty"] <= 5),
    })

