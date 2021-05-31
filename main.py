import numpy as np
from local.lib import utils
import os
import tensorflow as tf

print ('TF VERSION', tf.__version__)
print ('GPUs', tf.config.list_physical_devices('GPU'))
print ('running job', os.environ['JOBNAME'])

## get dataset from S3 if required
utils.command("aws s3 cp s3://clotheme-jobs/data/ACGPN_data.tar.gz .")
utils.command("tar zxvf ACGPN_data.tar.gz")


## simulate some output
utils.command("mkdir output")
with open("output/results.txt", "w") as f:
    for _  in range(100):
        f.write(str(np.random.randint(10000000))+"\n")

with open("output/extra.txt", "w") as f:
    for _  in range(100):
        f.write("AAA"+str(np.random.randint(10000000))+"\n")


## send  output to S3 
utils.command(f"aws s3 cp --recursive output s3://clotheme-jobs/outputs/{os.environ['JOBNAME']}", printoutput=True)

