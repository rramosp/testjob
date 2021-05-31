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

vars = ['AWS_BATCH_CE_NAME', 'AWS_BATCH_JOB_ID', 'AWS_BATCH_JQ_NAME', 'JOBNAME']

print ("------ ENV VARS -------")
for var in vars:
    if var in os.environ.keys():
       print (f'{var}={os.environ[var]}')


s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws_access_key'],
    aws_secret_access_key=os.environ['aws_secret_key'],
)
print ("-------- s3 buckets ---------")
print (s3.list_buckets())
print ("-----------------------------")

utils.command("aws s3 ls", printoutput=True)


#utils.command("which amazon-linux-extras", printoutput=True)
#utils.command("which yum", printoutput=True)
#utils.command("/usr/bin/sudo amazon-linux-extras install -y s3fs-fuse", printoutput=True)
#utils.command("/usr/bin/sudo yum install -y s3fs-fuse", printoutput=True)
