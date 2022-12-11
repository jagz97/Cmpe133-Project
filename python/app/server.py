# source /Users/tnappy/node_projects/quickstart/python/bin/activate
# Read env vars from .env file


from plaid.exceptions import ApiException
from plaid.model.payment_amount import PaymentAmount
from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
from plaid.model.payment_initiation_address import PaymentInitiationAddress
from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
from plaid.model.payment_initiation_payment_create_request import PaymentInitiationPaymentCreateRequest
from plaid.model.payment_initiation_payment_get_request import PaymentInitiationPaymentGetRequest
from plaid.model.link_token_create_request_payment_initiation import LinkTokenCreateRequestPaymentInitiation
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.asset_report_create_request import AssetReportCreateRequest
from plaid.model.asset_report_create_request_options import AssetReportCreateRequestOptions
from plaid.model.asset_report_user import AssetReportUser
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_get_request import TransferGetRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_user_in_request import TransferUserInRequest
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.api import plaid_api
from flask import Flask, send_file
from flask import render_template, session
from flask import request
from flask import jsonify
from datetime import datetime
from datetime import timedelta
import plaid
import base64
import os
import datetime
import json
import time
from dotenv import load_dotenv
from werkzeug.wrappers import response



from datetime import datetime
import secrets
from flask import render_template, redirect, url_for, request, flash, session, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash, generate_password_hash


from app import app as app
from app import db, photos, mail
from app.forms import  LoginForm, SignUpForm

from .models import User
from .ReceiptDB import Category, AddReceipt
from .forms import Addreceipt



load_dotenv()


########################################################################
################### PLAID API SETUP ####################################
########################################################################




# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
# PLAID_PRODUCTS is a comma-separated list of products to use when initializing
# Link. Note that this list must contain 'assets' in order for the app to be
# able to create and retrieve asset reports.
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')

# PLAID_COUNTRY_CODES is a comma-separated list of countries for which users
# will be able to select institutions from.
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')


def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value

host = plaid.Environment.Sandbox

if PLAID_ENV == 'sandbox':
    host = plaid.Environment.Sandbox

if PLAID_ENV == 'development':
    host = plaid.Environment.Development

if PLAID_ENV == 'production':
    host = plaid.Environment.Production

# Parameters used for the OAuth redirect Link flow.
#
# Set PLAID_REDIRECT_URI to 'http://localhost:3000/'
# The OAuth redirect flow requires an endpoint on the developer's website
# that the bank website should redirect to. You will need to configure
# this redirect URI for your client ID through the Plaid developer dashboard
# at https://dashboard.plaid.com/team/api.
PLAID_REDIRECT_URI = empty_to_none('PLAID_REDIRECT_URI')

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': '2020-09-14'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))


# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
# The payment_id is only relevant for the UK Payment Initiation product.
# We store the payment_id in memory - in production, store it in a secure
# persistent data store.
payment_id = None
# The transfer_id is only relevant for Transfer ACH product.
# We store the transfer_id in memomory - in produciton, store it in a secure
# persistent data store
transfer_id = None

item_id = None



@app.route('/addCategory', methods = ['GET','POST'])
def addCategory():
    """
    Allows the customer to add categories to manage their receipts.
    Updates Category database to include user-inputted String
    """
    if request.method =="POST":
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        flash(f'You have added the category {getCategory} !', 'success')
        db.session.commit()
        return redirect(url_for('addCategory'))

    return render_template('receipts/addCategory.html',categories = 'categories')

@app.route('/updateCategory/<int:id>', methods = ['GET','POST'])
def updateCategory(id):
    """
    Allows the user to modify or delete categories within the database
    """
    updateCategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =='POST':
        updateCategory.name = category
        flash(f'The category has been updated!','success')
        db.session.commit()
        return redirect(url_for('updateCategory/<int:id>'))
    return render_template('receipts/updateCategory.html', title = 'Update Category page', updateCategory = updateCategory)

@app.route('/deleteCategory/<int:id>', methods =['POST'])
def deleteCategory(id):
    """
    Allows the user to delete categories already in the database.
    """
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        flash(f'The category has been deleted!', ' success')
        return redirect(url_for('viewCategories'))

@app.route('/categories')
def viewCategories():
    """
    Allows the user to view categories already in the database.
    """
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('receipts/categories.html', title = 'Categories', categories = categories)



