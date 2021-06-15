import random
import sqlite3


random.seed()
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# Executes some SQL query
# cur.execute("DROP DATABASE IF EXISTS card")

# cur.execute("CREATE DATABASE IF NOT EXISTS card")
# conn.commit()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, 'number' TEXT, 'pin' TEXT, 'balance' INTEGER DEFAULT 0);")

# After doing some changes in DB don't forget to commit them!
conn.commit()


class Bank:
    def __init__(self):
        self.data = {}  # empty dictionary
        self.acc_num = None
        self.iin = 400000  # default Issue Identification Number(IIN)
        self.card_number = None
        self.pin = None
        self.control_digit = None
        self.balance = 0

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
            cur.execute("INSERT INTO card('number', 'pin') VALUES (?, ?)",(self.card_number, self.pin))
            conn.commit()
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
        login = str(input('Enter your card number:\n'))
        password = str(input('Enter your PIN:\n'))
        if self.data['card number'] == login and self.data['pin'] == password:
            return self.log_in_success()
        else:
            return self.log_in_failure()


    def gen_acc_number(self):  # test this separately
        self.acc_num = random.randint(100_000_000, 999_999_999)
        return self.acc_num

    def get_control_digit(self):
            first_15 = []
            # прогнать #first 15 через все шаги и затем присвоить уже контрольную цифру? умножить нечетные позиции на 2 ы
            for x in str(self.iin):
                first_15.append(int(x))
            for x in str(self.acc_num):
                first_15.append(int(x))
            for x in range(len(first_15)):
                first_15[x] = int(first_15[x])
            for x in range(0, len(first_15), 2):
                first_15[x] *= 2
            for x in range(len(first_15)):
                if first_15[x] > 9:
                    first_15[x] -= 9
            digits_sum = sum(first_15)
            self.control_digit = int(10 - (digits_sum % 10))
            if self.control_digit < 10:
                return self.control_digit
            else:
                return Bank.gen_acc_number(self)  # possible merge with the CC generator


    def gen_cc(self):
        self.get_control_digit()
        self.card_number = str(self.iin) + str(self.acc_num) + str(self.control_digit)
        return self.card_number


    def gen_pin(self):
        self.pin = random.randint(1000, 9999)
        self.pin = str(self.pin)
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
        cur.execute("UPDATE card SET balance  = ? WHERE 'number' == ?"(self.balance, self.card_number))
        conn.commit()


    def do_transfer(self):
        ...
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
            conn.close()
            return self.user_menu()  # можно так же перенести в другое место
        elif action == '2':
            return self.add_income()
        elif action == '3':
            return self.do_transfer()
        elif action == '4':
            return self.close_account()
        elif action == '5':
            print('You have successfully logged out!\n')
            conn.close()
            return self.main_menu()
        elif action == '0':
            conn.close()
            print("Bye!")
            return exit()


username = Bank()
username.main_menu()
