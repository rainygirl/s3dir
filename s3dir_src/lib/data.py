import os
import sys
from .s3 import S3


KUBE_COMMANDS = {
    "getpods": "kubectl get pods",
    "getcontainers": "kubectl get pods #pod -o jsonpath='{.spec.containers[*].name}'",
    "getlist": "kubectl exec -it #pod -c #container -- sh -c \"ls -ls ./#path | awk '{print \\$2,\\$10,\\$6}'\"",
}


def load_data(S, section="local"):

    if section == "local":
        with os.scandir(S["path"]["local"]) as entries:
            dirs, files = [], []

            for d in entries:
                (dirs if d.is_dir() else files).append(d)
            dirs = sorted(dirs, key=lambda x: x.name)
            files = sorted(files, key=lambda x: x.name)
            if S["path"]["local"] == "/":
                return dirs + files
            return [".."] + dirs + files
    else:
        if S["remoteorigin"] == "S3":
            s3 = S3(bucket=S["s3bucket"])
            try:
                return s3.load_data(S["path"]["remote"])
            except Exception as e:
                sys.exit(e)

        elif S["remoteorigin"] == "kubectl":
            if S["kubectl"]["pod"] == "":
                var = os.popen(KUBE_COMMANDS["getpods"]).read()
                pods = var.split("\n")[1:]
                if len(pods) == 0:
                    sys.exit("No pods")
                return pods
            elif S["kubectl"]["container"] == "":
                var = os.popen(
                    KUBE_COMMANDS["getcontainers"].replace("#pod", S["kubectl"]["pod"])
                ).read()
                containers = var.split(" ")
                if len(containers) == 0:
                    sys.exit("No containers")
                return [".."] + containers
            else:
                var = os.popen(
                    KUBE_COMMANDS["getlist"]
                    .replace("#pod", S["kubectl"]["pod"])
                    .replace("#container", S["kubectl"]["container"])
                    .replace("#path", S["path"]["remote"])
                ).read()
                dirs = []
                files = []
                for d in var.split("\n")[1:]:
                    if len(d) == 0 or d[0] == ".":
                        continue

                    s = d.split(" ")
                    if s[0][0] == "d":
                        dirs.append(f"{s[1]}/")
                    else:
                        files.append(
                            {
                                "key": s[1],
                                "size": int(s[2]),
                            }
                        )
                dirs = sorted(dirs, key=lambda x: x)
                files = sorted(files, key=lambda x: x["key"])

                return [".."] + dirs + files