@app.route('/addReceipt', methods = ['GET','POST'])
def addreceipt():
    """
    Allows the user to add a receipt to the database.
    """
    categories = Category.query.all()
    form = Addreceipt(request.form)
    if request.method =='POST':
        name = form.name.data
        merchant = form.merchant.data
        dateOfPurchase = form.dateOfPurchase.data
        returnDate = form.returnDate.data
        totalPrice = form.totalPrice.data
        numberOfItems = form.numberOfItems.data
        description = form.description.data
        category = request.form.get('category')
        uploadreceipt = AddReceipt(name=name,merchant=merchant,dateOfPurchase=dateOfPurchase,returnDate=returnDate,
                                totalPrice=totalPrice,numberOfItems=numberOfItems,description=description,
                                category_id = category)
        db.session.add(uploadreceipt)
        
        db.session.commit()
        return redirect(url_for('library'))
    return render_template('receipts/addReceipt.html',title = "Add Receipt Page", form = form,categories = categories)

@app.route('/updateReceipt/<int:id>', methods = ('GET','POST'))
def updateReceipt(id):
    """
    Allows the user to modify receipt information already in the database.
    """
    categories = Category.query.all()
    receipt = AddReceipt.query.get_or_404(id)
    category = request.form.get('category')
    form = Addreceipt(request.form)
    if request.method =='POST':
        receipt.name = form.name.data
        receipt.merchant = form.merchant.data
        receipt.category_id = category
        receipt.dateOfPurchase = form.dateOfPurchase.data
        receipt.returnDate = form.returnDate.data
        receipt.totalPrice = form.totalPrice.data
        form.numberOfItems = form.totalPrice.data
        form.description = form.description.data
        db.session.commit()
        flash(f'Receipt updated!','success')
        return redirect(url_for('library'))
    form.name.data = receipt.name
    form.merchant.data = receipt.merchant
    form.dateOfPurchase.data = receipt.dateOfPurchase
    form.returnDate.data = receipt.returnDate
    form.totalPrice.data = receipt.totalPrice
    form.numberOfItems.data = receipt.numberOfItems
    form.description.data = receipt.description

    form = Addreceipt(request.form)

    return render_template ('receipts/updateReceipt.html', form = form, categories = categories, receipt =receipt)

@app.route('/deleteReceipt/<int:id>', methods = ['POST'])
def deleteReceipt(id):
    """
    Allows the delete to receipts already in the database.
    """
    receipt = AddReceipt.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(receipt)
        db.session.commit()
        flash(f'The receipt has been deleted!')
        return redirect(url_for('library'))
    return redirect(url_for('library'))


@app.route('/library', methods=['GET','POST'])
def library():
    """
    Displays the user's uploaded receipts and retrieves values associated with receipts from database
    """
    receipts = AddReceipt.query.all()
    return render_template ('library.html', title = "Library", receipts = receipts)

@app.route('/support', methods= ['GET','POST'])
def support():
    """
    Allows the user to access support for any issues they may have.
    The user may also request an E-mail to speak with an agent via email
    """
    if request.method == 'POST':
        email = request.form.get("email")
        msg = Message("Support", sender = "receiptify@receiptify.com", recipients = [email] )
        msg.body = "Hello there," \
                   "I hope everything is going okay and you're enjoying Receiptify so far, if you have any questions " \
                   "just let us know by replying to this email!"
        mail.send(msg)
        flash(f'Message has been sent!')
        return redirect(url_for('support'))
    return render_template('support.html', title = "Support")


