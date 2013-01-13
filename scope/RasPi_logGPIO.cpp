// g++ -o RasPi_logGPIO RasPi_logGPIO.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include <time.h>

using namespace std;

int main (int argc, char **argv)
{
	/*
	 * Variable declarations:
	*/
	int i;
	int *gpio;
	int gpio_len;
	ofstream file_o;
	ifstream *file_i;
	stringstream tmp;
	struct timespec now;
	char c[2];
	/*
	 * Check arguments:
	*/
	if (argc < 2)
	{
		cerr << "Usage: " << argv[0] << " gpio1 [gpio2] [...]" << endl;
		return 1;
	};
	/*
	 * Convert GPIO numbers:
	*/
	gpio_len = argc-1;
	gpio = new int[gpio_len];
	for (i=0; i < gpio_len; i++)
		gpio[i] = atoi(argv[i+1]);
	/*
	 * Activate GPIO:
	*/
	for (i=0; i < gpio_len; i++)
	{
		cerr << "Activating GPIO" << gpio[i] << "..." << endl;
		file_o.exceptions(ofstream::failbit | ofstream::badbit);
		file_o.open("/sys/class/gpio/export");
		file_o << gpio[i];
		file_o.close();
	}
	/*
	 * Set as input:
	*/
	for (i=0; i < gpio_len; i++)
	{
		cerr << "Setting GPIO" << gpio[i] << " as input..." << endl;
		file_o.exceptions(ofstream::failbit | ofstream::badbit);
		tmp.str("");
		tmp << "/sys/class/gpio/gpio" << gpio[i] << "/direction";
		file_o.open(tmp.str().c_str());
		file_o << "in";
		file_o.close();
	}
	/*
	 * Write file header:
	*/
	cout << "###" << gpio_len << "###" << endl;
	/*
	 * Read & Write loop:
	*/
	cerr << "Start reading..." << endl;
	file_i = new ifstream[gpio_len];
	for (i=0; i < gpio_len; i++)
	{
		file_i[i].exceptions(ifstream::failbit | ifstream::badbit);
		tmp.str("");
		tmp << "/sys/class/gpio/gpio" << gpio[i] << "/value";
		file_i[i].open(tmp.str().c_str());
	}
	while (true)
	{
		for (i=0; i < gpio_len; i++)
		{
			file_i[i].get(c, 2);
			if (i != 0)
				cout << "#";
			clock_gettime(CLOCK_MONOTONIC, &now);
			cout << now.tv_sec << "." << now.tv_nsec << "." << atoi(c);
			file_i[i].seekg(0);
		}
		cout << endl;
	}
	/*
	 * Delete variables:
	*/
	delete[] gpio;
	delete[] file_i;
	return 0;
}
