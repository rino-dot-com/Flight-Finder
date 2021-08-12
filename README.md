# Flight Finder

Sample command line input: *python flights.py < input.txt > output.txt 2> error.txt*

This a test project I wrote that creates a record of flights and searches the record for any flight paths. It only accepts a file as input using Standard In. All output is sent to Standard Out and errors are directed to Standard Error. The program uses a txt file for the records and it'll create one if one doesn't already exist. Works in Windows or Linux.

You use specific commands to add/update/search the records:

ADD command - *ADD source,destination,distance,time*</br>
This adds a record to the "database" or updates if the record already exists. It also outputs the record after it successfully adds it.

QUERY command - *QUERY source,destination*</br>
This searches the records for any flights between the two cities. It will return all possible paths, including paths that take multiple flights. It outputs every path it finds along with the cost of each path (which is calculated based on the time and distance of the flights using an arbitrary formula), all in ascending order of cost.

Incorrect inputs and failed QUERYs will return an error message containing the input that caused the error.

Input commands should be written to a txt file and the txt file used as the input for the program. Multiple commands can be written to the input file.</br>
I've included an input file that can be used for testing and to demonstrate how commands should be written to the file.
