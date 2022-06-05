from queue import PriorityQueue
from queue import Queue

from Process import Process


def PE_SJF():
    burst_str = input("Enter Burst Times separate with SPACE :\n")
    arrival_str = input("Enter Arrival Times separate with SPACE :\n")

    # convert burst_str into int list
    try:
        b_str = burst_str.split(" ")
        a_str = arrival_str.split(" ")
        if len(b_str) != len(a_str):
            print("CHECK YOUR INPUT!!")
            exit(1)
        burst_list = []
        arrival_list = []
        for b_ele in b_str:
            burst_list.append(int(b_ele))
        for a_ele in a_str:
            arrival_list.append(int(a_ele))
        # print(burst_list)
        # print(arrival_list)
    except ValueError:
        print("WRONG FORM OF INPUT!!!")
        exit(1)
    #####################################################

    process_list = []
    # create Process lists ID starting from 0
    for i in range(len(burst_list)):
        process_list.append(Process(process_id=i, burst_time=burst_list[i], arrival_time=arrival_list[i]))

    schedule = PriorityQueue(maxsize=len(burst_list))
    waiting_q = PriorityQueue(maxsize=len(burst_list))

    for process in process_list:
        arr_t = process.arrival_time
        rem_t = process.remaining_time
        if arr_t == 0:
            # tuples
            schedule.put((rem_t, arr_t, process))
        else:
            waiting_q.put((arr_t, process))

    process_event_list = []
    time = 0
    while not schedule.empty():
        # print(schedule.get()[2].burst_time)
        # checking if more process arrives, if yes, put it into schedule queue, else remain in waitingQ
        event = []
        if not waiting_q.empty():
            waiting_process = waiting_q.get()[1]
            waiting_arrival = waiting_process.arrival_time
            remain_time = waiting_process.remaining_time
            if time == waiting_arrival:
                schedule.put((remain_time, waiting_arrival, waiting_process))
            else:
                waiting_q.put((waiting_arrival, waiting_process))

        current_ready_list = get_processes_in_queue(schedule)

        current_process = schedule.get()[2]

        event.append(current_process.process_id)

        current_process.remaining_time -= 1
        time += 1
        other_ready_process_waiting_plus_1(current_process.process_id, current_ready_list)

        event.append(time)

        if current_process.remaining_time == 0:
            pass
        else:
            schedule.put((current_process.remaining_time, current_process.arrival_time, current_process))

        process_event_list.append(event)

    total_waiting_time = 0
    print()
    for element in process_list:
        total_waiting_time += element.cumulative_waiting_time
        print("P" + str(element.process_id + 1) + " Waiting Time: " + str(element.cumulative_waiting_time))

    average_waiting_time = total_waiting_time / len(process_list)
    print()
    print("Average Waiting Time: " + str(average_waiting_time))

    # print(process_event_list)

    temp = process_event_list.copy()
    for jj in range(len(temp)):
        for ii in range(1, len(temp)):
            if temp[ii][0] == temp[ii-1][0]:
                temp[ii-1] = temp[ii]
    timing_arr = [temp[0]]

    j = 0
    for iii in range(len(temp)):
        if timing_arr[j] == temp[iii]:
            pass
        else:
            j += 1
            timing_arr.append(temp[iii])
    # print(timing_arr)

    final_print_array = [[timing_arr[0][0], timing_arr[0][1], timing_arr[0][1]]]
    for i in range(1, len(timing_arr)):
        final_print_array.append([timing_arr[i][0], timing_arr[i][1]-timing_arr[i-1][1], timing_arr[i][1]])

    print_schedule(final_print_array)




def get_processes_in_queue(queue):
    ps_l = []
    while not queue.empty():
        ps_l.append(queue.get())

    for ele in ps_l:
        queue.put(ele)

    ps_li = []
    for ii in range(len(ps_l)):
        ps_li.append(ps_l[ii][2])

    return ps_li


def other_ready_process_waiting_plus_1(the_id, obj_l):
    new_list = other_process_havent_done(the_id, obj_l)
    for ele in new_list:
        ele.cumulative_waiting_time += 1




def other_process_havent_done(the_id, obj_l):
    new_list = []
    for element in obj_l:
        if element.remaining_time != 0 and element.process_id != the_id:
            new_list.append(element)
    return new_list

# [PROCESS_ID, RUNNING_TIME_CURRENT_ROUND, TOTAL_TIME_SNAPSHOT]
def convert_schedule_list(the_list):
    new_list = []
    for i in range(len(the_list)):
        time_snap = 0
        for j in range(i + 1):
            time_snap += the_list[j][1]
        new_list.append([the_list[i][0], the_list[i][1], time_snap])
    return new_list


def print_schedule(the_list):
    new_list = convert_schedule_list(the_list)

    result_str = " | "
    for i in new_list:
        result_str += "P" + str(i[0] + 1) + " t:" + str(i[1]) + " \t| "

    timing_str = " 0"
    for i in new_list:
        timing_str += "\t\t\t" + str(i[2])

    print(result_str)
    print(timing_str)
