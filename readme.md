In Latin American countries the traffict jump it's big problem. One of the solutions that is commonly applied consists on restricting the cars that can circulate. This restriction is usually according to the last number of the "car licence plate". For example, cars which has 1 as the last number of the license plate, can not cirulate on Moday. 

This repository contains two programs coded in python that according to a picture of the car determines whether the car can circulate or not:

1) "license_plate_detection.py": identifies the license plate of the car in the picture and then tells us the ID number of the plate.

2) "picoyplaca.py": tests whether the car can be on the road by following the restriction: A car can not drive in the city from 7:00 to 9:30 and from 16:00 to 19:30 according to the last digit of the license plate on the following days:
- Monday: cars whose last digit ends in 1 or 2
- Tuesday: cars whose last digit ends in 3 or 4
- Wednesday: cars whose last digit ends in 5 or 6
- Thursday: cars whose last digit ends in 7 or 8
- Friday: cars whose last digit ends in 9 or 0

Execution:
You can execute both programs using
"master.py". The program will ask you to provide the input.

Note:
Both programs can be used independently.
