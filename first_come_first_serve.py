from tabulate import tabulate


def FCFS():
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

    process_num = len(b_list)
    timing_point = [0]

    for i in range(process_num):
        timing = 0
        for j in range(i + 1):
            timing += b_list[j]
        timing_point.append(timing)

    # print(timing_point)

    result_str = "  | "
    for i in range(process_num):
        result_str += "P" + str(i + 1) + "\t| "

    timing_str = "  0"
    for i in range(process_num):
        timing_str += "\t\t" + str(timing_point[i + 1])

    print()
    print(result_str)
    print(timing_str)
    print()
    ave_wait_time = 0
    for i in range(process_num):
        ave_wait_time += timing_point[i]
    ave_wait_time /= process_num
    print("Average Waiting Time: " + str(ave_wait_time))
