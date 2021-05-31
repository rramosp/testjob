import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime
from local.lib import utils
import os, json, boto3

print ("starting job ...")
print ("numpy version is", np.__version__)

import tensorflow as tf
print('TF VERSION', tf.__version__)
print ('GPUs', tf.config.list_physical_devices('GPU'))

vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_DEFAULT_REGION', 'AWS_BATCH_CE_NAME', 'AWS_BATCH_JOB_ID', 'AWS_BATCH_JQ_NAME', 'JOBNAME']

print ("------ ENV VARS -------")
for var in vars:
    if var in os.environ.keys():
       print (f'{var}={os.environ[var]}')

## retrieve dataset from S3 if required
utils.command("aws s3 cp s3://clotheme-jobs/data/ACGPN_data.tar.gz .")
utils.command("tar zxvf ACGPN_data.tar.gz")
utils.command("ls -las ACGPN_data", printoutput=True)


## simulate some output
utils.command("mkdir output")
with open("output/results.txt", "w") as f:
    for _  in range(100):
        f.write(str(np.random.randint(10000000))+"\n")


## send back output to S3 
#utils.command(f"aws s3api put-object --bucket clotheme-jobs --key outputs/{os.environ['JOBNAME']}", printoutput=True)
utils.command(f"aws s3 cp --recursive output s3://clotheme-jobs/outputs/{os.environ['JOBNAME']}", printoutput=True)

