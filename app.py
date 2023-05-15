from flask import Flask,render_template, request, redirect, url_for
from forms import ProductForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tralalala'

class Product:
    def __init__(self, name, quantity, unit, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.unit_price = unit_price

    def __str__(self):
        return f'{self.name},{self.quantity},{self.unit},{self.unit_price}'

product1 = Product(name='Milk', quantity=120, unit='l', unit_price=2.3)
product2 = Product(name='Sugar', quantity=1000, unit='kg', unit_price=3)
product3 = Product(name='Flour', quantity=12000, unit='kg', unit_price=1.2)
product4 = Product(name='Coffee', quantity=25, unit='kg', unit_price=40)


items = [product1, product2, product3, product4]


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/products', methods=['GET', 'POST'])
def product_list():
    form = ProductForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            name = form.name.data
            quantity = form.quantity.data
            unit = form.unit.data
            unit_price = form.unit_price.data
            item = Product(name=name, quantity=quantity, unit=unit, unit_price=unit_price)

            items.append(item)
        return redirect(url_for('product_list'))
    
    return render_template('product_list.html', form=form, items=items)

if __name__ == '__main__':
    app.run(debug=True)