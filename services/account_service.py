from config.database import get_db
from models.account import Account
import psycopg2

class AccountService:
    @staticmethod
    def get_all_accounts():
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, balance, created_at FROM accounts ORDER BY id")
        accounts = [Account.from_db_row(row) for row in cursor.fetchall()]
        
        return accounts

    @staticmethod
    def get_account_by_id(account_id):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, balance, created_at FROM accounts WHERE id = %s", (account_id,))
        row = cursor.fetchone()
        
        if row:
            return Account.from_db_row(row)
        return None

    @staticmethod
    def create_account(name, initial_balance=0.0):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO accounts (name, balance) VALUES (%s, %s) RETURNING id, name, balance, created_at",
            (name, initial_balance)
        )
        row = cursor.fetchone()
        conn.commit()
        
        return Account.from_db_row(row)

    @staticmethod
    def update_balance(account_id, amount):
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("BEGIN")
            cursor.execute(
                "SELECT balance FROM accounts WHERE id = %s FOR UPDATE",
                (account_id,)
            )
            row = cursor.fetchone()
            if not row:
                cursor.execute("ROLLBACK")
                return False
            
            # Asegúrate de que ambos sean de tipo numérico
            current_balance = float(row[0])
            amount_float = float(amount)
            
            new_balance = current_balance + amount_float
            if new_balance < 0:
                cursor.execute("ROLLBACK")
                return False
            
            cursor.execute(
                "UPDATE accounts SET balance = %s WHERE id = %s",
                (new_balance, account_id)
            )
            conn.commit()
            return True
        except (psycopg2.Error, ValueError) as e:
            conn.rollback()
            print(f"Error updating balance: {e}")
            return False