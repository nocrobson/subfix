#!/usr/bin/python3

import sys
import argparse

def usage():
    print(
    """ 
    How to use this program:

    subfix.py -f [subtitle-file.srt] (-s|-m|-h) (-s = seconds, -m = minutes, -h = hours) [time-adjust] (-a | -r) (-a = add, -r = remove)
    """
    )

def get_initial_time(unit_time, read_data):
    if 'seconds' in unit_time:
        return int(read_data[6:8])

    elif 'minutes' in unit_time:
        return int(read_data[3:5])

    elif 'hours' in unit_time:
        return int(read_data[0:2])

def get_final_time(unit_time, read_data):
    if 'seconds' in unit_time:
        return int(read_data[23:25])

    elif 'minutes' in unit_time:
        return int(read_data[20:22])

    elif 'hours' in unit_time:
        return int(read_data[17:19])

def set_initial_time(unit_time, initial, read_data, is_add_action):
    list_read_data = list(read_data)
    if 'seconds' in unit_time:                        
        adjust_minute = 0
        if initial > 59:
            new_initial_seconds = initial % 60
            if is_add_action == 1:
                adjust_minute = get_initial_time('minutes', read_data) + (initial / 60)
            else:
                adjust_minute = get_initial_time('minutes', read_data) - (initial / 60)

            list_read_data[3:5] = str(adjust_minute).zfill(2)    
            list_read_data[6:8] = str(new_initial_seconds).zfill(2)
        else:
            list_read_data[6:8] = str(initial).zfill(2)

    elif 'minutes' in unit_time:
        list_read_data[3:5] = str(initial).zfill(2)

    elif 'hours' in unit_time:
        list_read_data[0:2] = str(initial).zfill(2)
    
    return ''.join(list_read_data)

def set_final_time(unit_time, final, read_data, is_add_action):
    list_read_data = list(read_data)
    if 'seconds' in unit_time:      
        if final > 59:
            new_final_seconds = final % 60
            if is_add_action == 1:
                adjust_minute = get_final_time('minutes', read_data) + (final / 60)
            else:
                adjust_minute = get_final_time('minutes', read_data) - (final / 60)

            list_read_data[20:22] = str(adjust_minute).zfill(2)    
            list_read_data[23:25] = str(new_final_seconds).zfill(2)
        else:
            list_read_data[23:25] = str(final).zfill(2)

    elif 'minutes' in unit_time:
        list_read_data[20:22] = str(final).zfill(2)

    elif 'hours' in unit_time:
        list_read_data[17:19] = str(final).zfill(2)
    
    return ''.join(list_read_data)


def adjust_subs(absolute_file_path, unit_time, amount_adjust_time, is_add_action):
    print('Ajustando o arquivo '+ absolute_file_path)
    with open(absolute_file_path + '.adj', 'w+') as w:
        with open(absolute_file_path, "r", encoding='latin-1') as r:
            read_data = r.readline()
            while read_data:
                if '-->' in read_data:
                    initial = get_initial_time(unit_time, read_data) + int(amount_adjust_time)
                    final   = get_final_time(unit_time, read_data) + int(amount_adjust_time)
                    list_read_data = set_initial_time(unit_time, initial, read_data, is_add_action)
                    list_read_data = set_final_time(unit_time, final, list_read_data, is_add_action)
                    w.write(''.join(list_read_data))
                else:
                    w.write(read_data)

                read_data = r.readline()
        
        w.close()
    print('Novo arquivo ' + absolute_file_path + '.adj criado com os ajustes de legenda')

def prepare_commands():
    print("In development...")

def main(argv):
    prepare_commands()
    if argv[1] == '-h' or argv[1] == '--help':
        usage()

    elif argv[1] == '-f':
        absolute_file_path = ''
        unit_time = 'seconds'
        is_add_action = 0
        amount_adjust_time = 0

        # Validate the parameters
        if argv[2] is None:
            print("Please inform the sub file to adjust")

        elif argv[3] is None:
            print("Please inform the time unit that must be adjusted")
        elif argv[4] is None:
            print("Please inform the amount of time that must be adjusted")

        elif argv[5] is None:
            print("Please inform if i must add or remove time")

        else:
            absolute_file_path = argv[2]

            if argv[3] == '-s':
                unit_time = 'seconds'
            elif argv[3] == '-m':
                unit_time = 'minutes'
            elif argv[3] == '-h':
                unit_time = 'hours'
            else:
                print("time-adjust parameter invalid!")

            amount_adjust_time = argv[4]

            if argv[5] == '-a':
                is_add_action = 1 
            else:
                is_add_action = 0

            adjust_subs(absolute_file_path, unit_time, amount_adjust_time, is_add_action)
            return None
        
        usage()
        
    else:
        print("Bad usage, try --help option!!!")


if __name__ == "__main__":
    ret = main(sys.argv)
    if ret is not None:
        sys.exit(ret)
