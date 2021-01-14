# final credit calculator with annuity and differentiated payments
# python3 --type=annuity --principal=30000 --periods=-14 --interest=10

import argparse
import math

### FUNCTIONS
def diff_payment_calculation(principal, periods, i):
    i = float(interest / (12 * 100))
    return principal / periods + i * (principal - (principal * (m - 1) / periods))
def periods_calculation(principal, monthly_payment, interest):
    i = float(interest / (12 * 100))
    return math.ceil(math.log((monthly_payment / (monthly_payment - i * principal)), 1 + i))
def annuity_calculation(principal, periods, interest):
    i = float(interest / (12 * 100))
    return principal * (i * pow((i + 1), periods)) / (pow((i + 1), periods) - 1)
def principal_calculation(payment, interest, periods):
    i = float(interest / (12 * 100))
    return payment / ((i * pow((1 + i), periods)) / (pow((1 + i), periods) - 1))
def annuity_overpayment_value(n, payment, principal):
    i = float(interest / (12 * 100))
    return int(n * payment - principal)

#   Error functions:

def error_message_and_exit():
    print("Incorrect parameters")
    exit()

parser = argparse.ArgumentParser(usage='', description = 'This god damn calculator will calculate whatever option you need.')


parser.add_argument("--type", type=str, help="Payment type can be either 'annuity' or 'diff'. if no type choosen the program will not work", choices=["annuity", "diff"])
parser.add_argument("--payment", type=int, help="If --type=diff, their combination is invalid")
parser.add_argument("--principal", type=int, help="Valid with every combination")
parser.add_argument("--periods", type=int, help="Denotes the number of months and/or years  needed to repay the credit")
parser.add_argument("--interest", type=float, help="Must always be specified.") # the first short name or an argument (must be a single dash (-)) , the second one is full

args = parser.parse_args()

type = args.type
payment = args.payment
principal = args.principal
periods = args.periods
interest = args.interest



variables = [args.type, args.payment, args.principal, args.periods, args.interest]

#   Errors block:
# payment type should be either 'annuity' or 'diff'
if type is None:
    error_message_and_exit()
elif type =='annuity' or 'diff':
    pass
else:
    error_message_and_exit()

#  if any value is negarive - error and exit

if principal is not None and int(principal) < 0:
    error_message_and_exit()
elif periods is  not None and int(periods) < 0:
    error_message_and_exit()
elif interest is not None and int(interest) < 0:
    error_message_and_exit()
elif payment is not None and int(payment) < 0:
    error_message_and_exit()
else:
    pass


if len(variables) > 5 or len(variables) < 3:    # why not 4 and 3?
    error_message_and_exit()
elif type =='diff' and payment is not None:
    error_message_and_exit()
elif interest is None:
    error_message_and_exit()


if type == 'annuity':
    if periods is None: # periods parameter missing, calculating it here
        n = periods_calculation(principal, payment, interest)
        if n < 12:
            print('It will take {} months to repay this loan!'.format(n))
        elif n % 12 == 0:
            if n == 12:
                print('It will take 1 year to repay this loan!')
            else:
                print('It will take {} years to repay this loan!'.format(math.ceil(n / 12)))
                print(f'Overpayment = {annuity_overpayment_value(n, payment, principal)}')
        elif int(n) > 12:
            y = int(n / 12)
            m = round(int(n % 12))
            print('It will take {} years and {}'' months' if m != 1 else ' month','to repay this loan!'.format(y, m))

    elif payment is None: # annuity parameter missing, calculating it here
        a = annuity_calculation(principal, periods, interest)
        print("Your monthly payment = {}!".format(math.ceil(a)))    # here we can add code if the last payment is not equal to the regular

    elif principal is None: # # principal parameter missing, calculating it here
        p = principal_calculation(payment, interest, periods)
        print(f'Your loan principal = {p}!')

elif type == 'diff':
    # for type=diff we can't calculate periods of loan principal as each payment is different
    total = 0 # Very important to declare this variable outside the loop
    if payment is None: # annuity parameter missing, calculating it here
        for m in range (1, periods + 1):
            a = diff_payment_calculation(principal, periods, interest)
            total += math.ceil(a)
            print(f'Month {m}: payment is {(math.ceil(a))}!')

        print(f'\n Overpayment = {int(total - principal)}')

else:
    error_message_and_exit()
