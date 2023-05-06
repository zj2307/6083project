from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField, DecimalField, IntegerField, \
    TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateShowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=1024)])
    type = SelectField('Type', choices=[('drama', 'Drama'), ('musical', 'Musical'), ('comedy', 'Comedy'),
                                        ('horror', 'Horror'), ('adventure', 'Adventure')], validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S',
                               render_kw={'class': 'form-control'}, validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S',
                             render_kw={'class': 'form-control'}, validators=[DataRequired()])
    wheelchair_accessible = SelectField('Wheelchair Accessible', choices=[('Yes', 'Yes'), ('No', 'No')],
                                        validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Update Show')


class UpdateAttractionForm(FlaskForm):
    attraction_name = StringField('Attraction Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    type = SelectField('Type', validators=[DataRequired()],
                       choices=[('roller coaster', 'Roller Coaster'),
                                ('water ride', 'Water Ride'),
                                ('dark ride', 'Dark Ride'),
                                ('kid ride', 'Kid Ride')])
    status = SelectField('Status', validators=[DataRequired()],
                         choices=[('open', 'Open'),
                                  ('closed', 'Closed'),
                                  ('under maintenance', 'Under Maintenance')])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    minimum_height = IntegerField('Minimum Height', validators=[DataRequired()])
    duration_in_minutes = IntegerField('Duration in Minutes', validators=[DataRequired()])
    location_section = SelectField('Location Section', validators=[DataRequired()],
                                   choices=[('Lot A', 'Lot A'),
                                            ('Lot B', 'Lot B'),
                                            ('Lot C', 'Lot C'),
                                            ('Lot D', 'Lot D')])
    submit = SubmitField('Update Attraction')


class UpdateStoreForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()],
                           choices=[('Food stall', 'Food stall'),
                                    ('Ice cream parlor', 'Ice cream parlor'),
                                    ('Restaurant', 'Restaurant'),
                                    ('Gift Shop', 'Gift Shop'),
                                    ('Apparels', 'Apparels')])
    menu_item = StringField('Menu Item', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    unit_price = DecimalField('Unit Price', validators=[DataRequired()])
    submit = SubmitField('Update Store')


class UpdateUserInfoForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = IntegerField('Zip', validators=[DataRequired()])
    submit = SubmitField('Update Information')


class InsertShowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=1024)])
    type = SelectField('Type', choices=[('drama', 'Drama'), ('musical', 'Musical'), ('comedy', 'Comedy'),
                                        ('horror', 'Horror'), ('adventure', 'Adventure')], validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S',
                               render_kw={'class': 'form-control'}, validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S',
                             render_kw={'class': 'form-control'}, validators=[DataRequired()])
    wheelchair_accessible = SelectField('Wheelchair Accessible', choices=[('Yes', 'Yes'), ('No', 'No')],
                                        validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Show')


class InsertAttractionForm(FlaskForm):
    attraction_name = StringField('Attraction Name', validators=[DataRequired(), Length(min=1, max=30)])
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=1024)])
    type = SelectField('Type', validators=[DataRequired()], choices=[('roller coaster', 'Roller Coaster'), ('water ride', 'Water Ride'), ('dark ride', 'Dark Ride'), ('kid ride', 'Kid Ride')])
    status = SelectField('Status', validators=[DataRequired()], choices=[('open', 'Open'), ('closed', 'Closed'), ('under maintenance', 'Under Maintenance')])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    minimum_height = IntegerField('Minimum Height', validators=[DataRequired()])
    duration_in_minutes = IntegerField('Duration in Minutes', validators=[DataRequired()])
    location_section = SelectField('Location Section', validators=[DataRequired()], choices=[('Lot A', 'Lot A'), ('Lot B', 'Lot B'), ('Lot C', 'Lot C'), ('Lot D', 'Lot D')])
    submit = SubmitField('Insert Attraction')


class InsertStoreForm(FlaskForm):
    name = StringField("Store Name", validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()], choices=[
        ('Food stall', 'Food stall'),
        ('Ice cream parlor', 'Ice cream parlor'),
        ('Restaurant', 'Restaurant'),
        ('Gift Shop', 'Gift Shop'),
        ('Apparels', 'Apparels'),
    ])
    menu_item = StringField("Menu Item", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    unit_price = DecimalField("Unit Price", validators=[DataRequired()], places=2)
    submit = SubmitField("Insert Store")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=1, max=20)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class PurchaseTicketForm(FlaskForm):
    visit_date = DateTimeField('Visit Date', format='%Y-%m-%d',
                               render_kw={'class': 'form-control'}, validators=[DataRequired()])
    ticket_type = SelectField('Ticket Type', choices=[('child', 'Child'), ('adult', 'Adult'), ('senior', 'Senior'),
                                        ('member', 'Member')], validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    submit = SubmitField('Purchase Ticket')




