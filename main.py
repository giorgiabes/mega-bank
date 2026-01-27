#!/usr/bin/env python3
import sys
from db import init_database
from auth import register_user, login_user
from banking import get_balance, deposit, withdraw, transfer, get_transaction_history

def display_menu(username):
    """Display main menu"""
    print("\n" + "="*40)
    print(f"Welcome, {username}!")
    print("="*40)
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Transaction History")
    print("6. Logout")
    print("="*40)

def main_menu(user_id, username):
    """Main banking menu after login"""
    while True:
        display_menu(username)
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == '1':
            balance = get_balance(user_id)
            if balance is not None:
                print(f"\nYour current balance: ${balance:.2f}")
        
        elif choice == '2':
            try:
                amount = float(input("Enter amount to deposit: $"))
                deposit(user_id, amount)
            except ValueError:
                print("Invalid amount!")
        
        elif choice == '3':
            try:
                amount = float(input("Enter amount to withdraw: $"))
                withdraw(user_id, amount)
            except ValueError:
                print("Invalid amount!")
        
        elif choice == '4':
            to_username = input("Enter recipient username: ").strip()
            try:
                amount = float(input("Enter amount to transfer: $"))
                transfer(user_id, to_username, amount)
            except ValueError:
                print("Invalid amount!")
        
        elif choice == '5':
            transactions = get_transaction_history(user_id)
            if transactions:
                print("\n" + "="*60)
                print("Transaction History")
                print("="*60)
                for tx in transactions:
                    tx_type, amount, description, created_at = tx
                    print(f"{created_at} | {tx_type:15} | ${amount:10.2f} | {description}")
                print("="*60)
            else:
                print("No transactions found.")
        
        elif choice == '6':
            print(f"Goodbye, {username}!")
            break
        
        else:
            print("Invalid option! Please choose 1-6.")

def main():
    """Main application entry point"""
    print("\n" + "="*40)
    print("  MEGA BANK - CLI Banking System")
    print("="*40)
    
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == '1':
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            user_id = login_user(username, password)
            if user_id:
                print(f"\nLogin successful!")
                main_menu(user_id, username)
        
        elif choice == '2':
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            register_user(username, password)
        
        elif choice == '3':
            print("Thank you for using Mega Bank!")
            sys.exit(0)
        
        else:
            print("Invalid option! Please choose 1-3.")

if __name__ == "__main__":
    # Initialize database on first run
    init_database()
    main()
