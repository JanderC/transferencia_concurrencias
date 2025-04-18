from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.transaction_service import TransactionService
from services.account_service import AccountService

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('/')
def list_transactions():
    transactions = TransactionService.get_all_transactions()
    accounts = AccountService.get_all_accounts()
    return render_template('transactions.html', transactions=transactions, accounts=accounts)

# En transaction_controller.py, modifica el método create_deposit
@transaction_bp.route('/deposit', methods=['POST'])
def create_deposit():
    account_id = int(request.form.get('account_id'))
    amount = float(request.form.get('amount'))
    
    if amount <= 0:
        return jsonify({'success': False, 'message': 'El monto debe ser mayor que cero'})
    
    transaction = TransactionService.create_deposit(account_id, amount)
    
    if transaction:
        account = AccountService.get_account_by_id(account_id)
        return jsonify({
            'success': True,
            'transaction': {
                'id': transaction.id,
                'type': transaction.transaction_type,
                'amount': float(transaction.amount)  # Convertir explícitamente a float
            },
            'account': {
                'id': account.id,
                'balance': float(account.balance)  # Convertir explícitamente a float
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Error al realizar el depósito'})
        
    account_id = int(request.form.get('account_id'))
    amount = float(request.form.get('amount'))
    
    if amount <= 0:
        return jsonify({'success': False, 'message': 'El monto debe ser mayor que cero'})
    
    transaction = TransactionService.create_deposit(account_id, amount)
    
    if transaction:
        account = AccountService.get_account_by_id(account_id)
        return jsonify({
            'success': True,
            'transaction': {
                'id': transaction.id,
                'type': transaction.transaction_type,
                'amount': transaction.amount
            },
            'account': {
                'id': account.id,
                'balance': account.balance
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Error al realizar el depósito'})

@transaction_bp.route('/withdraw', methods=['POST'])
def create_withdrawal():
    account_id = int(request.form.get('account_id'))
    amount = float(request.form.get('amount'))
    
    if amount <= 0:
        return jsonify({'success': False, 'message': 'El monto debe ser mayor que cero'})
    
    transaction = TransactionService.create_withdrawal(account_id, amount)
    
    if transaction:
        account = AccountService.get_account_by_id(account_id)
        return jsonify({
            'success': True,
            'transaction': {
                'id': transaction.id,
                'type': transaction.transaction_type,
                'amount': transaction.amount
            },
            'account': {
                'id': account.id,
                'balance': account.balance
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Fondos insuficientes o error al realizar el retiro'})

@transaction_bp.route('/transfer', methods=['POST'])
def create_transfer():
    from_account_id = int(request.form.get('from_account_id'))
    to_account_id = int(request.form.get('to_account_id'))
    amount = float(request.form.get('amount'))
    
    if amount <= 0:
        return jsonify({'success': False, 'message': 'El monto debe ser mayor que cero'})
    
    if from_account_id == to_account_id:
        return jsonify({'success': False, 'message': 'No puedes transferir a la misma cuenta'})
    
    transaction = TransactionService.create_transfer(from_account_id, to_account_id, amount)
    
    if transaction:
        from_account = AccountService.get_account_by_id(from_account_id)
        to_account = AccountService.get_account_by_id(to_account_id)
        return jsonify({
            'success': True,
            'transaction': {
                'id': transaction.id,
                'type': transaction.transaction_type,
                'amount': transaction.amount
            },
            'from_account': {
                'id': from_account.id,
                'balance': from_account.balance
            },
            'to_account': {
                'id': to_account.id,
                'balance': to_account.balance
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Fondos insuficientes o error al realizar la transferencia'})
