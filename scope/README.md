scope
=====

This is a simple Oscilloscope logger for the Raspberry Pi.

The main program **RasPi_logGPIO.sh** logs digital signals from the GPIO pins into a text file. By calling **RasPi_normalizeGPIO.py**, this file gets converted into a file readable for [xoscope](http://xoscope.sourceforge.net/).

Before you can use it, you have to compile **RasPi_logGPIO.cpp** (on the Raspberry Pi or at least for ARMv6):
```bash
g++ -o RasPi_logGPIO RasPi_logGPIO.cpp
```
After that, you can call **RasPi_logGPIO.sh** with the GPIO pins as an argument (on the Raspberry Pi):
```bash
./RasPi_logGPIO.sh 14 31 23 > logfile_14_31_23.txt
```
This will log the values of GPIO14, GPIO31 and GPIO23 as fast as possible into logfile_14_31_23.txt until you abort with Ctrl+C.

It's important to know that this program doesn't use a static sample rate and that you have to normalize it with the Python program to get usable data. You should do this on another computer, because the script needs relatively much RAM and CPU time:
```bash
./RasPi_normalizeGPIO.py logfile_14_31_23.txt > logfile_14_31_23.dat
```
Now, **logfile_14_31_23.dat** is an xoscope file. You can open it and recall the saved channels. In this example, GPIO14 will be in Memory A, GPIO31 in Memory B and GPIO23 in Memory C.

## Examples ##
I used this program to log the sensor values of the Epson Model-620, a printer for a calculating machine.

The signals don't have a really big frequency, but I got pretty good results:
![Scale: 1x](http://www.abload.de/img/epson_rechenmaschine_aziby.png)
![Scale: 2.5x](http://www.abload.de/img/epson_rechenmaschine_qscgq.png)
