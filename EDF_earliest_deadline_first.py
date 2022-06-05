from tabulate import tabulate
from math import gcd
from CyclicProcess import CyclicProcess
from queue import PriorityQueue


def EDF():
    num_of_processes = int(input("Enter Number of Processes: "))
    p_info = []
    for i in range(num_of_processes):
        a, b, c = [int(x) for x in input(f"Enter (c, p, d) with Space Separated For Process {i + 1}: ").split(' ')]
        p_info.append([a, b, c])
    # print(p_info)
    # print(lcm(p_info))

    major_cycle = lcm(p_info)

    process_list = []

    max = 99999999

    # create Process instances and save it into a list
    i = 0
    for element in p_info:
        process_list.append(CyclicProcess(c=element[0], p=element[1], d=element[2], process_id=i))
        i += 1

    schedule = PriorityQueue(num_of_processes)

    for element in process_list:
        schedule.put((element.next_deadline, 0, element.process_id, element))

    final_table = []
    for time in range(major_cycle):
        frame = [time]
        for element in process_list:
            if time == element.next_deadline:
                # every new period update remaining comp time, and rejoin the queue
                element.remaining_c = element.c
                element.next_deadline = (int(time / element.d) + 1) * element.d
                if previous_process_id != element.process_id:
                    schedule.put((element.next_deadline, 1, element.process_id, element))
                else:
                    schedule.put((element.next_deadline, 0, element.process_id, element))
            element.next_deadline = (int(time / element.d) + 1) * element.d
            frame.append(element.next_deadline)

        for element in process_list:
            frame.append(element.remaining_c)

        current_process = schedule.get()[3]
        if time == 0:
            previous_process_id = 0
        else:
            final_table_size = len(final_table)
            frame_size = len(final_table[final_table_size - 1])
            # recorded on the last entry
            previous_process_id = final_table[final_table_size - 1][frame_size - 1]

        frame.append(current_process.process_id)

        current_process.remaining_c -= 1

        if current_process.remaining_c == 0:
            pass
        else:
            schedule.put((current_process.next_deadline, 0, current_process.process_id, current_process))

        final_table.append(frame)

    # print(final_table)

    for element in final_table:
        element[len(element) - 1] = str("P" + str(element[len(element) - 1] + 1))

    # print(final_table)

    headers = ["Time"]
    for i in range(num_of_processes):
        headers.append(f"P{i + 1} next d")
    for i in range(num_of_processes):
        headers.append(f"P{i + 1} comp t")
    headers.append("Schedule")

    print(tabulate(final_table, headers, tablefmt="grid"))


def lcm(the_list):
    new_list = []
    for element in the_list:
        new_list.append(element[1])
    # Snippet Source: https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
    lcm_ = 1
    for i in new_list:
        lcm_ = lcm_ * i // gcd(lcm_, i)
    return lcm_
    ####################################################################
