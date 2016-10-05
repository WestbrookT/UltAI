import time

count = 0
total = 0

for i in range(0, 1000):
	start = time.time()
	temp = 123456789123456789123456789777777777777 % 5
	stop = time.time()
	total += stop -start
	count += 1

print(total)

count = 0
total = 0

for i in range(0, 1000):
	start = time.time()
	temp = 123456789123456789123456789777777777777 * .2
	temp = (temp - int(temp)) * 5
	stop = time.time()
	total += stop -start
	count += 1

print(total)