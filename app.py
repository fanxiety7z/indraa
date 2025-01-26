from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Nama file CSV
CSV_FILE = "pesanan.csv"

# Buat file CSV dengan header jika belum ada
def initialize_csv():
    try:
        with open(CSV_FILE, mode="x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama Produk", "Harga", "Nama Pelanggan", "Email", "Alamat", "Metode Pembayaran"])
    except FileExistsError:
        pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chocolate")
def chocolate():
    return render_template("chocolate.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Route untuk menyimpan data checkout ke CSV
@app.route("/submit_checkout", methods=["POST"])
def submit_checkout():
    try:
        # Ambil data dari form
        cart = request.json.get("cart", [])
        customer_info = request.json.get("customer_info", {})

        # Simpan data ke file CSV
        with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for item in cart:
                writer.writerow([
                    item["name"], 
                    item["price"], 
                    customer_info.get("name"), 
                    customer_info.get("email"), 
                    customer_info.get("address"), 
                    customer_info.get("payment_method")
                ])

        return jsonify({"message": "Pesanan berhasil disimpan ke CSV!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    initialize_csv()
    app.run(debug=True)
