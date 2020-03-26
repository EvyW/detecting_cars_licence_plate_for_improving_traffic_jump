import datetime
from datetime import time

class classPicoyPlaca:

    def pico_y_placa():

    # Function for entering the date and validate it
        def enter_and_validate_date():
            inputDate = input("Enter the date in format 'dd/mm/yy'")
            day, month, year = inputDate.split('/')
            isValidDate = True
            try:
                datetime.datetime(int(year), int(month), int(day))
            except ValueError:
                isValidDate = False
            if (isValidDate):
                print("Date is valid")
                weekday = datetime.datetime(int(year), int(month), int(day)).weekday()
                return weekday
            else:
                print("Date is NOT valid! please, try again with a valid date")
                exit()


        # Function for entering the time and validate it
        def enter_and_validate_time():
            inputTime = input("Enter the time in 24 hour format 'HH:MM' (hour:minute)")
            hour, minute = inputTime.split(':')
            isValidTime = True
            try:
                datetime.time(int(hour), int(minute))
            except ValueError:
                isValidTime = False
            if (isValidTime):
                print("Time is valid")
                return inputTime
            else:
                print("Time is NOT valid! please, try again with a valid time")
                exit()


        # Function for entering the license plate and validate whether it is correct
        def enter_and_validate_plate_number():
            # enter the license plate number
            input_plate = input("Enter the license plate in format 'Province abbreviation-Numbers' (3 letters and 3 or 4 numbers)")
            province_abbr, plate_number = input_plate.split('-')

            # Validate whether the "plate number" is a number and has minimum 3 characters and maximum 4
            is_valid_plate = True
            try:
                # 1) Check whether the plate_number are truly numbers --> Try to convert plate number to integers
                int(plate_number)
                # 2) Check whether the number of numbers in the plate are minimum 3 and maximum 4
                lenght_plate_number = len(plate_number)
                if lenght_plate_number < 3 or lenght_plate_number > 4:
                    raise ValueError('Number of characters in plate number is not correct, enter 3 or 4 numbers')
            except ValueError:
                is_valid_plate = False

            if (is_valid_plate):
                print("License plate numbers are valid")

                # Now validate whether the "province abbreviation" is a string and has exclusively 3 characters
                is_valid_abbr = True
                try:
                    # 1) Check whether the "province abbraviation" is a string --> check whether they are not numbers as strings
                    is_not_string = province_abbr.isdigit()
                    if is_not_string == True:
                        raise ValueError('Are not letters')
                    # 2) Check whether there are only 3 characters
                    lenght_province_abbr = len(province_abbr)
                    if lenght_province_abbr != 3:
                        raise ValueError('Number of characters is incorrect')
                except ValueError:
                    is_valid_abbr = False

                if (is_valid_abbr):
                    print("Province abbreviation is valid")

                    # If plate number and province abbreviation are ok, then return the last digit of the plate number
                    last_digit = int(plate_number[-1])
                    return last_digit
                else:
                    print("Province abbreviation is NOT valid! please, try again with a valid format")
                    exit()
            else:
                print("License plate number is NOT valid! please, try again with a valid format")
                exit()


        # Function for checking whether the time lies in between the time restriction
        def is_time_between(begin_time, end_time, check_time):
            # If check time is not given, default to current UTC time
            check_time = check_time
            if check_time >= begin_time and check_time <= end_time:
                return True


        # Finally evaluate whether the car can be pn the road

        # retrieve last digit of license plate
        last_digit = enter_and_validate_plate_number()
        # retrieve weekday
        weekday = enter_and_validate_date() # Note that 0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday
        # retrieve time
        get_time = enter_and_validate_time()
        hour, minute = get_time.split(':')

        # Rule for Mondays
        if weekday == 0 and \
                (last_digit == 1 or last_digit == 2) and\
                (is_time_between(time(7, 0), time(9, 30), time(int(hour),int(minute))) == True or\
                 is_time_between(time(16, 0), time(19, 30), time(int(hour),int(minute))) == True):
            print('The car can NOT be on the road!')
        # Rule for Tuesdays
        elif weekday == 1 and \
                (last_digit == 3 or last_digit == 4) and\
                (is_time_between(time(7, 0), time(9, 30), time(int(hour),int(minute))) == True or\
                 is_time_between(time(16, 0), time(19, 30), time(int(hour),int(minute))) == True):
            print('The car can NOT be on the road!')
        # Rule for Wednesdays
        elif weekday == 2 and \
                (last_digit == 5 or last_digit == 6) and\
                (is_time_between(time(7, 0), time(9, 30), time(int(hour),int(minute))) == True or\
                 is_time_between(time(16, 0), time(19, 30), time(int(hour),int(minute))) == True):
            print('The car can NOT be on the road!')
        # Rule for Thursdays
        elif weekday == 3 and \
                (last_digit == 7 or last_digit == 8) and\
                (is_time_between(time(7, 0), time(9, 30), time(int(hour),int(minute))) == True or\
                 is_time_between(time(16, 0), time(19, 30), time(int(hour),int(minute))) == True):
            print('The car can NOT be on the road!')
        # Rule for Friday
        elif weekday == 4 and \
                (last_digit == 9 or last_digit == 0) and\
                (is_time_between(time(7, 0), time(9, 30), time(int(hour),int(minute))) == True or\
                 is_time_between(time(16, 0), time(19, 30), time(int(hour),int(minute))) == True):
            print('The car can NOT be on the road!')
        else:
            print('The car can be on the road ;)')
