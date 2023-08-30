### https://episyche.com/blog/how-to-build-a-cli-tool-using-python
### 
### Add a test for whether the virtual environment already exists or the kernel name is already taken.
import getopt
import sys
import os
import subprocess

nameargv = sys.argv[1:]
command = "conda"
python_argument=""

opts,argv = getopt.getopt(nameargv, "n:prm", ["name =", "python-version =", "requirements","mamba"])

requirements_txt = False
for o,v in opts:
    if o in ['-n','--name']:
        conda_env_name = v
    elif o in ['-r','--requirements']:
        requirements_txt = True
        if v:
            requirements_txt_path = os.getcwd()+"/"+v
        else:
            requirements_txt_path = os.getcwd()+"/requirements.txt"
    elif o in ['-p','--python-version']:
        python_version = v
        python_argument = f"python={python_version}"
        print(python_argument)
    elif o in ['-m','--mamba']:
        command = "mamba"
        
        


        
#subprocess.run(f'conda create --yes -n {conda_env_name} python=3.7 ipykernel', shell=True)
subprocess.run(f'{command} create --yes -n {conda_env_name} {python_argument} ipykernel', shell=True, check=True)
if requirements_txt:
    subprocess.run(f'{command} run -n {conda_env_name} pip install -r {requirements_txt_path}', shell=True, check=True)
    
subprocess.run(f'{command} run -n {conda_env_name} pip install ipykernel', shell=True, check=True)
subprocess.run(f'{command} run -n {conda_env_name} python -m ipykernel install --user --name={conda_env_name}', shell=True, check=True)

