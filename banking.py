from db import get_connection

def get_account_id(user_id):
    """Get account_id for a user"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM accounts WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return result[0] if result else None

def get_balance(user_id):
    """Get current balance for a user"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor()
    cursor.execute(
        "SELECT balance FROM accounts WHERE user_id = %s",
        (user_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return float(result[0]) if result else None

def deposit(user_id, amount):
    """Deposit money into user's account"""
    if amount <= 0:
        print("Amount must be positive!")
        return False
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        account_id = get_account_id(user_id)
        
        # Update balance
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE user_id = %s",
            (amount, user_id)
        )
        
        # Record transaction
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, description) VALUES (%s, %s, %s, %s)",
            (account_id, 'deposit', amount, f"Deposited ${amount:.2f}")
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Successfully deposited ${amount:.2f}")
        return True
    except Exception as e:
        print(f"Error depositing: {e}")
        return False

def withdraw(user_id, amount):
    """Withdraw money from user's account"""
    if amount <= 0:
        print("Amount must be positive!")
        return False
    
    balance = get_balance(user_id)
    if balance is None:
        return False
    
    if balance < amount:
        print(f"Insufficient funds! Current balance: ${balance:.2f}")
        return False
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        account_id = get_account_id(user_id)
        
        # Update balance
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE user_id = %s",
            (amount, user_id)
        )
        
        # Record transaction
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, description) VALUES (%s, %s, %s, %s)",
            (account_id, 'withdrawal', amount, f"Withdrew ${amount:.2f}")
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Successfully withdrew ${amount:.2f}")
        return True
    except Exception as e:
        print(f"Error withdrawing: {e}")
        return False

def transfer(from_user_id, to_username, amount):
    """Transfer money from one user to another"""
    if amount <= 0:
        print("Amount must be positive!")
        return False
    
    balance = get_balance(from_user_id)
    if balance is None:
        return False
    
    if balance < amount:
        print(f"Insufficient funds! Current balance: ${balance:.2f}")
        return False
    
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Get recipient user_id
        cursor.execute("SELECT id FROM users WHERE username = %s", (to_username,))
        result = cursor.fetchone()
        if not result:
            print(f"User '{to_username}' not found!")
            return False
        
        to_user_id = result[0]
        
        if from_user_id == to_user_id:
            print("Cannot transfer to yourself!")
            return False
        
        from_account_id = get_account_id(from_user_id)
        to_account_id = get_account_id(to_user_id)
        
        # Deduct from sender
        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE user_id = %s",
            (amount, from_user_id)
        )
        
        # Add to recipient
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE user_id = %s",
            (amount, to_user_id)
        )
        
        # Record transactions
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, related_account_id, description) VALUES (%s, %s, %s, %s, %s)",
            (from_account_id, 'transfer_out', amount, to_account_id, f"Transferred ${amount:.2f} to {to_username}")
        )
        cursor.execute(
            "INSERT INTO transactions (account_id, transaction_type, amount, related_account_id, description) VALUES (%s, %s, %s, %s, %s)",
            (to_account_id, 'transfer_in', amount, from_account_id, f"Received ${amount:.2f} from transfer")
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Successfully transferred ${amount:.2f} to {to_username}")
        return True
    except Exception as e:
        print(f"Error transferring: {e}")
        return False

def get_transaction_history(user_id, limit=10):
    """Get transaction history for a user"""
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        account_id = get_account_id(user_id)
        
        cursor.execute(
            "SELECT transaction_type, amount, description, created_at FROM transactions WHERE account_id = %s ORDER BY created_at DESC LIMIT %s",
            (account_id, limit)
        )
        
        transactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return transactions
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return None
