card_num = 4000008449433403
card_num1 = '4000003305160035'
card_num2 = '4000009455296122'

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




print(luhn_check(card_num))
