def RR():
    burst_str = input("Enter Burst Times separate with SPACE :\n")

    try:
        b_str = burst_str.split(" ")
        b_list = []
        for b_ele in b_str:
            b_list.append(int(b_ele))
        # print(b_list)
    except ValueError:
        print("WRONG FORM OF INPUT!!!")
        exit(1)