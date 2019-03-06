from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

id = 0
menuid = 0
@app.route('/')
@app.route('/restaurants/<restaurantname>/')
def restaurantMenu(restaurantname):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    #items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    restaurant = session.query(Restaurant).filter_by(name=restaurantname)
    for restaurant in restaurant:
        global id
        id = restaurant.id
    items = session.query(MenuItem).filter_by(restaurant_id=id)


    return render_template('menu.html', restaurant=restaurant, items=items)


# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<restaurantname>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurantname):
    
    restaurant = session.query(Restaurant).filter_by(name=restaurantname)
    for restaurant in restaurant:
        global id
        id = restaurant.id
   #items = session.query(MenuItem).filter_by(restaurant_id=id)

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurantname = restaurantname))

    else:
        return render_template('newmenuitem.html', restaurant_name = restaurantname)
       


# Task 2: Create route for editMenuItem function here


@app.route('/restaurants/<restaurantname>/<itemname>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurantname, itemname):
    restaurant = session.query(Restaurant).filter_by(name=restaurantname)
    for restaurant in restaurant:
        global id
        print id
        id = restaurant.id
    itemName = session.query(MenuItem).filter_by(name=itemname)
    for itemName in itemName:
        global menuid 
        menuid = itemName.id
    editedItem = session.query(MenuItem).filter_by(id=menuid).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurantname = restaurantname))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        # I can use the following line instead
        #return render_template('editmenuitem.html', restaurant_name = restaurantname, item=editedItem)
        return render_template('editmenuitem.html', restaurant_name = restaurantname, restaurant_id=id, menu_name=itemname, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<restaurantname>/<itemname>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurantname, itemname):
    restaurant = session.query(Restaurant).filter_by(name=restaurantname)
    for restaurant in restaurant:
        global id
        id = restaurant.id
    itemName = session.query(MenuItem).filter_by(name=itemname)
    for itemName in itemName:
        global menuid 
        menuid = itemName.id
    itemToDelete = session.query(MenuItem).filter_by(id=menuid).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurantname = restaurantname))
    else:
        return render_template('deleteconfirmation.html', restaurant_name = restaurantname, item=itemToDelete)



# @app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
# def deleteMenuItem(restaurant_id, menu_id):
#     return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)