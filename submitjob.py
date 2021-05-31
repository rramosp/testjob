import argparse, json
from datetime import datetime
import boto3
from local.lib.utils import command

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--job-name', required=False, help='AWS batch jobname')
parser.add_argument('--job-queue', default='train_models_queue', help='AWS batch job queue')
parser.add_argument('--job-definition', default='CPU_tensorflow', help='AWS batch job definition')
args = parser.parse_args()

# commit content to github
print ("\n------ committing to github ---------")
command("git commit -a -m iterate", printoutput=True)
command("git push", printoutput=True)

# build job name
_, gitremote, _ = command("git remote -v")
gitremote = gitremote.split("\n")[0].split()[1].split(":")[-1]
_, gitcommit, _ = command("git rev-parse --short HEAD")
gitcommit = gitcommit.split("\n")[0]

if args.job_name is None:
    job_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + "__" + gitremote + "__" + gitcommit
else:
    job_name = args.job_name

job_name = job_name.replace("/", "__").replace(".git", "")

# include credentials as env vars in the running container
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
                "name": "JOBNAME",
                "value": job_name
            },
            {
                "name": "AWS_ACCESS_KEY_ID",
                "value": creds.access_key
            },
            {
                "name": "AWS_SECRET_ACCESS_KEY",
                "value": creds.secret_key
            },
            {
                "name": "AWS_DEFAULT_REGION",
                "value": session.region_name
            }
        ]
    }
}

# launch job
with open("job.json", "w") as f:
    json.dump(job,f)

print ("\n------ submitting job ---------")
command("aws batch submit-job --cli-input-json file://job.json", printoutput=True)
command("rm job.json")
