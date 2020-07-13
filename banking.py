import random

import sqlite3
conn = sqlite3.connect('banking/card.s3db')
cur = conn.cursor()
# cur.execute('''create table card (
#                       id integer,
#                       number text,
#                       pin text,
#                       balance INTEGER DEFAULT 0)''')
def menu():
    print("""1. Create an account
2. Log into account
0. Exit""")

def luhn_check(card_num):
    # drop the last symbol and save it as variable "last_sym".
    last_sym = str(card_num)[-1]
    card_num = str(card_num)[0:-1]

    # multiply odd digits by 2 and subtract 9 if digit more them 9.
    n = 1
    num_list = []
    for i in card_num:
        # odd check
        if n % 2 == 1:
            i = (int(i)*2)
            #subtract 9 if digit more them 9.
            if i > 9:
                num_list.append(i - 9)
            else:
                num_list.append(i)
        else:
             num_list.append(int(i))
        n += 1

    # check sum and return result
    if (sum(num_list) + int(last_sym)) % 10 == 0:
        return True
    else:
        return False


def create_an_a_card_num():
    card_num = str(400000000000000 + random.randint(100000000, 999999999))
    n = 1
    card_sum = int()
    card_list = []
    for i in card_num:
        i = int(i)
        if n == 16:
            print(i)
            break
        if n % 2 != 0:
            i *= 2
        if i > 9:
            i -= 9
        n += 1
        card_list.append(i)
        card_sum += (i)
    if card_sum % 10 == 0:
        card_num = str(card_num) +str(0)
    else:
        card_num = str(card_num) + str(10 - card_sum % 10)
    return card_num

def create_an_account():
    card_num = create_an_a_card_num()
    while card_num in cur.execute(f'''select number from card'''):
        card_num = create_an_a_card_num()
    pin = random.randint(1000, 9999)
    balance = 0
    id = random.randint(1, 999999999)
    cur.execute(f'''insert into card values 
                    ({int(id)}, {str(card_num)}, {int(pin)}, {str(balance)})''')
    conn.commit()

    print(f"""Your card has been created
Your card number:{card_num}
Your card PIN:
{pin}
""")

def log_into_account():
    print("Enter your card number:")
    card_num = str(input())
    print("Enter your PIN:")
    pin = (input())
    db_card_num = str(cur.execute('''select number from card''').fetchall())
    db_pin = (str(cur.execute(f"select pin from card where number = {card_num}").fetchall())[3:-4])
    if str(f"('{card_num}',)") in db_card_num:
        if db_pin == pin:
            print("You have successfully logged in!")
            button1 = 1
            while button1 not in (0,4,5):
                print('''1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit''')
                button1 = int(input())

                if button1 == 1:
                    print(f''' Balance: { str(cur.execute ( "select balance from card where number = '{}'".format(card_num) 
                                     ).fetchall())[2:-3]
                     } 
        ''')

                elif button1 == 2:
                    print("Enter income:")
                    income = int(input())
                    cur.execute(f"update card set balance = balance + {income} where number = '{card_num}' ")
                    conn.commit()
                    print("Income was added!")

                elif button1 == 3:
                    print("Transfer\nEnter card number:")
                    trans_card = str(input())

                    if card_num == trans_card:
                        print("You can't transfer money to the same account!")
                    elif str(cur.execute(f'select number from card where number = "{trans_card}"').fetchall())[0:-5] == str(f"[('{trans_card}")[0:-1]:
                        if str(cur.execute(f'select number from card where number = "{trans_card}"').fetchall())[0:-4] == str(f"[('{trans_card}"):
                            print('Enter how much money you want to transfer:')
                            trans_money = input()
                            if float(str(cur.execute(f'select balance from card where number = "{card_num}"').fetchall())[2:-3]) >= float(trans_money):
                                cur.execute(f"update card set balance = balance - {trans_money} where number ='{card_num}'")
                                cur.execute(f"update card set balance = balance + {trans_money} where number ='{trans_card}'")
                                conn.commit()
                                print('Success!')
                            else:
                                print('Not enough money!')
                        else:
                            print("Such a card does not exist.")
                    else:
                        if luhn_check(trans_card):
                            print("Such a card does not exist.")
                        else:
                            print("Probably you made mistake in the card number. Please try again!")



                elif button1 == 4:
                    cur.execute(f"delete from card where number = '{card_num}'")
                    conn.commit()
                    print('The account has been closed!')
                elif button1 == 5:
                    print("You have successfully logged out!")
                    return button1
                elif button1 == 0:
                    print("Bye")
                    return button1

        else:
            print("Wrong card number or PIN!")
    else:
            print("Wrong card number or PIN!")


button = int(1)

while button != 0:
    menu()
    button = int(input())
    if button == 1:
        create_an_account()
    elif button == 0:
        print("Bye")
    elif button == 2:
        if log_into_account() == 0:
            break
        else:
            continue
