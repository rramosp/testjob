import argparse, json
from datetime import datetime
from local.lib.utils import command

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--job-name', required=False, help='AWS batch jobname')
parser.add_argument('--job-queue', default='train_models_queue', help='AWS batch job queue')
parser.add_argument('--job-definition', default='CPU_tensorflow', help='AWS batch job definition')
#parser.add_argument('--repo', required=True, help='AWS batch jobname')

args = parser.parse_args()
print ("ARGS", args)

# get git info

print ("\n------ committing to github ---------")
command("git commit -a -m iterate", printoutput=True)

print ("------ pushing to github ---------")
command("git push", printoutput=True)

_, gitremote, _ = command("git remote -v")
gitremote = gitremote.split("\n")[0].split()[1].split(":")[-1]
_, gitcommit, _ = command("git rev-parse --short HEAD")
gitcommit = gitcommit.split("\n")[0]

print (gitremote, gitcommit)

if args.job_name is None:
    job_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "__" + gitremote + "__" + gitcommit
else:
    job_name = args.job_name

job_name = job_name.replace("/", "__").replace(".git", "")

job = f"""
{{
    "jobName": "{job_name}",
    "jobQueue": "{args.job_queue}",
    "jobDefinition": "{args.job_definition}",
    "containerOverrides": {{
        "environment": [
            {{
                "name": "JOBREPO",
                "value": "https://github.com/rramosp/testjob"
            }}
        ]
    }}
}}
"""
import boto3

session = boto3.session.Session()
creds = session.get_credentials().get_frozen_credentials()

job = {
    "jobName": job_name,
    "jobQueue": args.job_queue,
    "jobDefinition": args.job_definition,
    "containerOverrides": {
        "environment": [
            {
                "name": "JOBREPO",
                "value": "https://github.com/rramosp/testjob"
            },
            {
                "name": "aws_secret_key",
                "value": creds.secret_key
            },
            {
                "name": "aws_access_key",
                "value": creds.access_key
            }
        ]
    }
}

with open("job.json", "w") as f:
    json.dump(job,f)

print ("\n------ submitting job ---------")
command("aws batch submit-job --cli-input-json file://job.json", printoutput=True)
command("rm job.json")
