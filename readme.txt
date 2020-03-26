This is a repository that consists of two independent programs coded in python:
1) "license_plate_detection.py" and 2) "picoyplaca.py". You can execute both using
"master.py". The program will ask you to provide the input.

The 1st program detects the license plate ID directly from pictures and
outputs a string with the plate ID. The 2nd program tests whether the car
can be on the road by following the restriction: A car can not drive in 
the city from 7:00 to 9:30 and from 16:00 to 19:30 according to the last digit of 
the license plate on the following days:
- Monday: cars whose last digit ends in 1 or 2
- Tuesday: cars whose last digit ends in 3 or 4
- Wednesday: cars whose last digit ends in 5 or 6
- Thursday: cars whose last digit ends in 7 or 8
- Friday: cars whose last digit ends in 9 or 0

Both programs can be used independently.
