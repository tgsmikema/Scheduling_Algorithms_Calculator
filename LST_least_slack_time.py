from tabulate import tabulate
from math import gcd
from CyclicProcess import CyclicProcess
from queue import PriorityQueue


def LST():
    num_of_processes = int(input("Enter Number of Processes: "))
    p_info = []
    for i in range(num_of_processes):
        a, b, c = [int(x) for x in input(f"Enter (c, p, d) with Space Separated For Process {i + 1}: ").split(' ')]
        p_info.append([a, b, c])

    major_cycle = lcm(p_info)

    process_list = []

    # create Process instances and save it into a list
    i = 0
    for element in p_info:
        process_list.append(CyclicProcess(c=element[0], p=element[1], d=element[2], process_id=i))
        i += 1

    schedule = PriorityQueue(num_of_processes)

    for element in process_list:
        schedule.put((element.slack_time, element.in_prev_round, element.process_id, element))

    final_table = []
    for time in range(major_cycle):
        frame = [time]
        for e in process_list:
            e.in_prev_round = 1

        for element in process_list:
            if time == element.next_deadline:
                # every new period update remaining comp time, and rejoin the queue
                element.remaining_c = element.c
                element.slack_time = element.d - element.c
                element.next_deadline = (int(time / element.d) + 1) * element.d
                if previous_process_id != element.process_id:
                    schedule.put((element.slack_time, element.in_prev_round, element.process_id, element))
                else:
                    schedule.put((element.slack_time, element.in_prev_round, element.process_id, element))
            element.next_deadline = (int(time / element.d) + 1) * element.d
            # frame.append(element.next_deadline)

        for element in process_list:
            frame.append(element.remaining_c)
        for element in process_list:
            frame.append(element.slack_time)

        if schedule.empty():
            frame.append(-1000)
            final_table.append(frame)
            continue
        else:
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

            if current_process.remaining_c != 0:
                current_process.slack_time = current_process.next_deadline - (time + 1) - current_process.remaining_c
            elif current_process.remaining_c == 0:
                current_process.slack_time = 9999

            for eee in process_list:
                if eee.slack_time < 5000:
                    eee.slack_time = eee.next_deadline - (time + 1) - eee.remaining_c

            #     pass
            # else:
            #     schedule.put((current_process.slack_time, 0, current_process.process_id, current_process))

            while not schedule.empty():
                schedule.get()
            for proces in process_list:
                if proces.slack_time < 1000 and proces.process_id != previous_process_id:
                    schedule.put((proces.slack_time, proces.in_prev_round, proces.process_id, proces))

            the_list = get_minimum_slack(process_list)
            for ele in the_list:
                if ele.process_id == previous_process_id:
                    ele.in_prev_round = 0

            for proces in process_list:
                if proces.slack_time < 1000 and proces.process_id == previous_process_id:
                    schedule.put((proces.slack_time, proces.in_prev_round, proces.process_id, proces))


            final_table.append(frame)

    # print(final_table)

    for element in final_table:
        element[len(element) - 1] = str("P" + str(element[len(element) - 1] + 1))

    # print(final_table)

    headers = ["Time"]
    for i in range(num_of_processes):
        headers.append(f"P{i + 1} comp t")
    for i in range(num_of_processes):
        headers.append(f"P{i + 1} slack t")
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

def get_minimum_slack(the_list):
    ret = [the_list[0]]
    min_slk = the_list[0].slack_time
    position = 0
    for i in range(len(the_list)):
        if the_list[i].slack_time <= min_slk:
            min_slk = the_list[i].slack_time
            ret[0] = the_list[i]
            position = i

    for i in range(len(the_list)):
        if i != position:
            if the_list[i].slack_time == ret[0].slack_time:
                ret.append(the_list[i])

    return ret