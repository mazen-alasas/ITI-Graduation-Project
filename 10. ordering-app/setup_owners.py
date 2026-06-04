"""
FoodFlow — Owner Account Setup
Run this once to create owner logins for the dashboard.
Usage: python setup_owners.py
"""

import hashlib
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn_str = (
        f"DRIVER={{{os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')}}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_owner(username: str, full_name: str, password: str, role: str = 'Manager'):
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO AppOwner (Username, PasswordHash, FullName, Role)
            VALUES (?, ?, ?, ?)
        """, username, hash_password(password), full_name, role)
        conn.commit()
        print(f"  ✅  Owner '{username}' created successfully.")
    except Exception as e:
        if 'UNIQUE' in str(e) or 'duplicate' in str(e).lower():
            print(f"  ⚠️  Username '{username}' already exists — skipped.")
        else:
            print(f"  ❌  Error: {e}")
    finally:
        conn.close()


def list_owners():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OwnerID, Username, FullName, Role, CreatedAt FROM AppOwner")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print("  No owners found.")
    else:
        print(f"\n  {'ID':<5} {'Username':<20} {'Full Name':<25} {'Role':<15} {'Created'}")
        print("  " + "-" * 75)
        for row in rows:
            print(f"  {row[0]:<5} {row[1]:<20} {row[2]:<25} {row[3]:<15} {str(row[4])[:19]}")


if __name__ == '__main__':
    print("\n=== FoodFlow Owner Account Setup ===\n")
    print("1. Create new owner account")
    print("2. List existing owners")
    print("3. Exit")
    print()

    choice = input("Choose (1/2/3): ").strip()

    if choice == '1':
        print()
        username  = input("Username (e.g. admin):          ").strip()
        full_name = input("Full Name (e.g. Ali Elsabaa):   ").strip()
        password  = input("Password:                       ").strip()
        role      = input("Role [Manager/Admin] (default: Manager): ").strip() or 'Manager'

        if not username or not full_name or not password:
            print("  ❌  All fields are required.")
        else:
            create_owner(username, full_name, password, role)

    elif choice == '2':
        list_owners()

    elif choice == '3':
        print("  Bye!")

    else:
        print("  Invalid choice.")

    print()
