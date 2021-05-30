import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime

print ("starting job ...")
print ("numpy version is", np.__version__)

import tensorflow as tf
print('TF VERSION', tf.__version__)
print ('GPUs', tf.config.list_physical_devices('GPU'))

for i in range(20):
    print (f"{i:3d} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sleep(5)






