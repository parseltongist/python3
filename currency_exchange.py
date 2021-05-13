import json
import requests

class Kantor:

    usd = requests.get('http://www.floatrates.com/daily/usd.json')
    eur = requests.get('http://www.floatrates.com/daily/eur.json')
    usd_python = json.loads(usd.content)
    eur_python = json.loads(eur.content)


    def __init__(self, curr_for_sale, curr_to_buy, sell_amount):
        self.curr_for_sale = curr_for_sale
        self.curr_to_buy = curr_to_buy
        self.sell_amount = sell_amount

    def create_cache(self):


    def beginning(self):
        print("Checking the cache...")
        if str(self.curr_to_buy) == "usd":
            print("Oh! It is in the cache!")
            usd_rate = self.usd_python[f"{self.curr_for_sale}"]["rate"]
            print(f"You received {(self.sell_amount / usd_rate):.2f} {self.curr_to_buy.upper()}.")
            return self.next_deal()

        elif str(self.curr_to_buy) == "eur":
            print("Oh! It is in the cache!")
            eur_rate = self.eur_python[f"{self.curr_for_sale}"]["rate"]
            print(f"You received {(self.sell_amount / eur_rate):.2f} {self.curr_to_buy.upper()}.")
            return self.next_deal()

        else:
            print("Sorry, but it is not in the cache!")
            r = requests.get(f'http://www.floatrates.com/daily/{self.curr_for_sale}.json')
            r_cache = json.loads(r.content)
            ex_rate = json_to_python[f"{self.curr_to_buy.lower()}"]["rate"]
            print(f"You received {(self.sell_amount * ex_rate):.2f} {self.curr_to_buy.upper()}.")
            return self.next_deal()
            #print("exchange rate for {}:", json_to_python[f"{self.curr_to_buy}"]["rate"])

    def next_deal(self):
        while True:
            self.curr_to_buy = str(input().lower())
            if self.curr_to_buy == "":
                break
            else:
                self.sell_amount = float(input())
                return self.beginning()

deal1 = Kantor(str(input().lower()),str(input().lower()), float(input()))
Kantor.beginning(deal1)
