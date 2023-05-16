from flask import Flask,render_template, request, redirect, url_for, flash
from forms import ProductForm, ProductSaleForm
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tralalala'

class Product:
    def __init__(self, name, quantity, unit, unit_price):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.unit_price = unit_price

    def __repr__(self):
        return f'({self.name},{self.quantity},{self.unit},{self.unit_price})'


items = {

    'Milk': Product(name='Milk', quantity=120, unit='l', unit_price=2.3),
    'Sugar': Product(name='Sugar', quantity=1000, unit='kg', unit_price=3),
    'Flour': Product(name='Flour', quantity=12000, unit='kg', unit_price=1.2),
    'Coffee': Product(name='Coffee', quantity=25, unit='kg', unit_price=40)
}

sold_items = {}

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

            items.update({name: Product(name=name, quantity=quantity, unit=unit, unit_price=unit_price)})
        
        flash(f'Successfully add product!')
        return redirect(url_for('product_list'))
    
    return render_template('product_list.html', form=form, items=items)

@app.route('/products/<product_name>/sell', methods=['GET', 'POST'])
def sell_product(product_name):
    form = ProductSaleForm()
    product = items.get(product_name)
    if not product:
        return 'Product not found'
    
    if request.method == 'POST':
        if form.validate_on_submit():
            quantity_sold = form.quantity.data

            if quantity_sold > product.quantity:
                return 'Insufficient quantity available'
            

            product.quantity -= quantity_sold
            sold_items.update({product.name: (product_name, quantity_sold, product.unit, product.unit_price)})
            print(sold_items)
            flash(f'Successfully sold {quantity_sold} {product.unit} of {product.name}!')
            return redirect(url_for('product_list'))
        

    return render_template('sell_product.html', form=form, product=product)

@app.route('/sold_products')
def sold_product_list():
    return render_template('sold_product_list.html', sold_items=sold_items)

@app.route('/export_to_csv')
def export():
    with open ('warehouse.csv', 'w') as csvfile:
        fieldnames = ['name', 'quantity', 'unit', 'unit_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item, info in items.items():
            writer.writerow({'name': info.name,
                             'quantity': info.quantity,
                             'unit': info.unit,
                             'unit_price': info.unit_price})
            
    flash('Successfully exported data to warehouse.csv!')
    return redirect(url_for('product_list'))
        

if __name__ == '__main__':
    app.run(debug=True)