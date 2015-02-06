from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""

    # our cart in our session - a list of melons
    if 'cart' not in session:
        session['cart'] = []
    melons_in_cart = session['cart']
    return render_template("cart.html", melons_in_cart = melons_in_cart)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    melon = model.get_melon_by_id(id)
    melon_name = melon.common_name
    melon_price = melon.price

    if 'cart' not in session:
        session['cart'] = []
    for a_melon_list in session['cart']:
        if a_melon_list[0] == melon_name:
            a_melon_list[1] = a_melon_list[1] + 1
            flash('You just incremented the quantity of %s in your cart.'% melon_name) 
            print "All the melons in our cart ", session['cart']
            return render_template("cart.html", melons_in_cart=session['cart'])

    session['cart'].append([melon_name, 1, melon_price]) 
    flash('You just added %s to your cart.'% melon_name) 
    return render_template("cart.html", melons_in_cart=session['cart'], melon_name=melon_name, melon_price=melon_price)

    
        

@app.route("/login", methods=['GET'])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    session['email'] = request.form['email']
    if 'email' in session:
        flash('You are logged in as %s' % session['email'])
    return redirect(url_for('index'))


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
