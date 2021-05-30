import argparse, subprocess

def command(cmd, printoutput=False):
    """
    Runs a command in the underlying shell

    Parameters:
    -----------

    cmd : str
        string containing the command to run

    Returns:
    --------
    code:  int
        return code from the executed command

    stdout: str
        captured standard output from the command

    stderr: str
        captured standard error from the command

    """
    try:
        # search for single quoted args (just one such arg is accepted)
        init = cmd.find("'")
        end  = len(cmd)-cmd[::-1].find("'")
        if init>0 and init!=end-1:
            scmd = cmd[:init].split() + [cmd[init+1:end-1]] + cmd[end+1:].split()
        else:
            scmd = cmd.split()

        p = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = p.communicate()
        code = p.returncode
    except Exception as e:
        stderr = str(e)
        code = 127
        stdout = ""

    stdout = stdout.decode() if type(stdout)==bytes else stdout
    stderr = stderr.decode() if type(stderr)==bytes else stderr

    if printoutput:
        if code!=0:
            print ("------ CODE --------", code)
        if stdout!="":
            print ("------ STDOUT ------\n", stdout)
        if stderr!="":
            print ("------ STDERR ------\n", stderr)


    return code, stdout, stderr


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--job-name', required=True, help='AWS batch jobname')
parser.add_argument('--job-queue', default='train_models_queue', help='AWS batch job queue')
parser.add_argument('--job-definition', default='CPU_tensorflow', help='AWS batch job definition')
#parser.add_argument('--repo', required=True, help='AWS batch jobname')

args = parser.parse_args()
print ("ARGS", args)

job = f"asdasd{args}asdasd"

job = f"""
{{
    "jobName": "{args.job_name}",
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

print (job)

# get git info
_, gitremote, _ = command("git remote -v")
gitremote = gitremote.split("\n")[0].split()[1].split(":")[-1]
_, gitcommit, _ = command("git rev-parse --short HEAD")

print (gitremote, gitcommit)

command("git commit -a -m iterate", printoutput=True)
command("git push", printoutput=True)



"""

code, stdout, stderr = command("aws batch submit-job")

print ("CODE", code)
if stdout!="":
    print ("------ STDOUT ------\n", stdout)
if stderr!="":
    print ("------ STDERR ------\n", stderr)
"""