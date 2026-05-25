import sqlite3
import sys

def delete_user(username_or_email):
    conn = sqlite3.connect('database/burnout.db')
    c = conn.cursor()
    
    # Find the user
    c.execute('SELECT id, username FROM users WHERE username = ? OR email = ?', (username_or_email, username_or_email))
    user = c.fetchone()
    
    if user:
        user_id, username = user
        # Foreign key constraints mean we must delete their surveys and predictions first
        c.execute('DELETE FROM predictions WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM weekly_responses WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        print(f"✅ Successfully deleted user '{username}' and all their survey data from the local database.")
    else:
        print(f"❌ Could not find a user with username or email '{username_or_email}'.")
        
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python delete_user.py <username_or_email>")
    else:
        delete_user(sys.argv[1])
