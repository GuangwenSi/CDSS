import time
num = 10000
# Run our time.sleep() command,
# and show the before and after time
print('Before: %s' % time.ctime())
print('step1')
time.sleep(num/9)
print('step2')
time.sleep(num/8)
print('step3')
time.sleep(num/7)
print('step4')
time.sleep(num/6)
print('step5')
time.sleep(num/5)
print('step6')
time.sleep(num/4)
print('step7')
time.sleep(num/3)
print('step8')
time.sleep(num/2)
print('step9')
time.sleep(num)
print('After: %s\n' % time.ctime())
