from OpenViatica import ovutils
import time
start_time = time.time()
result = ovutils.fibonacci(100000)
print(time.time() - start_time)