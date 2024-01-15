
from datetime import date, datetime


def suffix(day):
    suffix = ""
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return suffix

def validateday(day):
    today = date.today()

    # dd/mm/YY
    #d1 = today.strftime("%d/%m/%Y")
    #print("d1 =", d1)

    # Textual month, day and year	
    d2 = today.strftime("%B %d, %Y")
    #print("d2 =", d2)

    # mm/dd/y
    d3 = today.strftime("%m/%d/%y")
    #print("d3 =", d3)

    # Month abbreviation, day and year	
    d4 = today.strftime("%b-%d-%Y")
    #print("d4 =", d4)

    # mm dd yyyyy
    d5 = today.strftime("%d %b %Y")
    #print("d5 =", d5)

    # mm dd yyyyy
    d6 = today.strftime("%b %d %Y")
    #print("d6 =", d6)

    # mm/dd/y
    d7 = today.strftime("%m/%d/%y").replace('0', '')
    #print("d7 =", d7)

    # mm/dd/y
    d8 = today.strftime("%m.%d.%y")
    #print("d8 =", d8)

    #   March 11 | 2021
    d9 = today.strftime("%B %d | %Y")
    #print("d9 =", d9)

    # 03.8.21
    d10 = today.strftime("%m.%-d.%y")
    #print("d10 =", d10)

    # March 9th, 2021
    d11 = today.strftime("%B %-d" + suffix(datetime.now().day) +  ", %Y")
    #print("d11 =", d11)

    # mm dd yyyyy
    d12 = today.strftime("%d %b / %y")
    #print("d12 =", d12)

    # mm dd, yyyyy
    d13 = today.strftime("%b %-d, %Y")
    #print("d13 =", d13)

    # yyyyy.mm.dd
    d14 = today.strftime("%Y.%m.%d")
    #print("d14 =", d14)

    # mm dd, yyyyy
    d15 = today.strftime("%b %d, %Y")
    #print("d15 =", d15)

    # mm-dd-yyyyy
    d16 = today.strftime("%m-%d-%Y")
    #print("d16 =", d16)


    if(d2 in day or d3 in day or d4 in day or d5 in day or d6 in day or d7 in day or d8 in day or d9 in day or d10 in day or d11 in day or d12 in day or d13 in day or d14 in day or d15 in day or d16 in day):
        return True, str(date.today().strftime("%Y-%m-%d"))

    return False, str(date.today().strftime("%Y-%m-%d"))

#d2 = March 10, 2021
#d3 = 03/10/21
#d4 = Mar-10-2021
#d5 = 10 Mar 2021
#d6 = Mar 10 2021
#d7 = 3/5/21  
#d8 = 03.10.21
#d9 = March 11 | 2021
#d10 = 03.8.21 
#d11 = March 9th, 2021| 
#d12 = 10 Mar / 21
#d13 = Mar 3, 2023
#d14 = 2023.11.03
#d15 = Mar 03, 2023
#d16 = 12-27-2023


#def main():
#    print("Entra")
#    print(validateday('April 2nd, 2021|'))
#
#if __name__ == "__main__":
#    main()