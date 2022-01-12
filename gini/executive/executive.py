# global variables
accounts = {}
ledger = {}
accountIndex = 1

# menu functions
def mainMenu():
    menuStr = 'Please select an option:\n1. Register\n2. Login\n3. Exit\n: '
    try:
        return int(input(menuStr))
    except ValueError:
        # input was not an integer; force invalid input
        return -1

def userMenu():
    menuStr = 'Please select an option:\n1. Check Balance\n2. Deposit Funds\n3. Withdraw Funds\n4. Transfer Funds\n5. Last 5 transactions\n6. Logout\n: '
    try:
        return int(input(menuStr))
    except ValueError:
        # input was not an integer; force invalid input
        return -1

# user functions
def registerUser():
    # globals
    global accounts, ledger, accountIndex
    # get the user details
    # =========================================================================
    name = input('Please enter your full name: ')
    # validate name
    while len(name) < 5:
        print('Your name must be at least 5 characters long!')
        name = input('Please enter your full name: ')
    age = input('Please enter your age in years: ')
    # validate age
    while (not age.isnumeric()) or (int(age) < 18) or (int(age) > 140):
        print('Your age must be a number between 18 and 140')
        age = input('Please enter your age in years: ')
    nationalID = input('Please enter your social security number: ')
    # validate national ID
    while len(nationalID) != 12 or (not nationalID.isnumeric()):
        print('Your social security must be a number 12 digits long')
        nationalID = input('Please enter your social security number: ')
    balance = input('Please enter your initial account balance: ')
    # validate balance
    while (not balance.isnumeric()) or (int(balance) < 500) or (int(balance) > 99999999):
        print('Your balance must be a number between 500 and 99,999,999')
        balance = input('Please enter your initial account balance: ')
    passwd = input('Please enter a password for your account: ')
    # validate password
    while len(passwd) < 5:
        print('Your password must be at least 5 characters long!')
        passwd = input('Please enter a password for your account: ')
    accNo = f'BOK-0{accountIndex}'
    # ==========================================================================
    # save record to accounts dictionary
    accounts[accNo] = [name, int(age), nationalID, int(balance), passwd]
    # save deposit transaction to ledger dictionary
    ledger[accNo] = []
    ledger[accNo].append(('Deposit', balance, 'Opening balance'))
    print(f'Registered successfully. Your account number is {accNo}')
    # increment
    accountIndex += 1

def loginUser():
    # globals
    global accounts
    # ask for credentials and login
    accNo = input('Please enter your account number: ')
    passwd = input('Please enter your password: ')
    # check whether key exists
    if accNo not in accounts:
        print('Invalid account number')
        return (False, 0)
    else:
        if accounts[accNo][4] != passwd:
            print('Invalid password')
            return (False, 0)
        else:
            print('Successfully logged in!')
            return (True, accNo)
        
# account functions
def checkBalance(accNo):
    # globals
    global accounts
    # check balance
    print(f'Your balance is {accounts[accNo][3]} SEK')
    
def depositFunds(accNo):
    # globals
    global accounts, ledger
    # make a deposit
    amount = input('Please enter an amount to deposit: ')
    # validate amount
    while (not amount.isnumeric()) or (int(amount) < 500) or (int(amount) > 999999):
        print('Your deposit amount must be a number between 500 and 999,999')
        amount = input('Please enter an amount to deposit: ')
    # can be safely converted to int
    amount = int(amount)
    # save to accounts
    accounts[accNo][3] += amount
    # save to ledger
    ledger[accNo].append(('Deposit', amount, 'User deposit'))
    print(f'You successfully deposited {amount} SEK')
        
def withdrawFunds(accNo):
    # globals
    global accounts, ledger
    # make a withdrawal
    amount = input('Please enter an amount to withdraw: ')
    # validate amount
    while (not amount.isnumeric()) or (int(amount) < 500) or (int(amount) > 999999):
        print('Your withdrawal amount must be a number between 500 and 999,999')
        amount = input('Please enter an amount to withdraw: ')
    # can be safely converted to int
    amount = int(amount)
    if amount > accounts[accNo][3]:
        print(f'Insufficient funds to withdraw {amount} SEK, your balance is {accounts[accNo][3]} SEK')
    else:
        # save to accounts
        accounts[accNo][3] -= amount
        # save to ledger
        ledger[accNo].append(('Withdrawal', amount, 'User withdrawal'))
        print(f'You successfully withdrew {amount} SEK') 
        
def transferFunds(accNo):
    # globals
    global accounts, ledger
    # make a transfer
    amount = input('Please enter an amount to transfer: ')
    # validate amount
    while (not amount.isnumeric()) or (int(amount) < 500) or (int(amount) > 999999):
        print('Your transfer amount must be a number between 500 and 999,999')
        amount = input('Please enter an amount to transfer: ')
    # can be safely converted to int
    amount = int(amount)
    if amount > accounts[accNo][3]:
        print(f'Insufficient funds to transfer {amount} SEK, your balance is {accounts[accNo][3]} SEK')
    else:
        # ask for recipient
        rx = input('Please enter the recipient account number: ')
        if rx not in accounts:
            print('Invalid account number')
        else:
            # save to accounts
            accounts[accNo][3] -= amount
            accounts[rx][3] += amount
            # save to ledger
            ledger[accNo].append(('Transfer', amount, f'User transfer to {rx}'))
            ledger[rx].append(('Received', amount, f'{accNo} transfer to user'))
            print(f'You successfully transferred {amount} SEK to {rx}') 
    
def lastTransactions(accNo, cutOff):
    # globals
    global accounts, ledger
    # show last cutOff transactions
    cutOff *= -1
    for t in ledger[accNo][cutOff:]:
        # display the transaction
        print(f'{t[0]} of {t[1]} SEK. {t[2]}')
                
def userLoop(accNo):
    # globals
    global accounts, ledger
    # user while loop
    uchoice = userMenu()
    while uchoice != 6:
        # process selection
        if uchoice == 1:
            checkBalance(accNo)
        elif uchoice == 2:
            depositFunds(accNo)
        elif uchoice == 3:
            withdrawFunds(accNo)
        elif uchoice == 4:
            transferFunds(accNo)
        elif uchoice == 5:
            lastTransactions(accNo, 5)
        else:
            # invalid entry
            print('Invalid option')
        # get the next selection
        uchoice = userMenu()
    print(f'Goodbye {accounts[accNo][0]}')

def mainLoop():
    # main while loop
    choice = mainMenu()
    while choice != 3:
        # process choice
        if choice == 1:
            # register a new user
            registerUser()
        elif choice == 2:
            # login
            result = loginUser()
            if result[0] == True:
                # main user loop
                userLoop(result[1])   
        else:
            # invalid entry
            print('Invalid option')
        # get the next choice
        choice = mainMenu()
    print('Virtual Bank is now closed.')