@app.route('/CSV', methods = ['GET'])
def CSV():
    """
    Allows the user to download receipt information from the database
    """
    info = AddReceipt.query.all()

    with open ('test.csv','w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        csvwriter.writerow(["ID","Name","Merchant","Date of Purchase","Return Date", "Price", "number of Items", "Description", "Category"])
        for i in info:
            csvwriter.writerow([i.id, i.name, i.merchant, i.dateOfPurchase , i.returnDate , i.totalPrice , i.numberOfItems, i.description])

    return send_file('../test.csv', mimetype='text/csv', attachment_filename='receipts.csv', as_attachment= True)




########################################################################
################### ALL APP ROUTES  ####################################
########################################################################



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Manges the login for customer trying to login
    Checks for the password and retrieve the user profile for right user
    """
    if current_user.is_authenticated:
        print(current_user.id)
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signUp', methods=['GET', 'POST'])
def signup():
    """
    Manages the signup for Customer
    Retrieves info from the signup form and adds it to the database
    """
    if not current_user.is_authenticated:
        form = SignUpForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            access_token = str('access-sandbox-dc1a7d2a-748b-47ef-8d78-55afd577c169')

            try:
                newuser = User(username=username, email=email, password_hash=password_hash, access_token=access_token)
                db.session.add(newuser)
                db.session.commit()
                flash('Account created for user {}'.format(form.username.data))
            except Exception:
                flash('Username or email is taken')
                return redirect(url_for('signup'))
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Sign Up', form=form)


@app.route('/logout')
def logout():
    """
    Manges the logout response from user
    Securely logs out the customer and redirects them to login page
    """
    logout_user()
    return redirect(url_for('login'))



@app.route('/')
def index():
    
    return render_template('base.html', id = id)





@app.route('/profile')
def profile():
    return render_template('profile.html')







@app.route('/api/info', methods=['POST'])
def info():
    global access_token
    global item_id
    return jsonify({
        'item_id': item_id,
        'access_token': access_token,
        'products': PLAID_PRODUCTS
    })





@app.route('/api/create_link_token', methods=['POST'])
def create_link_token():
        print(current_user)
        request = LinkTokenCreateRequest(
            products=products,
            client_name="Plaid Quickstart",
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )
        if PLAID_REDIRECT_URI!=None:
            request['redirect_uri']=PLAID_REDIRECT_URI
    # create link token
        response = client.link_token_create(request)
        return jsonify(response.to_dict())
    


# Exchange token flow - exchange a Link public_token for
# an API access_token
# https://plaid.com/docs/#exchange-token-flow

access_token = None

@app.route('/api/set_access_token', methods=['POST'])
def get_access_token():
    global access_token
    global item_id
    global transfer_id
    public_token = request.form['public_token']
    
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        if 'transfer' in PLAID_PRODUCTS:
            transfer_id = authorize_and_create_transfer(access_token)

        return jsonify(exchange_response.to_dict())
    except plaid.ApiException as e:
        return json.loads(e.body)


@app.route('/token')
def token():


    current_user.access_token = access_token
    db.session.commit()
    return render_template('base.html', access_token= access_token)


# Retrieve ACH or ETF account numbers for an Item
# https://plaid.com/docs/#auth


@app.route('/api/auth', methods=['GET'])
def get_auth():
    try:
       request = AuthGetRequest(
            access_token=current_user.access_token
        )
       response = client.auth_get(request)
       pretty_print_response(response.to_dict())
       data =  jsonify(response.to_dict())
    except plaid.ApiException as e:
        error_response = format_error(e)
        data_error= jsonify(error_response)
        
    return render_template('profile.html', data = data)


# Retrieve Transactions for an Item
# https://plaid.com/docs/#transactions


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    # Set cursor to empty to receive all historical updates
    cursor = ''

    # New transaction updates since "cursor"
    added = []
    modified = []
    removed = [] # Removed transaction ids
    has_more = True
    access_token =current_user.access_token
    try:
        # Iterate through each page of new transaction updates for item
        while has_more:
            request = TransactionsSyncRequest(
                access_token=access_token,
                cursor=cursor,
            )
            response = client.transactions_sync(request).to_dict()
            # Add this page of results
            added.extend(response['added'])
            modified.extend(response['modified'])
            removed.extend(response['removed'])
            has_more = response['has_more']
            # Update cursor to the next cursor
            cursor = response['next_cursor']
            pretty_print_response(response)

        # Return the 8 most recent transactions
        latest_transactions = sorted(added, key=lambda t: t['date'])[-30:]
        

    except plaid.ApiException as e:
        error_response = format_error(e)
        data_error = jsonify(error_response)
    
    return render_template('dashboard.html', title='Sign Up',data = latest_transactions)


# Retrieve Identity data for an Item
# https://plaid.com/docs/#identity


@app.route('/api/identity', methods=['GET'])
def get_identity():
    try:
        request = IdentityGetRequest(
            access_token=access_token
        )
        response = client.identity_get(request)
        pretty_print_response(response.to_dict())
        data= jsonify(
            {'error': None, 'identity': response.to_dict()['accounts']})
    except plaid.ApiException as e:
        error_response = format_error(e)
        data= jsonify(error_response)
        

# Retrieve real-time balance data for each of an Item's accounts
# https://plaid.com/docs/#balance


@app.route('/api/balance', methods=['GET'])
def get_balance():
    try:
        request = AccountsBalanceGetRequest(
            access_token=current_user.access_token
        )
        response = client.accounts_balance_get(request)
        pretty_print_response(response.to_dict())
        data= jsonify(response.to_dict())
    except plaid.ApiException as e:
        error_response = format_error(e)
        data_e = jsonify(error_response)
    return render_template('profile.html', data = response)
# Retrieve an Item's accounts
# https://plaid.com/docs/#accounts


@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    
    request = AccountsGetRequest(
    access_token=current_user.access_token
    )
    response = client.accounts_get(request)
    pretty_print_response(response.to_dict())
    data =  jsonify(response.to_dict())
    

    return render_template('index.html', data = response)


# Create and then retrieve an Asset Report for one or more Items. Note that an
# Asset Report can contain up to 100 items, but for simplicity we're only
# including one Item here.
# https://plaid.com/docs/#assets


@app.route('/api/assets', methods=['GET'])
def get_assets():
    try:
        request = AssetReportCreateRequest(
            access_tokens=[access_token],
            days_requested=60,
            options=AssetReportCreateRequestOptions(
                webhook='https://www.example.com',
                client_report_id='123',
                user=AssetReportUser(
                    client_user_id='789',
                    first_name='Jane',
                    middle_name='Leah',
                    last_name='Doe',
                    ssn='123-45-6789',
                    phone_number='(555) 123-4567',
                    email='jane.doe@example.com',
                )
            )
        )

        response = client.asset_report_create(request)
        pretty_print_response(response.to_dict())
        asset_report_token = response['asset_report_token']
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)

    # Poll for the completion of the Asset Report.
    num_retries_remaining = 20
    asset_report_json = None
    while num_retries_remaining > 0:
        try:
            request = AssetReportGetRequest(
                asset_report_token=asset_report_token,
            )
            response = client.asset_report_get(request)
            asset_report_json = response['report']
            break
        except plaid.ApiException as e:
            response = json.loads(e.body)
            if response['error_code'] == 'PRODUCT_NOT_READY':
                num_retries_remaining -= 1
                time.sleep(1)
                continue
        error_response = format_error(e)
        return jsonify(error_response)
    if asset_report_json is None:
        return jsonify({'error': {'status_code': e.status, 'display_message':
                                  'Timed out when polling for Asset Report', 'error_code': '', 'error_type': ''}})

    asset_report_pdf = None
    try:
        request = AssetReportPDFGetRequest(
            asset_report_token=asset_report_token,
        )
        pdf = client.asset_report_pdf_get(request)
        return jsonify({
            'error': None,
            'json': asset_report_json.to_dict(),
            'pdf': base64.b64encode(pdf.read()).decode('utf-8'),
        })
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


# Retrieve investment holdings data for an Item
# https://plaid.com/docs/#investments


@app.route('/api/holdings', methods=['GET'])
def get_holdings():
    try:
        request = InvestmentsHoldingsGetRequest(access_token=access_token)
        response = client.investments_holdings_get(request)
        pretty_print_response(response.to_dict())
        return jsonify({'error': None, 'holdings': response.to_dict()})
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


# Retrieve Investment Transactions for an Item
# https://plaid.com/docs/#investments


@app.route('/api/investments_transactions', methods=['GET'])
def get_investments_transactions():
    # Pull transactions for the last 30 days

    start_date = (datetime.datetime.now() - timedelta(days=(30)))
    end_date = datetime.datetime.now()
    try:
        options = InvestmentsTransactionsGetRequestOptions()
        request = InvestmentsTransactionsGetRequest(
            access_token=access_token,
            start_date=start_date.date(),
            end_date=end_date.date(),
            options=options
        )
        response = client.investments_transactions_get(
            request)
        pretty_print_response(response.to_dict())
        return jsonify(
            {'error': None, 'investments_transactions': response.to_dict()})

    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


@app.route('/api/item', methods=['GET'])
def item():
    try:
        request = ItemGetRequest(access_token=access_token)
        response = client.item_get(request)
        request = InstitutionsGetByIdRequest(
            institution_id=response['item']['institution_id'],
            country_codes=list(map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES))
        )
        institution_response = client.institutions_get_by_id(request)
        pretty_print_response(response.to_dict())
        pretty_print_response(institution_response.to_dict())
        return jsonify({'error': None, 'item': response.to_dict()[
            'item'], 'institution': institution_response.to_dict()['institution']})
    except plaid.ApiException as e:
        error_response = format_error(e)
        return jsonify(error_response)


def pretty_print_response(response):
  print(json.dumps(response, indent=2, sort_keys=True, default=str))

def format_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
                      response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}
