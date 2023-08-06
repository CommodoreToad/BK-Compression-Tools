import math
import sys

def main():

	table1 = []
	table4 = []
	filename = sys.argv[1]
	with open(filename,'rb') as f:
		byte_count = 0
		while (byte:= f.read(1)):
			byte = int.from_bytes(byte, "big")
			if byte_count <256:
				table1.append(byte)
			elif byte_count == 256:
				c1 = byte<<24
			elif byte_count == 257:
				c2 = byte<<16
			elif byte_count == 258:
				c3 = byte<<8
			elif byte_count == 259:
				c4 = byte
			else:
				table4.append(byte)
			byte_count +=1
	

	outfile2 = open(filename + '_decoded','wb')

	hex_c = 0

	code_count =[]
	for x in range(256):
		code_count.append(0)
	c_d = 0
	
	table2 = [] 
	table2.append(0) # Need to add a 0 to table 2, this corresponds to 0x8022dfc6 between table 1 and table 2
	table3=[]
	


	a = 0 #starting value
	b = 0XFFFFFFFF # starting value
	option = 0 # starting value
	store_c = 1
	cache_c = 0XFEE

	
	c = c1 + c2 +c3 + c4
	
	# Load all of the remaining c values into an array
	for x in range(260, len(table1)):
		temp = str2int(table1[x])
		table4.append(temp)

	# This is the counter array. Once c needs to pulled, increaste by 1
	c_count = 0
	
	# Calculate table 2 from table 1
	for x in range(256):
		table2.append(table2[x]+table1[x])
	
	# Calculate table 3
	for x in range(1,257):
		nbyte = table2[x] - table2[x-1]
		for y in range(nbyte):
			table3.append(x-1)

	
	cache = []
	for x in range(4096):
		cache.append(0) 

	while c_count < len(table4):
	
		b = math.floor((b/table2[-1]))
		t1 = c-a
		t2 = math.floor(t1/b)
		decoded = table3[t2]
		
		
		code_count[decoded] += 1
		
		c_d+=1
		

		t3=int(round((decoded<<1)/2,0)) #divide by 2 

		t4=table2[t3]
		
		a = t4*b + a

		b = table1[t3]*b
	


		if option == 2: 
			store2 = decoded
			option = 3	
		
		elif option ==0: 
			store = decoded
			option = next_option(decoded,1)
	
		elif option == 1: 
			outfile2.write(decoded.to_bytes(1,'big'))
			cache[cache_c] = decoded
			cache_c += 1
			if cache_c == 4096:
				cache_c = 0
			store_c *= 2
			if store_c ==256:
				store_c = 1
				option = 0
			else:
				option = next_option(store,store_c)


				
		elif option == 3: 
			t2 = mask_high(decoded,4) +3
			loop_counter = t2<<31>>32
			loop_extra = t2%2
			t1 = decoded>>4<<8
			index = store2 + t1

	
			
			for x in range(loop_counter):
				outfile2.write(cache[index].to_bytes(1,'big'))
				cache[cache_c] = cache[index]
				
				index+=1
				if index == 4096:
					index = 0
				
				cache_c += 1
				if cache_c == 4096:
					cache_c = 0
				

				outfile2.write(cache[index].to_bytes(1,'big'))
				cache[cache_c] = cache[index]
				
				index+=1
				if index == 4096:
					index = 0

				cache_c += 1
				if cache_c == 4096:
					cache_c = 0
			if loop_counter==0:
				loop_extra==1
			
			if loop_extra == 1:
				outfile2.write(cache[index].to_bytes(1,'big'))
				cache[cache_c] = cache[index]
				
				index+=1
				if index == 4096:
					index = 0
				
				cache_c += 1
				if cache_c == 4096:
					cache_c = 0
					
			store_c *= 2
			if store_c ==256:
				store_c = 1
				option = 0
			else:
				option = next_option(store,store_c)
	

		xor = 0x01000000
		
		boo_xor = True
		
		while boo_xor:
		
		
			t5= a+b
			t6=a^t5


			if t6 < xor:
				t6a = c<<8
				t6b = t6a>>32<<32
				t6c = table4[c_count]
				c = t6a - t6b + t6c
				c_count+=1

				t6a = b<<8
				t6b = t6a>>32<<32
				b = t6a - t6b

				t6a = a<<8
				t6b = t6a>>32<<32
				a = t6a - t6b

				

			else:
				boo_xor =False
				
		while b <8192:
		
			c = c<<8
			c = mask_high(c,32)
			c = c + table4[c_count]
			c_count +=1
			
			b=0xFFFFFFFF-a+1
			b = b<<8
			b = mask_high(b,24)
			
			a =a<<8
			a=mask_high(a,32)


	

def next_option(decoded,compare):

	t1 = decoded&compare
	t2 = -1*t1
	t3 = t2 | compare
	t4 = t3>>31
	option = t4+2
 
	return option

def str2int(value):
    convert_string = int(value, base=16)
    return convert_string

def mask_high(value,bits):
	#Value is the number to be masked, bits is how many bits to keep
	value = value - (value>>bits<<bits)
	return(value)
	

	
    
if __name__ == '__main__':
    main()
