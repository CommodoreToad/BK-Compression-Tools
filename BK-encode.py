import math
import subprocess
import os
import sys

def main():
	low = 0
	ranges = 0xFFFFFFFF

		
	filename = sys.argv[1]
	file3 = filename
	filename = filename.strip('_decoded')
	
	path = os.path.dirname(sys.argv[0])
	
	file1 = filename + '_lzss'
	file2 = filename + '_c'
	file4 = path + '\\lzss.exe'

	
	subprocess.call([file4, 'e', file3, file1])

	outfile = open(file2, 'wb')
	
	byte_count =[]
	prob_table = []
	prob_table.append(0)
	
	for x in range(256):
		byte_count.append(0)
		
	with open(file1,'rb') as f:
		while (byte:= f.read(1)):
			byte = int.from_bytes(byte, "big")
			byte_count[byte] += 1
	
	max_val = 0
	for x in range(256):
		if byte_count[x] > max_val:
			max_val = byte_count[x]

	for x in range(256):
		byte_count[x] = math.ceil(byte_count[x]*255/max_val)
		outfile.write(byte_count[x].to_bytes(1,'big'))
		
	for x in range(1,257):
		prob_table.append(prob_table[x-1] + byte_count[x-1])

	total = prob_table[-1]
	
	
	with open(file1,'rb') as f:
		while (byte:= f.read(1)):
			byte = int.from_bytes(byte, "big")
	
			t1 = math.floor(ranges/prob_table[-1])
			
			t3 = int(round((byte<<1)/2,0))
			t4 = prob_table[byte]
			

			
			low = t4*t1+low

			ranges = byte_count[t3]*t1

			xor = 0x01000000
			boo_xor = True
			while boo_xor:
	
				
				t5 = low+ranges
				t6=low^t5
				if t6 <xor:
					outfile.write((low>>24).to_bytes(1,'big'))
					t6a = ranges<<8
					t6b = t6a>>32<<32
					ranges = t6a - t6b

					t6a = low<<8
					t6b = t6a>>32<<32
					low = t6a - t6b

				else:
					boo_xor =False

			while ranges < 8192:
				
				outfile.write((low>>24).to_bytes(1,'big'))
				
				ranges=0xFFFFFFFF-low+1
				ranges = ranges<<8
				ranges = mask_high(ranges,24)
				
				low =low<<8
				low=mask_high(low,32)


	while ranges > 0x1000000:
		outfile.write((low>>24).to_bytes(1,'big'))
		t6a = ranges<<8
		t6b = t6a>>32<<32
		ranges = t6a - t6b

		t6a = low<<8
		t6b = t6a>>32<<32
		low = t6a - t6b
		
	outfile.write((low).to_bytes(1,'big'))

	os.remove(file1)

def mask_high(value,bits):
	#Value is the number to be masked, bits is how many bits to keep
	value = value - (value>>bits<<bits)
	return(value)


if __name__ == '__main__':
    main()
