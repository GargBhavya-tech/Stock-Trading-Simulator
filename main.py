import yfinance as yf
import json
import os
from getpass import getpass

# File to store user data
USERS_FILE = 'users.json'

def load_users():
    """Load all users from the file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as file:
                users = json.load(file)
                
                # Fix old data format - convert 'balance' to 'cash' and 'portfolio' to 'stocks'
                for username in users:
                    if 'balance' in users[username]:
                        users[username]['cash'] = users[username].pop('balance')
                    if 'portfolio' in users[username]:
                        users[username]['stocks'] = users[username].pop('portfolio')
                    
                    # Fix stock data format (avg_price -> buy_price)
                    if 'stocks' in users[username]:
                        for symbol in users[username]['stocks']:
                            if 'avg_price' in users[username]['stocks'][symbol]:
                                users[username]['stocks'][symbol]['buy_price'] = users[username]['stocks'][symbol].pop('avg_price')
                
                # Save the updated format
                save_users(users)
                return users
        except:
            return {}
    return {}

def save_users(users):
    """Save all users to the file"""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def register_user(users):
    #Create a new account for new user
    print("\n CREATE YOUR ACCOUNT ")
    print("Let's get you set up!")
    
    username = input("\nChoose a username: ")
    
    # Check if username already exists
    if username in users:
        print("\n Sorry, that username is already taken.")
        print(" Try adding some numbers or a different spelling!")
        #same username for two user cant exist
        return users
    
    if not username:#checkin if username is empty
        print("\n Username cannot be empty!")
        return users
    
    password = getpass("Create a password: ")
    
    if not password:#checkin is password is empty
        print("\n Password cannot be empty!")
        return users
    
    # Create new user account
    #saving all the data of this user
    #in our database
    users[username] = {
        'password': password,
        'cash': 100000.0,
        'stocks': {}
    }
    
    save_users(users)
    
    print("\n Account created successfully!")
    print(f" You've been given Rs.100,000 to start your trading journey!")
    print(f" Welcome to the world of investement, {username}!")
    
    return users

def login_user(users):
    #Log into an existing account
    print("\n LOGIN TO YOUR ACCOUNT")
    
    username = input("Username: ")
    
    # Check if user exists
    if username not in users:
        print("\n We couldn't find that username.")
        print(" Make sure you've registered first, or check your spelling!")
        #only registered user can login obviously
        return None
    
    password = getpass("Password: ")
    
    # Verify password
    if users[username]['password'] == password:
        print(f"\nWelcome back, {username}!")
        print("Ready to do some trading?")
        return username
    else:
        print("\n Incorrect password.")
        print(" Please try again!")
        return None

def get_current_price(symbol):
    #Get the current stock price
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        
        if data.empty:
            return None
        
        return data['Close'].iloc[-1]
    except:
        return None

def view_portfolio(users, username):
    #users is the database
    #username is what we loggined through
    #Show the user's portfolio
    user = users[username]
    
    print("\n" + "=" * 60)#gui
    print(f" {username.upper()}'S PORTFOLIO")
    print("=" * 60)
    
    print(f"\n Available Cash: Rs.{user['cash']:,.2f}")
    #avaliable balance in account
    
    # Check if user has any stocks
    if not user['stocks']:
        print("\n You don't own any stocks yet.")
        #if stocks are empty
        print(" Time to make your first investment!")
        return
    
    print("\n YOUR STOCKS:")
    print("-" * 60)#gui
    print(f"{'Stock':<10} {'Shares':<12} {'Buy Price':<15} {'Current Price':<15} {'Profit/Loss':<15}")
    print("-" * 60)
    
    total_invested = 0
    total_current_value = 0
    
    # Show each stock
    for symbol, info in user['stocks'].items():
        shares = info['shares']
        buy_price = info['buy_price']
        
        current_price = get_current_price(symbol)
        
        if current_price:
            invested = shares * buy_price
            current_value = shares * current_price
            profit_loss = current_value - invested
            profit_percent = (profit_loss / invested) * 100
            
            total_invested += invested
            total_current_value += current_value
            
            # Show profit in green, loss in red
            if profit_loss >= 0:
                status = f" +Rs.{profit_loss:,.2f} (+{profit_percent:.1f}%)"
            else:
                status = f" Rs.{profit_loss:,.2f} ({profit_percent:.1f}%)"
            
            print(f"{symbol:<10} {shares:<12.2f} Rs.{buy_price:<14.2f} Rs.{current_price:<14.2f} {status}")
        else:
            print(f"{symbol:<10} {shares:<12.2f} Rs.{buy_price:<14.2f} {'Error':<15} {'N/A':<15}")
    
    print("-" * 60)
    
    # Calculate total portfolio value
    total_portfolio = user['cash'] + total_current_value
    total_profit = total_current_value - total_invested
    
    print(f"\n PORTFOLIO SUMMARY:")
    print(f"    Total Cash: Rs.{user['cash']:,.2f}")
    print(f"    Total Stock Value: Rs.{total_current_value:,.2f}")
    print(f"    Total Portfolio Value: Rs.{total_portfolio:,.2f}")
    
    if total_invested > 0:
        overall_profit_percent = (total_profit / total_invested) * 100
        if total_profit >= 0:
            print(f"    Overall Profit: +Rs.{total_profit:,.2f} (+{overall_profit_percent:.1f}%)")
        else:
            print(f"    Overall Loss: Rs.{total_profit:,.2f} ({overall_profit_percent:.1f}%)")

def buy_stock(users, username):
    #Buy shares of a stock
    print("\n BUY STOCKS")
    
    symbol = input("\nEnter stock symbol (e.g., AAPL, TSLA, MSFT): ").strip().upper()
    
    if not symbol:
        print(" Please enter a valid stock symbol!")
        return users
    
    print(f"\n Looking up {symbol}...")
    
    # Get current price
    #from the yfinance library
    current_price = get_current_price(symbol)
    
    if not current_price:
        print(f"\n Couldn't find stock data for {symbol}")
        print(" Make sure the symbol is correct and try again!")
        return users
    
    print(f" Current price of {symbol}: Rs.{current_price:.2f}")
    
    # Get number of shares to buy
    try:
        shares = float(input("\nHow many shares do you want to buy? "))
        
        if shares <= 0:
            print("\n Please enter a positive number of shares!")
            return users
        
    except ValueError:
        print("\n Please enter a valid number!")
        return users
    
    # Calculate total cost
    total_cost = current_price * shares
    user = users[username]
    
    print(f"\n ORDER SUMMARY:")
    print(f"   Stock: {symbol}")
    print(f"   Shares: {shares}")
    print(f"   Price per share: Rs.{current_price:.2f}")
    print(f"   Total cost: Rs.{total_cost:,.2f}")
    print(f"   Your cash: Rs.{user['cash']:,.2f}")
    
    # Check if user has enough cash
    if user['cash'] < total_cost:
        print(f"\n Insufficient funds!")
        print(f" You need Rs.{total_cost:,.2f} but only have Rs.{user['cash']:,.2f}")
        return users
    
    # # Confirm purchase
    # confirm = input("\n Do you want to proceed? (yes/no): ").strip().lower()
    
    # if confirm != 'yes':
    #     print(" Purchase cancelled.")
    #     return users
    
    # Process the purchase
    user['cash'] -= total_cost
    
    # Update stock holdings
    if symbol in user['stocks']:
        # Already own this stock - calculate new average price
        old_shares = user['stocks'][symbol]['shares']
        old_price = user['stocks'][symbol]['buy_price']
        
        new_shares = old_shares + shares
        new_avg_price = ((old_shares * old_price) + (shares * current_price)) / new_shares
        
        user['stocks'][symbol] = {
            'shares': new_shares,
            'buy_price': new_avg_price
        }
        #using nested dictionaries
    else:
        # First time buying this stock
        user['stocks'][symbol] = {
            'shares': shares,
            'buy_price': current_price
        }
    
    save_users(users)
    
    print(f"\n Purchase successful!")
    print(f" You bought {shares} shares of {symbol} at Rs.{current_price:.2f}")
    print(f" Remaining cash: Rs.{user['cash']:,.2f}")
    
    return users

def sell_stock(users, username):
    #Sell shares of a stock
    print("\n SELL STOCKS")
    
    user = users[username]
    
    # Check if user owns any stocks
    #ownership of stalks
    if not user['stocks']:
        print("\n You don't own any stocks to sell!")
        return users
    
    symbol = input("\nEnter stock symbol to sell: ").strip().upper()
    #checking if the user owns that particular stock
    if symbol not in user['stocks']:
        print(f"\n You don't own any {symbol} shares!")
        return users
    
    owned_shares = user['stocks'][symbol]['shares']
    buy_price = user['stocks'][symbol]['buy_price']
    
    print(f"\n You own {owned_shares} shares of {symbol}")
    print(f" You bought them at an average price of Rs.{buy_price:.2f}")
    
    # Get current price
    current_price = get_current_price(symbol)
    
    # if not current_price:
    #     print(f"\n Couldn't get current price for {symbol}")
    #     return users
    
    print(f" Current price: Rs.{current_price:.2f}")
    
    # Get number of shares to sell
    try:
        shares = float(input(f"\nHow many shares do you want to sell (max {owned_shares})? "))
        
        if shares <= 0:
            print("\n Please enter a positive number!")
            return users
        
        if shares > owned_shares:
            print(f"\n You only have {owned_shares} shares!")
            return users
        
    except ValueError:
        print("\n Please enter a valid number!")
        return users
    
    # Calculate sale value
    total_value = current_price * shares
    profit = (current_price - buy_price) * shares
    profit_percent = (profit / (buy_price * shares)) * 100
    
    print(f"\n SALE SUMMARY:")
    print(f"   Stock: {symbol}")
    print(f"   Shares to sell: {shares}")
    print(f"   Your buy price: Rs.{buy_price:.2f}")
    print(f"   Current price: Rs.{current_price:.2f}")
    print(f"   Sale value: Rs.{total_value:,.2f}")
    
    if profit >= 0:
        print(f"    Profit: +Rs.{profit:,.2f} (+{profit_percent:.1f}%)")
    else:
        print(f"    Loss: Rs.{profit:,.2f} ({profit_percent:.1f}%)")
    
    # Confirm sale
    confirm = input("\n Confirm sale? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print(" Sale cancelled.")
        return users
    
    # Process the sale
    user['cash'] += total_value
    user['stocks'][symbol]['shares'] -= shares
    
    # Remove stock if all shares sold
    if user['stocks'][symbol]['shares'] == 0:
        del user['stocks'][symbol]
    
    save_users(users)
    
    print(f"\n Sale successful!")
    print(f" You sold {shares} shares of {symbol} at Rs.{current_price:.2f}")
    print(f" New cash balance: Rs.{user['cash']:,.2f}")
    
    return users

def main():
    """Main program"""
    print("=" * 60)
    print(" WELCOME TO THE STOCK TRADING SIMULATOR ")
    print("=" * 60)#for making it look similar to gui of app
    print(" Learn to trade with Rs.100,000 virtual money!")
    #first screen appearing after we run the code 
    print(" Practice your investing skills risk-free!")
    print("=" * 60)
    
    users = load_users()
    current_user = None
    
    while True:
        # If not logged in, show login menu
        if not current_user:
            print("\n" + "-" * 40)
            print("MAIN MENU")
            print("-" * 40)
            print("1.  Login")
            print("2.  Create Account")
            print("3.  Exit")
            print("-" * 40)
            
            choice = input("\nWhat would you like to do? ")
            
            if choice == '1':
                current_user = login_user(users)
            elif choice == '2':
                users = register_user(users)
            elif choice == '3':
                print("\nThanks for using the Stock Trading Simulator!")
                print(" Happy investing!")
                break
            else:
                print("\nInvalid choice. Please enter 1, 2, or 3.")
        
        # If logged in, show trading menu
        else:
            print("\n" + "-" * 40)
            print("TRADING MENU")
            print("-" * 40)
            print("1. View My Portfolio")
            print("2. Buy Stocks")#makin the code look like gui of app
            print("3. Sell Stocks")
            print("4. Logout")
            print("-" * 40)
            
            choice = input("\nWhat would you like to do? ")
            #different functionality of our code
            #after the user logins
            
            if choice == '1':
                view_portfolio(users, current_user)
            elif choice == '2':
                users = buy_stock(users, current_user)
            elif choice == '3':
                users = sell_stock(users, current_user)
            elif choice == '4':
                print(f"\n See you later, {current_user}!")
                print(" Keep building that portfolio!")
                current_user = None
            else:
                print("\n Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
