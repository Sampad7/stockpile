from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Global list — all products live here
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

@app.route('/')
def table():
    headings = ["#", "NAME", "CATEGORY", "QUANTITY", "STATUS", "ACTIONS"]

    # ✅ Build rows FROM products list (not hardcoded)
    data = []
    for i, p in enumerate(products):
        data.append((
            i + 1,
            p["name"],
            p["category"],
            p["qty"],
            get_status(p["qty"]),
            i    # index for edit/delete buttons
        ))
        headings = ["#", "NAME", "CATEGORY", "QUANTITY", "STATUS", "ACTIONS"]
    
    q = request.args.get('q', '').strip().lower()  # get search query from URL
    
    data = []
    for i, p in enumerate(products):
        # check if query matches name or category
        if q in p["name"].lower() or q in p["category"].lower():
            data.append((i + 1, p["name"], p["category"], p["qty"], get_status(p["qty"]), i))
    



    return render_template('invowner.html', headings=headings, data=data)


@app.route('/add', methods=['POST'])
def add_product():
    info     = request.get_json()
    name     = info.get('name', '').strip()
    category = info.get('category', '').strip()
    qty      = int(info.get('qty', 0))
    price    = float(info.get('price', 0))

    if name:
        products.append({          # ✅ appends to the same list table() reads
            "name":     name.upper(),
            "category": category.upper(),
            "qty":      qty,
            "price":    price,
        })
        return jsonify({"success": True})

    return jsonify({"success": False})
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

    # Example: Replace these queries with your actual database queries
    # e.g., in_stock = db.execute("SELECT COUNT(*) FROM products WHERE status='Available'").fetchone()[0]
    
    # Mocking your real-time data calculations:
    in_stock_query_result = 12  # Put your calculation logic here
    out_stock_query_result = 3  # Put your calculation logic here

# 1. YOUR MAIN DASHBOARD ROUTE (Loads the webpage and your table data)
@app.route('/dashboard') # or whatever your dashboard route path is named
def dashboard():
    # 1. Fetch your full inventory data from your database here
    # e.g., cursor.execute("SELECT * FROM products")
    inventory_data = [
        [1, "ATTA", "Groceries", 50, "Available", 101],
        [2, "SUNFLOWER OIL", "Groceries", 20, "Available", 102]
    ] # Replace this sample array with your actual database query fetchall()
    
    headings = ("NAME", "CATEGORY", "QUANTITY", "STATUS", "ACTIONS")

    # Pass BOTH headings and data variables into your HTML file
    return render_template('invowner.html', headings=headings, data=inventory_data)


# 2. YOUR REAL-TIME API ROUTE (Only used by JavaScript background fetch)

    # 1. YOUR MAIN DASHBOARD ROUTE (Loads the webpage and your table data)



# 2. YOUR REAL-TIME API ROUTE (Only used by JavaScript background fetch)
@app.route('/api/stock-counts')
def get_stock_counts():
    # Run separate quick count queries here
    in_stock_count = 12  # Replace with actual DB count logic
    out_stock_count = 0  # Replace with actual DB count logic

    # Return strictly JSON data (JavaScript reads this)
    return jsonify({
        'stat-in': in_stock_count,
        'stat-out': out_stock_count
    })

if __name__ == '__main__':
    app.run(debug=True)