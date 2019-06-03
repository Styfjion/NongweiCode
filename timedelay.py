import time

lastintime = time.time()-1e2
for i in range(50):
    intime = time.time()
    time.sleep(1)
    if i%5 == 0 and int(intime-lastintime) > 9:
        print(str(i))
        lastintime = intime
    


