from flask import Flask, session, render_template, request, redirect, url_for, flash, get_flashed_messages, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm, UpdateShowForm, UpdateAttractionForm, UpdateStoreForm, UpdateUserInfoForm, InsertShowForm, \
    InsertAttractionForm, InsertStoreForm, ChangePasswordForm, PurchaseTicketForm
from models import *
from extensions import db, migrate
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from datetime import datetime
from waitress import serve

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:89931166@localhost/6083test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate.init_app(app, db)


@app.route('/')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard' if current_user.permission == 'user' else 'admin_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password.encode('utf-8')):
            login_user(user)
            if user.permission == 'user':
                return redirect(url_for('user_dashboard'))
            elif user.permission == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid permission value.')
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('index'))
    return render_template('index.html', title='Login', form=form, messages=get_flashed_messages())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cell_number = request.form['cell_number']
        email_address = request.form['email_address']
        hashed_password = bcrypt.generate_password_hash(password.encode('utf-8')).decode('utf-8')
        new_user = User(username=username, password=hashed_password, cell_number=cell_number,
                        email_address=email_address, permission='user')

        # check the user name if exist
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        db.session.add(new_user)
        db.session.commit()

        flash('registration success!')
        return redirect(url_for('index'))

    return render_template('register.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    attractions = Attraction.query.all()
    shows = Show.query.all()
    return render_template('user_dashboard.html', attractions=attractions, shows=shows)


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    shows = Show.query.all()
    attractions = Attraction.query.all()
    stores = Store.query.all()

    payment_total = get_payment_total()
    visitor_counts = get_visitor_counts()

    chart_data = {
        'payment_total': payment_total,
        'visitor_counts': visitor_counts,
    }

    return render_template('admin_dashboard.html', shows=shows, attractions=attractions, stores=stores,
                           chart_data=chart_data)


def get_payment_total():
    total = db.session.query(func.sum(Payment.payment_amount)).scalar()
    return total if total is not None else 0


def get_visitor_counts():
    visitor_attraction_count = db.session.query(VisitorAttraction).count()
    visitor_show_count = db.session.query(VisitorShow).count()
    return {
        'attractions': visitor_attraction_count,
        'shows': visitor_show_count
    }


@app.route('/update_show/<int:show_id>', methods=['GET', 'POST'])
def update_show(show_id):
    show = Show.query.get(show_id)
    form = UpdateShowForm()

    if form.validate_on_submit():
        show.name = form.name.data
        show.description = form.description.data
        show.type = form.type.data
        show.start_time = form.start_time.data
        show.end_time = form.end_time.data
        show.wheelchair_accessible = form.wheelchair_accessible.data
        show.price = form.price.data

        db.session.commit()
        return redirect(url_for('admin_shows'))

    elif request.method == 'GET':
        form.name.data = show.name
        form.description.data = show.description
        form.type.data = show.type
        form.start_time.data = show.start_time
        form.end_time.data = show.end_time
        form.wheelchair_accessible.data = show.wheelchair_accessible
        form.price.data = show.price

    return render_template('update_show.html', form=form)


# app.py
@app.route('/update_attraction/<int:attraction_id>', methods=['GET', 'POST'])
def update_attraction(attraction_id):
    attraction = Attraction.query.get(attraction_id)
    form = UpdateAttractionForm()

    if form.validate_on_submit():
        attraction.attraction_name = form.attraction_name.data
        attraction.description = form.description.data
        attraction.type = form.type.data
        attraction.status = form.status.data
        attraction.capacity = form.capacity.data
        attraction.minimum_height = form.minimum_height.data
        attraction.duration_in_minutes = form.duration_in_minutes.data
        attraction.location_section = form.location_section.data

        db.session.commit()
        return redirect(url_for('admin_attractions'))

    elif request.method == 'GET':
        form.attraction_name.data = attraction.attraction_name
        form.description.data = attraction.description
        form.type.data = attraction.type
        form.status.data = attraction.status
        form.capacity.data = attraction.capacity
        form.minimum_height.data = attraction.minimum_height
        form.duration_in_minutes.data = attraction.duration_in_minutes
        form.location_section.data = attraction.location_section

    return render_template('update_attraction.html', form=form)


@app.route('/update_store/<int:store_id>', methods=['GET', 'POST'])
def update_store(store_id):
    store = Store.query.get(store_id)
    form = UpdateStoreForm()

    if form.validate_on_submit():
        store.name = form.name.data
        store.category = form.category.data
        store.menu_item = form.menu_item.data
        store.description = form.description.data
        store.unit_price = form.unit_price.data
        db.session.commit()
        return redirect(url_for('admin_stores'))

    form.name.data = store.name
    form.category.data = store.category
    form.menu_item.data = store.menu_item
    form.description.data = store.description
    form.unit_price.data = store.unit_price
    return render_template('update_store.html', form=form)


@app.route('/update_user_info', methods=['GET', 'POST'])
def update_user_info():
    visitor = Visitor.query.filter_by(cell_number=current_user.cell_number).first()
    form = UpdateUserInfoForm()

    if form.validate_on_submit():
        visitor.first_name = form.first_name.data
        visitor.last_name = form.last_name.data
        visitor.street = form.street.data
        visitor.city = form.city.data
        visitor.state = form.state.data
        visitor.zip = form.zip.data
        db.session.commit()
        return redirect(url_for('user_dashboard'))

    form.first_name.data = visitor.first_name
    form.last_name.data = visitor.last_name
    form.street.data = visitor.street
    form.city.data = visitor.city
    form.state.data = visitor.state
    form.zip.data = visitor.zip
    return render_template('update_user_info.html', form=form)


@app.route('/delete_show/<int:show_id>', methods=['GET', 'POST'])
def delete_show(show_id):
    show_to_delete = Show.query.get(show_id)
    if show_to_delete:
        db.session.delete(show_to_delete)
        db.session.commit()
    else:
        flash('Show not found', 'danger')
    return redirect(url_for('admin_shows'))


@app.route('/insert_show', methods=['GET', 'POST'])
def insert_show():
    form = InsertShowForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        type = form.type.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        wheelchair_accessible = form.wheelchair_accessible.data
        price = form.price.data

        new_show = Show(name=name, description=description, type=type, start_time=start_time, end_time=end_time,
                        wheelchair_accessible=wheelchair_accessible, price=price)
        db.session.add(new_show)
        db.session.commit()

        return redirect(url_for('admin_shows'))
    return render_template('insert_show.html', form=form)


@app.route('/delete_attraction/<int:attraction_id>', methods=['GET', 'POST'])
def delete_attraction(attraction_id):
    attraction_to_delete = Attraction.query.get(attraction_id)
    if attraction_to_delete:
        db.session.delete(attraction_to_delete)
        db.session.commit()
    else:
        flash('Attraction not found', 'danger')
    return redirect(url_for('admin_attractions'))


@app.route('/insert_attraction', methods=['GET', 'POST'])
def insert_attraction():
    form = InsertAttractionForm()
    if form.validate_on_submit():
        attraction_name = form.attraction_name.data
        description = form.description.data
        type = form.type.data
        status = form.status.data
        capacity = form.capacity.data
        minimum_height = form.minimum_height.data
        duration_in_minutes = form.duration_in_minutes.data
        location_section = form.location_section.data

        new_attraction = Attraction(attraction_name=attraction_name, description=description, type=type, status=status, capacity=capacity, minimum_height=minimum_height, duration_in_minutes=duration_in_minutes, location_section=location_section)
        db.session.add(new_attraction)
        db.session.commit()

        return redirect(url_for('admin_attractions'))
    return render_template('insert_attraction.html', form=form)


@app.route('/insert_store', methods=['GET', 'POST'])
def insert_store():
    form = InsertStoreForm()
    if form.validate_on_submit():
        new_store = Store(
            name=form.name.data,
            category=form.category.data,
            menu_item=form.menu_item.data,
            description=form.description.data,
            unit_price=form.unit_price.data
        )
        db.session.add(new_store)
        db.session.commit()
        return redirect(url_for("admin_stores"))
    return render_template("insert_store.html", form=form)


@app.route('/delete_store/<int:store_id>', methods=['GET', 'POST'])
def delete_store(store_id):
    store_to_delete = Store.query.get(store_id)
    if store_to_delete:
        db.session.delete(store_to_delete)
        db.session.commit()
    else:
        flash('Store not found', 'danger')
    return redirect(url_for('admin_stores'))


@app.route('/your_information')
@login_required
def your_information():
    user = User.query.filter_by(username=current_user.username).first()
    user_visitors = Visitor.query.filter_by(cell_number=user.cell_number).all()
    return render_template('your_information.html', visitors=user_visitors)


@app.route('/my_records')
@login_required
def my_records():
    user = User.query.filter_by(username=current_user.username).first()
    user_visitors = Visitor.query.filter_by(cell_number=user.cell_number).all()

    user_tickets = []
    user_show_data = []
    user_attraction_data = []
    user_parking_data = []
    user_payment_data = []
    user_orders = []

    for visitor in user_visitors:
        user_tickets.extend(Ticket.query.filter_by(visitor_id=visitor.visitor_id).all())
        user_parking_data.extend(Parking.query.filter_by(visitor_id=visitor.visitor_id).all())
        user_payment_data.extend(Payment.query.filter_by(visitor_id=visitor.visitor_id).all())

        visitor_orders = Order.query.filter_by(visitor_id=visitor.visitor_id).all()
        for order in visitor_orders:
            store = Store.query.filter_by(store_id=order.store_id).first()
            order.store_name = store.name
            user_orders.append(order)

        user_visitor_shows = VisitorShow.query.filter_by(visitor_id=visitor.visitor_id).all()
        for visitor_show in user_visitor_shows:
            show = Show.query.filter_by(show_id=visitor_show.show_id).first()
            user_show_data.append(show)

        user_visitor_attractions = VisitorAttraction.query.filter_by(visitor_id=visitor.visitor_id).all()
        for visitor_attraction in user_visitor_attractions:
            attraction = Attraction.query.filter_by(attraction_id=visitor_attraction.attraction_id).first()
            user_attraction_data.append(attraction)

    return render_template('my_records.html', tickets=user_tickets, shows=user_show_data,
                           attractions=user_attraction_data, parkings=user_parking_data,
                           payments=user_payment_data, orders=user_orders)


@app.route('/admin_shows')
def admin_shows():
    # Query all shows
    all_shows = Show.query.all()
    return render_template('admin_shows.html', shows=all_shows)


@app.route('/admin_attractions')
def admin_attractions():
    # Query all attractions
    all_attractions = Attraction.query.all()
    return render_template('admin_attractions.html', attractions=all_attractions)


@app.route('/admin_stores')
def admin_stores():
    # Query all stores
    all_stores = Store.query.all()
    return render_template('admin_stores.html', stores=all_stores)


@app.route('/change-password_user', methods=['GET', 'POST'])
@login_required
def change_password_user():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()

        if user and bcrypt.check_password_hash(user.password, form.old_password.data.encode('utf-8')):
            user.password = bcrypt.generate_password_hash(form.new_password.data.encode('utf-8')).decode('utf-8')
            db.session.commit()
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('change_password_user.html', title='Change Password', form=form, error_msg='Incorrect old password. Please try again.')

    return render_template('change_password_user.html', title='Change Password', form=form)


@app.route('/change-password_admin', methods=['GET', 'POST'])
@login_required
def change_password_admin():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()

        if user and bcrypt.check_password_hash(user.password, form.old_password.data.encode('utf-8')):
            user.password = bcrypt.generate_password_hash(form.new_password.data.encode('utf-8')).decode('utf-8')
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('change_password_admin.html', title='Change Password', form=form, error_msg='Incorrect old password. Please try again.')

    return render_template('change_password_admin.html', title='Change Password', form=form)


@app.route('/purchase_ticket', methods=['GET', 'POST'])
@login_required
def purchase_ticket():
    form = PurchaseTicketForm()
    purchase_date = datetime.now()
    ticket_method = 'online'
    if form.validate_on_submit():
        visitor = Visitor.query.filter_by(cell_number=current_user.cell_number).first()
        new_ticket = Ticket(ticket_method=ticket_method,
                            purchase_date=purchase_date,
                            visit_date=form.visit_date.data,
                            type=form.ticket_type.data,
                            price=form.price.data,
                            discount=0,
                            visitor_id=visitor.visitor_id,
                            payment_id=1)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('user_dashboard'))

    return render_template('purchase_ticket.html', title='Purchase Ticket', form=form)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
