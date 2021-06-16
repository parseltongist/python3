import random
import sqlite3

#establish initial connection
random.seed()
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


# Executes some SQL query
# cur.execute("DROP DATABASE IF EXISTS card")

# cur.execute("CREATE DATABASE IF NOT EXISTS card")
# conn.commit()
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
            return self.log_in_success()
        else:
            return self.log_in_failure()


    def gen_acc_number(self):  # test this separately
        self.acc_num = random.randint(100_000_000, 999_999_999)
        return self.acc_num


    def luhn_algorithm_check(self, cc_number):
        for x in range(len(cc_number)):
            cc_number[x] = int(cc_number[x])
        for x in range(0, len(cc_number), 2):
            cc_number[x] *= 2
        for x in range(len(first_15)):
            if cc_number[x] > 9:
                cc_number[x] -= 9
        digits_sum = sum(cc_number)
        if digits_sum % 10 == 0:
            return False
        else:
            control_digit = int(10 - (digits_sum % 10))
            if control_digit == cc_number[15]:
                return True
            else:
                return False
        return None

    def get_control_digit(self):
            # прогнать #first 15 через все шаги и затем присвоить уже контрольную цифру? умножить нечетные позиции на 2 ы
            #adding
        first_15 = list(str(self.iin) + str(self.acc_num))
        first_15 = [int(x) for x in first_15]
        #calculating
        for x in range(len(first_15)):
            first_15[x] = int(first_15[x])
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


    def add_income(self):
        self.balance += int(input("Enter income:\n"))
        print('Income was added!')
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute('''UPDATE card
                    SET
                        balance = ?
                    WHERE
                        number == ?''',
                        (self.balance, self.card_number))
        conn.commit()
        conn.close()

        return self.user_menu()

    def do_transfer(self):
        # will check in two ways 1) luhn algorithm 2) if CC num id DB
        card_number = input("Enter card number:\n")
        if luhn_algorithm_check(card_number):
            #if card in DB:
            #transfer_amount = input("Enter how much money you want to transfer:")
            # check if user has this money, if not print("Not enough money!") return self.user_menu() or print("Success!") return self.user_menu()
            #else:
            # print("Such a card does not exist.")
            #return self.user_menu()
            print("algorithm is working. - UPDATE DB")
        else:
            print('Probably you made mistake in card number. Please try again!')
            return self.user_menu()


    def close_account(self):
        cur.execute("DELETE FROM card WHERE 'number' = ?",(self.card_number))
        conn.commit()
        print("The account has been closed!")

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
