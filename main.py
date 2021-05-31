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

vars = ['AWS_BATCH_CE_NAME', 'AWS_BATCH_JOB_ID', 'AWS_BATCH_JQ_NAME', 'PATH']

print ("------ ENV VARS -------")
for var in vars:
    if var in os.environ.keys():
       print (f'{var}={os.environ[var]}')


print ("-----------------------")
utils.command("df -h", printoutput=True)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws_access_key'],
    aws_secret_access_key=os.environ['aws_secret_key'],
)
print ("-------- s3 buckets ---------")
print (s3.list_buckets())
print ("-----------------------------")

utils.command("sudo amazon-linux-extras install -y s3fs-fuse", printoutput=True)
utils.command("sudo yum install -y s3fs-fuse", printoutput=True)
utils.command("s3fs", printoutput=True)
utils.command(f"echo {os.environ['aws_access_key']}:{os.environ['aws_secret_key']} > ~/.passwd-s3fs")
utils.command("cat ~/.passwd-s3fs", printoutput=True)
utils.command("chmod 600 ~/.passwd-s3fs")
utils.command("mkdir s3")
utils.command("s3fs clotheme-jobs s3")
utils.command("ls -las s3", printoutput=True)