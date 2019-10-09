header = b'\x50\x41\x54\x43\x48' #PATCH
end = b'\x45\x4F\x46' #EOF

def patch(filelocation, patchlocation):
	# Open stuff
	file = open(filelocation, 'rb+')
	ips = open(patchlocation, 'rb')

	# Check if the file is indeed a IPS using the header
	if not ips.read(5) == header:
		raise Exception(patchlocation + ' failed IPS check!')

	# var for holding data to write
	data = []

	start = 5
	while True:
		ips.seek(start)
		# var for holding data before adding to the data var
		found = []
		# Check if is the end of the file
		if ips.read(3) == end:
			break

		# Get three-byte pointer
		ips.seek(start)
		found.append(int.from_bytes(ips.read(3), byteorder='big'))
		
		# Get two-byte size
		ips.seek(start + 3)
		found.append(int.from_bytes(ips.read(2), byteorder='big'))

		# Get the data
		ips.seek(start + 5)
		found.append(ips.read(found[1]))

		# Append to data var
		data.append(found)
		start = start + 5 + found[1]

	# write stuff
	for x in data:
		file.seek(x[0])
		file.write(x[2])