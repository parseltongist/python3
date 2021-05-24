import random

class Bill_splitter():

    def __init__(self):
        self.lucky_mode = None
        self.invited_people_num = None
        self.names_list = None
        self.guest_list = None
        self.bill_amount = None
        self.lucky_guest = None


    def bill_split(self, bill, guests_quantity, guestlist):
        if self.lucky_mode is True:
            payment_per_guest = round((bill / (guests_quantity - 1)), 2)
            for guest in guestlist:
                guestlist[guest] = payment_per_guest
            guestlist[self.lucky_guest] = 0
        else:
            payment_per_guest = round(bill / guests_quantity , 2)
            for guest in guestlist:
                guestlist[guest] = payment_per_guest


    def lucky_guest_feature(self, guestlist):
        lucky_feature = input("Do you want to use the \"Who is lucky?\" feature? Write Yes/No:")
        if lucky_feature.lower() == "yes":
            self.lucky_mode = True
            self.lucky_guest = random.choice(guestlist)
            print()
            print(f"{self.lucky_guest} is the lucky one!")
            return self.lucky_guest
        else:
            self.lucky_mode = False
            print()
            print("No one is going to be lucky")

    def main_logic(self):
        self.invited_people_num = int(input("Enter the number of friends joining (including you):"))
        print()
        if self.invited_people_num <= 0:
            print("No one is joining for the party")
        else:
            print("Enter the number of friends joining (including you):")
            self.names_list = [input() for name in range(self.invited_people_num)]
            self.guest_list = dict.fromkeys(self.names_list, 0)
            print()
            self.bill_amount = float(input("Enter the total bill value:"))
            print()
            self.lucky_guest = self.lucky_guest_feature(self.names_list)
            print()
            self.bill_split(self.bill_amount, self.invited_people_num, self.guest_list)
            print(self.guest_list)

party = Bill_splitter()
Bill_splitter.main_logic(party)
