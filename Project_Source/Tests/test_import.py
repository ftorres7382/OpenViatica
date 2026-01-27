from OpenViatica import rust_fibonacci
from OpenViatica import ovutils
import time
start_time = time.time()
result = ovutils.fibonacci(100)
print(time.time() - start_time)

start_time = time.time()
result = rust_fibonacci(100)
print(time.time() - start_time)