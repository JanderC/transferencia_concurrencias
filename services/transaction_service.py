from config.database import get_db
from models.transaction import Transaction
import psycopg2
from services.account_service import AccountService

class TransactionService:
    @staticmethod
    def get_all_transactions():
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT t.id, t.account_id, t.recipient_id, t.amount, 
                   t.transaction_type, t.status, t.created_at
            FROM transactions t
            ORDER BY t.created_at DESC
            """
        )
        transactions = [Transaction.from_db_row(row) for row in cursor.fetchall()]
        
        return transactions

    @staticmethod
    def get_account_transactions(account_id):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT t.id, t.account_id, t.recipient_id, t.amount, 
                   t.transaction_type, t.status, t.created_at
            FROM transactions t
            WHERE t.account_id = %s OR t.recipient_id = %s
            ORDER BY t.created_at DESC
            """,
            (account_id, account_id)
        )
        transactions = [Transaction.from_db_row(row) for row in cursor.fetchall()]
        
        return transactions

    @staticmethod
    def create_deposit(account_id, amount):
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            
            # Actualizar el saldo de la cuenta
            if not AccountService.update_balance(account_id, amount):
                cursor.execute("ROLLBACK")
                return None
            
            # Registrar la transacción
            cursor.execute(
                """
                INSERT INTO transactions 
                (account_id, recipient_id, amount, transaction_type, status)
                VALUES (%s, NULL, %s, 'deposit', 'completed')
                RETURNING id, account_id, recipient_id, amount, transaction_type, status, created_at
                """,
                (account_id, amount)
            )
            row = cursor.fetchone()
            conn.commit()
            
            return Transaction.from_db_row(row)
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error creating deposit: {e}")
            return None

    @staticmethod
    def create_withdrawal(account_id, amount):
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            
            # Actualizar el saldo de la cuenta (resta)
            if not AccountService.update_balance(account_id, -amount):
                cursor.execute("ROLLBACK")
                return None
            
            # Registrar la transacción
            cursor.execute(
                """
                INSERT INTO transactions 
                (account_id, recipient_id, amount, transaction_type, status)
                VALUES (%s, NULL, %s, 'withdrawal', 'completed')
                RETURNING id, account_id, recipient_id, amount, transaction_type, status, created_at
                """,
                (account_id, amount)
            )
            row = cursor.fetchone()
            conn.commit()
            
            return Transaction.from_db_row(row)
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error creating withdrawal: {e}")
            return None

    @staticmethod
    def create_transfer(from_account_id, to_account_id, amount):
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            
            # Restar de la cuenta origen
            if not AccountService.update_balance(from_account_id, -amount):
                cursor.execute("ROLLBACK")
                return None
            
            # Sumar a la cuenta destino
            if not AccountService.update_balance(to_account_id, amount):
                cursor.execute("ROLLBACK")
                return None
            
            # Registrar la transacción
            cursor.execute(
                """
                INSERT INTO transactions 
                (account_id, recipient_id, amount, transaction_type, status)
                VALUES (%s, %s, %s, 'transfer', 'completed')
                RETURNING id, account_id, recipient_id, amount, transaction_type, status, created_at
                """,
                (from_account_id, to_account_id, amount)
            )
            row = cursor.fetchone()
            conn.commit()
            
            return Transaction.from_db_row(row)
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error creating transfer: {e}")
            return None