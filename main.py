import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime
from local.lib import utils
import os, json

print ("starting job ...")
print ("numpy version is", np.__version__)

import tensorflow as tf
print('TF VERSION', tf.__version__)
print ('GPUs', tf.config.list_physical_devices('GPU'))

vars = ['AWS_BATCH_CE_NAME', 'AWS_BATCH_JOB_ID', 'AWS_BATCH_JQ_NAME', 'PATH']

print ("------ ENV VARS -------")
for var in vars:
    if var in os.environ.keys():
       print (f'{var}={os.environ[var]}')
print ("-----------------------")

print (os.environ)

for i in range(5):
    print (f"{i:3d} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sleep(5)


print ("---------------------")

utils.command("df -h", printoutput=True)

_,s,_ = utils.command(f"curl 169.254.170.2{os.environ['AWS_CONTAINER_CREDENTIALS_RELATIVE_URI']}", printoutput=True)
aws_credentials = json.loads(s)

print ("credentials", aws_credentials)
print ("credentials-type", type(aws_credentials))


print ("accessing boto3")
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws_access_key'],
    aws_secret_access_key=os.environ['aws_secret_key'],
)

print ("-------- s3 buckets ---------")
print (s3.list_buckets())
print ("-----------------------------")