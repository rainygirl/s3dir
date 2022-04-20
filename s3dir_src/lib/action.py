import os
import sys
from .s3 import S3


def action_and_exit(action, S):
    if action == "copy":
        for path in S["queue"]:
            filename = path.split("/")[-1] if "/" in path else path
            if S["remoteorigin"] == "kubectl":
                if S["section"] == "remote":
                    newpath = os.path.join(S["path"]["local"], filename)
                    cmd = f"kubectl cp {S['kubectl']['pod']}:{path} {newpath} -c {S['kubectl']['container']}"
                    sys.stdout.write(f"{S['kubectl']['pod']}:{path}\n -> {newpath}\n")
                else:
                    newpath = S["path"]["remote"] + filename
                    cmd = f"kubectl cp {path} {S['kubectl']['pod']}:{newpath} -c {S['kubectl']['container']}"
                    sys.stdout.write(f"{path}\n -> {S['kubectl']['pod']}:{newpath}\n")

                out = os.popen(cmd).read()
                if out.strip() != "":
                    sys.stdout.write(f"{out}\n\n")

            elif S["remoteorigin"] == "S3":
                s3 = S3(bucket=S["s3bucket"])

                if S["section"] == "remote":
                    newpath = os.path.join(S["path"]["local"], filename)
                    s3.download(key=path, destination=newpath)
                    sys.stdout.write(f"s3://{S['s3bucket']}/{path}\n -> {newpath}\n")
                else:
                    newpath = S["path"]["remote"] + filename
                    s3.upload(source=path, key=newpath)
                    sys.stdout.write(f"{path}\n -> s3://{S['s3bucket']}/{newpath}\n")

    sys.stdout.write("Done\n")
    sys.exit()
