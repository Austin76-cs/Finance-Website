print('LOADED app/routes/plaid.py')

import os
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
import plaid
from plaid.api import plaid_api
from app import db
from app.models.user import User
# Plaid model imports
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

plaid_bp = Blueprint('plaid', __name__)

def get_plaid_client():
    configuration = plaid.Configuration(
        host=plaid.Environment.Sandbox if current_app.config['PLAID_ENVIRONMENT'] == 'sandbox' else plaid.Environment.Development,
        api_key={
            'clientId': current_app.config['PLAID_CLIENT_ID'],
            'secret': current_app.config['PLAID_SECRET'],
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

@plaid_bp.route('/create_link_token', methods=['POST'])
@login_required
def create_link_token():
    print('--- /create_link_token called ---')
    print('PLAID_ENVIRONMENT:', os.getenv('PLAID_ENVIRONMENT'))
    print('PLAID_CLIENT_ID:', os.getenv('PLAID_CLIENT_ID'))
    print('PLAID_SECRET:', os.getenv('PLAID_SECRET'))
    try:
        client = get_plaid_client()
        request_data = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=str(current_user.id)),
            client_name='Personal Finance App',
            products=[Products('transactions')],
            country_codes=[CountryCode('US')],
            language='en'
        )
        response = client.link_token_create(request_data)
        print('Link token created:', response.to_dict()['link_token'])
        return jsonify({'link_token': response.to_dict()['link_token']})
    except Exception as e:
        print('Error in create_link_token:', type(e), e)
        return jsonify({'error': str(e)}), 500

@plaid_bp.route('/exchange_public_token', methods=['POST'])
@login_required
def exchange_public_token():
    try:
        public_token = request.json.get('public_token')
        client = get_plaid_client()
        request_data = plaid_api.ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request_data)
        access_token = response.access_token
        
        # Save access token to user
        current_user.plaid_access_token = access_token
        db.session.commit()
        
        return jsonify({'success': True})
    except plaid.ApiException as e:
        return jsonify({'error': str(e)}), 400

@plaid_bp.route('/sync_transactions', methods=['POST'])
@login_required
def sync_transactions():
    if not current_user.plaid_access_token:
        return jsonify({'error': 'No Plaid access token found'}), 400
        
    try:
        client = get_plaid_client()
        request_data = plaid_api.TransactionsGetRequest(
            access_token=current_user.plaid_access_token,
            start_date='2020-01-01',
            end_date='2023-12-31'
        )
        response = client.transactions_get(request_data)
        return jsonify(response.to_dict())
    except plaid.ApiException as e:
        return jsonify({'error': str(e)}), 400

@plaid_bp.route('/api/accounts', methods=['GET'])
@login_required
def get_accounts():
    print('--- /api/accounts called ---')
    try:
        client = get_plaid_client()
        request_data = plaid_api.AccountsGetRequest(access_token=current_user.plaid_access_token)
        response = client.accounts_get(request_data)
        print('Accounts response:', response.to_dict())
        return jsonify(response.to_dict()['accounts'])
    except Exception as e:
        print('Error in /api/accounts:', type(e), e)
        return jsonify({'error': str(e)}), 500

@plaid_bp.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    print('--- /api/transactions called ---')
    try:
        start_date = datetime.now().date() - timedelta(days=30)
        end_date = datetime.now().date()
        client = get_plaid_client()
        request_data = plaid_api.TransactionsGetRequest(
            access_token=current_user.plaid_access_token,
            start_date=start_date,
            end_date=end_date
        )
        response = client.transactions_get(request_data)
        transactions = response.to_dict().get('transactions', [])
        print('Transactions response:', response.to_dict())
        print(f'Number of transactions returned: {len(transactions)}')
        return jsonify(transactions)
    except Exception as e:
        print('Error in /api/transactions:', type(e), e)
        return jsonify({'error': str(e)}), 500

@plaid_bp.route('/api/balance', methods=['GET'])
@login_required
def get_balance():
    print('--- /api/balance called ---')
    try:
        client = get_plaid_client()
        request_data = plaid_api.AccountsBalanceGetRequest(access_token=current_user.plaid_access_token)
        response = client.accounts_balance_get(request_data)
        print('Balance response:', response.to_dict())
        return jsonify(response.to_dict()['accounts'])
    except Exception as e:
        print('Error in /api/balance:', type(e), e)
        return jsonify({'error': str(e)}), 500 