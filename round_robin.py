from queue import Queue

from Process import Process


def RR():
    burst_str = input("Enter Burst Times separate with SPACE :\n")
    time_slice = int(input("Enter Time Slice: "))

    # convert burst_str into int list
    try:
        b_str = burst_str.split(" ")
        b_list = []
        for b_ele in b_str:
            b_list.append(int(b_ele))
        # print(b_list)
    except ValueError:
        print("WRONG FORM OF INPUT!!!")
        exit(1)

    process_list = []
    # create Process lists ID starting from 0
    for i in range(len(b_list)):
        process_list.append(Process(process_id=i, burst_time=b_list[i]))

    schedule = Queue(maxsize=len(b_list))

    for process in process_list:
        schedule.put(process)

    process_event_list = []
    while not schedule.empty():

        current_process = schedule.get()
        event = [current_process.process_id]

        if current_process.remaining_time <= time_slice:
            time_taken = current_process.remaining_time
            current_process.remaining_time = 0
            event.append(time_taken)
            other_list = other_process_havent_done(current_process.process_id, process_list)
            for p in other_list:
                p.cumulative_waiting_time += time_taken

        else:
            current_process.remaining_time -= time_slice
            event.append(time_slice)
            other_list = other_process_havent_done(current_process.process_id, process_list)
            for p in other_list:
                p.cumulative_waiting_time += time_slice
            schedule.put(current_process)

        process_event_list.append(event)

    # print(process_event_list)
    total_waiting_time = 0
    for element in process_list:
        total_waiting_time += element.cumulative_waiting_time
        print("P" + str(element.process_id + 1) + " Waiting Time: " + str(element.cumulative_waiting_time))

    average_waiting_time = total_waiting_time / len(process_list)
    print_schedule(process_event_list)
    print()
    print("Average Waiting Time: " + str(average_waiting_time))


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
