import random
import sqlite3

#establish initial connection
random.seed()
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
            );""")

# After doing some changes in DB don't forget to commit them!
conn.commit()
conn.close()


class Bank:
    def __init__(self):
        self.data = {}  # empty dictionary
        self.acc_num = None
        self.iin = 400000  # default Issue Identification Number(IIN)
        self.card_number = None
        self.pin = None
        self.control_digit = None
        self.balance = 0
        self.logged_userID = None


    def establish_connection(self):  # not working yet
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()


    def main_menu(self):
        user_input = input("""
1. Create an account
2. Log into account
0. Exit
""")
        if user_input == "1":
            return self.new_acc()
        elif user_input == "2":
            return self.log_in()  # remove return words
        elif user_input == "0":
            print("Bye!")
            return exit()
        else:
            print("incorrect parameters provided, switching back to the main menu")
            return self.main_menu()


    def new_acc(self):
        new_account = self.gen_acc_number()
        if self.acc_num not in self.data:
            self.data['card number'] = self.gen_cc()
            self.data['acc_number'] = new_account
            self.data['pin'] = self.gen_pin()
            self.data['balance'] = self.balance


            conn = sqlite3.connect('card.s3db')
            cur = conn.cursor()
            cur.execute("INSERT INTO card('number', 'pin') VALUES (?, ?)", (self.card_number, self.pin))
            conn.commit()
            conn.close()


            # self.data[self.acc_number] = {'card number': self.card_number,'pin': self.pin, 'balance': self.balance} #if an error - replace self.balance with "0"
            print(f'''
Your card has been created
Your card number:
{int(self.card_number)}
Your card PIN:
{self.pin}''')
            return self.main_menu()
        else:
            return self.new_acc()


    def log_in(self):
        login = str(input('\nEnter your card number:\n'))
        password = str(input('Enter your PIN:\n'))

        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()

        self.establish_connection()  # connecting to an SQL DB
        # working check method if returned value (login + password exist in a DB)
        if cur.execute("SELECT * FROM card WHERE number == ? and pin == ?",(login, password)).fetchone():  # fetchone() method returns one selected value. so this function cheching if such value exists
            self.logged_userID = login
            return self.log_in_success()
        else:
            return self.log_in_failure()


    def gen_acc_number(self):  # test this separately
        self.acc_num = random.randint(100_000_000, 999_999_999)
        return self.acc_num


    def luhn_algorithm_check(self, cc_number):
        if cc_number[-1] == "0":
            return False  # control digit cannot be 0
        else:
            # proceed with calculations:
            cc_number = [int(x) for x in cc_number]
            without_controlD = cc_number[0:15]
            for x in range(0, len(without_controlD), 2):
                without_controlD[x] *= 2
            for x in range(len(without_controlD)):
                if without_controlD[x] > 9:
                    without_controlD[x] -= 9
            digits_sum = sum(without_controlD)
            #  obtaning control digit and check if it mathes provided one.
            control_digit = int(10 - (digits_sum % 10))
            if control_digit == cc_number[15]: # numerating starts with 0, so checking if control digit provided mathes the generated
                return True
            else:
                return False
        return None


    def get_control_digit(self):
        #first 15 means that we currently don't have a control digit for our CC
        first_15 = list(str(self.iin) + str(self.acc_num))
        first_15 = [int(x) for x in first_15]
        #calculating
        #for x in range(len(first_15)):
        #    first_15[x] = int(first_15[x])
        for x in range(0, len(first_15), 2):
            first_15[x] *= 2
        for x in range(len(first_15)):
            if first_15[x] > 9:
                first_15[x] -= 9
        digits_sum = sum(first_15)
        if digits_sum % 10 == 0:
            # INVALID ACCOUNT # and should be re-generated again
            return Bank.new_acc(self)
        else:
            self.control_digit = int(10 - (digits_sum % 10))
            return self.control_digit


    def gen_cc(self):
        self.get_control_digit()
        self.card_number = str(self.iin) + str(self.acc_num) + str(self.control_digit)
        return self.card_number


    def gen_pin(self):
        self.pin = random.randint(0, 9999)  # or change from 1000
        self.pin = str(f'{self.pin:0>4d}')
        return self.pin


    def log_in_success(self):
        print('You have successfully logged in!\n')
        return self.user_menu()


    def log_in_failure(self):
        print('Wrong card number or PIN!\n')
        return self.main_menu()


    def add_income(self):  # there was a bug here, as function used to add the money to all existing cards, something was wrong with filter
        self.balance += int(input("Enter income:\n"))
        print('Income was added!')
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute('''UPDATE card
                    SET
                        balance = ?
                    WHERE
                        number == ?''',
                        #(self.balance, self.card_number))
                        (self.balance, self.logged_userID))

        conn.commit()
        conn.close()

        return self.user_menu()


    def do_transfer(self):
        # will check in two ways 1) luhn algorithm 2) if CC num id DB
        card_number = input("Enter card number:\n")
        # First of all checking if card number can exist based on Luhn algorithm.
        if Bank.luhn_algorithm_check(self, card_number):
            #print("ALHORITHM PASSED")
            conn = sqlite3.connect('card.s3db')  # connecting to a DB
            cur = conn.cursor()  # connecting to a DB
            # If card exists in our DB, proceed with transfer
            # very important room for bug in the next line is missing "," after 1st varialbe in brackets!
            if cur.execute("SELECT * FROM card WHERE number == ?",(card_number,)).fetchone():  # fetchone() method returns one selected value. so this function checking if such value exists:
                transfer_amount = int(input("Enter how much money you want to transfer:\n"))
                if transfer_amount <= self.balance:
                    # Decreasing balance of current user:
                    cur.execute('''UPDATE card
                                SET
                                    balance = balance - ?
                                WHERE
                                    number == ?''',
                                                    (transfer_amount, self.logged_userID))

                    conn.commit()  # commit changes
                    conn.close()

                    conn = sqlite3.connect('card.s3db')  # connecting to a DB
                    cur = conn.cursor()  # connecting to a DB
                    cur.execute('''UPDATE card
                                SET
                                    balance = balance + ?
                                WHERE
                                    number == ?''',
                                                    (transfer_amount, card_number))
                    conn.commit()  # commit changes
                    conn.close()
                    print("Success!")
                    return self.user_menu()
                else:
                    print("Not enough money!")
                    return self.user_menu()
            else:
                print("Such a card does not exist.")
                return self.user_menu()
        # If card doest not exist in our DB, print an error and return user_menu
        else:
            print('Probably you made mistake in card number. Please try again!')
            return self.user_menu()


    def close_account(self):
        conn = sqlite3.connect('card.s3db')  # connecting to a DB
        cur = conn.cursor()  # connecting to a DB
        cur.execute("DELETE FROM card WHERE number = ?",(self.logged_userID,))
        conn.commit()
        print("The account has been closed!")
        return self.main_menu()

    def user_menu(self):
        action = input('''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
''')
        if action == '1':
            print(f'Balance: {self.balance}\n')
            return self.user_menu()  # можно так же перенести в другое место
        elif action == '2':
            return self.add_income()
        elif action == '3':
            return self.do_transfer()
        elif action == '4':
            return self.close_account()
        elif action == '5':
            print('You have successfully logged out!\n')
            return self.main_menu()
        elif action == '0':
            conn.close()
            print("Bye!")
            return exit()


username = Bank()
username.main_menu()
