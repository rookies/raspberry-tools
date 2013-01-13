#!/usr/bin/python
import sys, math

if len(sys.argv) < 2:
	print("Usage: " + sys.argv[0] + " logfile.txt", file=sys.stderr)
f = open(sys.argv[1], "r")
print("Reading file " + sys.argv[1] + " ...", file=sys.stderr)
l = f.readline()
cnumber = int(l.split("###")[1])
print("Number of Channels: " + str(cnumber), file=sys.stderr)
print("Calculating sample rates ...", file=sys.stderr)
executed = False
last_times = [-1 for x in range(cnumber)]
min_times = [-1 for x in range(cnumber)]
max_times = [-1 for x in range(cnumber)]
samplerates = [-1 for x in range(cnumber)]
for line in f:
	line = line.replace("\n", "").split("#")
	i = 0
	for channel in line:
		channel = channel.split(".")
		time = (int(channel[0])*1000000000)+int(channel[1])
		intv = time-last_times[i]
		if not executed:
			min_times[i] = intv
		else:
			if intv < min_times[i]:
				min_times[i] = intv
			if intv > max_times[i]:
				max_times[i] = intv
		last_times[i] = time
		i += 1
	executed = True
i = 0
for time in min_times:
	print("Channel " + str(i) + ":", file=sys.stderr)
	print("  Minimum interval (ns): " + str(time), file=sys.stderr)
	print("  Minimum interval (s): " + str(time/1000000000.), file=sys.stderr)
	print("  Maximum sample rate (Hz): " + str(1./(time/1000000000.)), file=sys.stderr)
	samplerates[i] = math.ceil(1./(time/1000000000.))
	print("  Maximum sample rate rounded (Hz): " + str(samplerates[i]), file=sys.stderr)
	print("  ====", file=sys.stderr)
	print("  Maximum interval (ns): " + str(max_times[i]), file=sys.stderr)
	print("  Maximum interval (s): " + str(max_times[i]/1000000000.), file=sys.stderr)
	print("  Minimum sample rate (Hz): " + str(1./(max_times[i]/1000000000.)), file=sys.stderr)
	print("  Minimum sample rate rounded (Hz): " + str(math.floor(1./(max_times[i]/1000000000.))), file=sys.stderr)
	i += 1

f.seek(0)
f.readline()
# Write file header:
print("# xoscope, version 2.0")
print("#")
# Write channel names:
print("# ", end="")
for i in range(cnumber):
	if i != 0:
		print("\t", end="")
	print(chr(97+i) + "(15)", end="")
print("")
# Write samplerates:
print("#:", end="")
for i in range(cnumber):
	if i != 0:
		print("\t", end="")
	print(samplerates[i], end="")
print("")
# Write third line:
print("#=", end="")
for i in range(cnumber):
	if i != 0:
		print("\t", end="")
	print("0", end="")
print("")
# Read source values from file:
source_data = [[] for x in range(cnumber)]
for line in f:
	line = line.replace("\n", "").split("#")
	i = 0
	for channel in line:
		channel = channel.split(".")
		time = int(channel[0])*1000000000+int(channel[1])
		value = int(channel[2])
		source_data[i].append((time, value))
		i += 1
# Normalize and write data:
output_data = [[] for x in range(cnumber)]
for i in range(cnumber):
	offset_sourceindex = 0
	for val in range(source_data[i][0][0], source_data[i][-1][0]+1, min_times[i]):
		while True:
			if source_data[i][offset_sourceindex+1][0] <= val:
				offset_sourceindex += 1
			if source_data[i][offset_sourceindex][0] <= val:
				output_data[i].append(source_data[i][offset_sourceindex][1])
				break
			else:
				offset_sourceindex += 1
for i in range(max(len(x) for x in output_data)):
	for j in range(cnumber):
		if j != 0:
			print("\t", end="")
		if len(output_data[j]) > i:
			print(str(output_data[j][i]*100), end="")
	print("")
