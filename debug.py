import os
import subprocess
import tempfile
import json
import debugpy
import shutil

# config
port = 5678

# edit your code here
code = """# test example
sum = (5+10)
print("The sum of 5 and 10 is", sum)
"""
#############################################

def write_file(filepath: str, content: str):
    f = open(filepath, "w")
    f.write(content)
    f.close()

os.makedirs("temp", exist_ok=True)
dirname = tempfile.mkdtemp(dir="temp")

print('created temporary directory', dirname)
main_py = os.path.join(dirname, "main.py")

write_file(main_py, code)
os.makedirs(os.path.join(dirname, ".vscode"), exist_ok=True)
write_file(os.path.join(dirname, ".vscode", "launch.json"), json.dumps({
    "configurations": [{
        "name": "Python Debugger: Remote Attach",
        "type": "debugpy",
        "request":"attach",
        "connect":{"host":"localhost","port": port},
        "pathMappings":[
            {"localRoot":"${workspaceFolder}/main.py", "remoteRoot": main_py},
        ],
        "justMyCode": False
    }],
    "version":"0.2.0"
}))

compiled_code = compile(code, main_py, "exec")
debugpy.listen(port)

proc = subprocess.Popen(['code', dirname, main_py], shell=True)

print("Waiting for debugger attach")
debugpy.wait_for_client()
exec(compiled_code)

# print('close subpocess:', proc.wait())
# proc.terminate()

# shutil.rmtree(dirname)