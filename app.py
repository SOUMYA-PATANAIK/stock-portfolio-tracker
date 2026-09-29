from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Manually defined stock prices
stock_prices = {
    "TCS": 3500,
    "INFY": 1800,
    "RELIANCE": 2900,
    "HDFC": 1700,
    "WIPRO": 550,
    "ICICI": 1250
}

portfolio = []


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    if request.method == "POST":
        stock = request.form.get("stock")
        quantity = request.form.get("quantity")

        if stock not in stock_prices:
            message = "Please select a valid stock."

        else:
            try:
                quantity = int(quantity)

                if quantity <= 0:
                    message = "Quantity must be greater than 0."
                else:
                    price = stock_prices[stock]
                    investment = price * quantity

                    portfolio.append({
                        "stock": stock,
                        "price": price,
                        "quantity": quantity,
                        "investment": investment
                    })

                    message = f"✅ {stock} added successfully!"

            except ValueError:
                message = "⚠️ Please enter a valid quantity."

    total_investment = sum(
        item["investment"] for item in portfolio
    )

    total_quantity = sum(
        item["quantity"] for item in portfolio
    )

    total_stocks = len(portfolio)

    # Calculate portfolio percentage
    for item in portfolio:
        if total_investment > 0:
            item["percentage"] = round(
                (item["investment"] / total_investment) * 100, 2
            )
        else:
            item["percentage"] = 0

    return render_template(
        "index.html",
        stock_prices=stock_prices,
        portfolio=portfolio,
        total_investment=total_investment,
        total_quantity=total_quantity,
        total_stocks=total_stocks,
        message=message
    )


@app.route("/remove/<int:index>")
def remove_stock(index):
    if 0 <= index < len(portfolio):
        portfolio.pop(index)

    return redirect(url_for("index"))


@app.route("/clear")
def clear_portfolio():
    portfolio.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)