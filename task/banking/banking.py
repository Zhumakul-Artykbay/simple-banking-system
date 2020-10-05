import random
import sqlite3

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()
conn.commit()

dic = {}
ok = True

while ok:


    print("""
1. Create an account
2. Log into account
0. Exit
    """)
    case = int(input())

    if case == 1:
        randomlist = random.sample(range(0, 10), 9)
        card_number = "400000"
        
        check_list = randomlist.copy()

        for i in range(0, 9):
            if i % 2 == 0:
                check_list[i] *= 2
                if check_list[i] > 9:
                    check_list[i] -= 9

        check_sum = sum(check_list) + 8  
        last_digit = (10 - check_sum % 10) % 10

        string_list = [str(i) for i in randomlist]
        card_number += "".join(string_list) + str(last_digit)
        randomlist_PIN = random.sample(range(0, 10), 4)
        string_pin_list = [str(i) for i in randomlist_PIN]
        PIN = "".join(string_pin_list)
        print(f"""
Your card has been created
Your card number:
{card_number}
Your card PIN:
{PIN}
        """.format(card_number, PIN))
        dic[card_number] = PIN
        cur.execute(f'INSERT INTO card (number, pin) VALUES ({card_number}, {PIN})')
        conn.commit()
    elif case == 2:
        print("Enter your card number:")
        input_card_num = input()
        print("Enter your PIN:")
        input_PIN = input()

        if input_card_num in dic and dic[input_card_num] == input_PIN:

            print("You have successfully logged in!")
            balance = 0
            logged = True

            while logged:
                print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
                """)

                log_case = int(input())

                if log_case == 1:
                    print(f"Balance: {conn.execute('SELECT balance FROM card WHERE number = input_card_num')}")
                elif log_case == 2:
                    add_balance = int(input())
                    conn.execute(f'UPDATE card SET balance = balance + {add_balance} WHERE number = {input_card_num}')
                    conn.commit()
                    print("Income was added!")
                elif log_case == 3:
                    is_transfering = True
                    while is_transfering:
                        print("""
    Transfer
    Enter card number:""")

                        transfer_card_num = input()
                        ch_luhn_algorithm = []
                        ch_luhn_algorithm[:0] = transfer_card_num
                        ch_luhn_algorithm = [int(i) for i in ch_luhn_algorithm]

                        for i in range(0, len(ch_luhn_algorithm)):
                            if i % 2 == 0:
                                ch_luhn_algorithm[i] *= 2
                                if ch_luhn_algorithm[i] > 9:
                                    ch_luhn_algorithm[i] -= 9

                        if sum(ch_luhn_algorithm) % 10 == 0:
                            cur = conn.cursor()
                            cur.execute(f'SELECT number FROM card WHERE number = {transfer_card_num}')
                            if cur.fetchone():
                                if transfer_card_num != input_card_num:
                                    print("Enter how much money you want to transfer:")
                                    transfer_balance = int(input())
                                    if transfer_balance <= conn.execute(f"SELECT balance FROM card WHERE number = {input_card_num}").fetchone()[0]:
                                        conn.execute(f"UPDATE card SET balance = balance - {transfer_balance} WHERE number = {input_card_num}")
                                        conn.execute(
                                            f"UPDATE card SET balance = balance + {transfer_balance} WHERE number = {transfer_card_num}")
                                        conn.commit()
                                        print("Success!")
                                        is_transfering = False
                                    else:
                                        print("Not enough money!")
                                        is_transfering = False
                                else:
                                    print("You can't transfer money to the same account!")
                            else:
                                print("Such a card does not exist.")
                        else:
                            print("Probably you made a mistake in the card number. Please try again!")
                elif log_case == 4:
                    conn.execute(f'DELETE FROM card WHERE number = {input_card_num}')
                    conn.commit()
                    print("The account has been closed!")
                elif log_case == 5:
                    print("You have successfully logged out!")
                    logged = False
                elif log_case == 0:
                    logged = False
                    ok = False
        else:
            print("Wrong card number or PIN!")
    elif case == 0:
        ok = False

print("Bye!")
