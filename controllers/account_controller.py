from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.account_service import AccountService
from services.transaction_service import TransactionService

account_bp = Blueprint('account', __name__, url_prefix='/accounts')

@account_bp.route('/')
def list_accounts():
    accounts = AccountService.get_all_accounts()
    return render_template('accounts.html', accounts=accounts)

@account_bp.route('/<int:account_id>')
def view_account(account_id):
    account = AccountService.get_account_by_id(account_id)
    transactions = TransactionService.get_account_transactions(account_id)
    return render_template('account_detail.html', account=account, transactions=transactions)

@account_bp.route('/create', methods=['POST'])
def create_account():
    name = request.form.get('name')
    initial_balance = float(request.form.get('initial_balance', 0))
    
    account = AccountService.create_account(name, initial_balance)
    
    if account:
        return jsonify({
            'success': True,
            'account': {
                'id': account.id,
                'name': account.name, 
                'balance': account.balance
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Error al crear la cuenta'})

