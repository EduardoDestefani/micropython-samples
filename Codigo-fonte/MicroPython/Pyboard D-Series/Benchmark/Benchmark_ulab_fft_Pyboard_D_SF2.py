import gc
gc.collect()
free_ram_i = gc.mem_free()
import time
ti_time = time.ticks_us()
dt_time = time.ticks_diff(time.ticks_us(), ti_time)
ti_import = time.ticks_us()
import ulab as np
from ulab import vector
from ulab import fft
dt_import = time.ticks_diff(time.ticks_us(), ti_import)

n_points = 1024
x = np.linspace(0, 10, num=n_points)
y = vector.sin(x)
ti_fft = time.ticks_us()
a, b = fft.fft(y)
dt_fft = time.ticks_diff(time.ticks_us(), ti_fft)

gc.collect()
free_ram_f = gc.mem_free()

print("Free RAM from {} to {} bytes, so {} bytes used ".format(free_ram_i, free_ram_f, free_ram_i - free_ram_f))
print("Time to import ulab v{} : {:.3f} ms".format(np.__version__, (dt_import - dt_time)/1000))
print("Time to calculate FFT of {} points : {:.3f} ms".format(n_points, (dt_fft - dt_time)/1000))
