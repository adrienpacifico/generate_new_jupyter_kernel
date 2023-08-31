

"""
python ../app/create_jupyter_kernel.py -n test_cli2 -p 3.8 -r # returns an error if not compatible when running the pip operation
"""

import os
import subprocess
import pytest
from jupyter_client.kernelspecapp import InstallKernelSpec
from jupyter_client.kernelspecapp import ListKernelSpecs

def call_cmd(shell_command:str):
    """
    run a command, with assertion if the command line did not work (return code =! 0)
    with the error message if so.
    """
    cmd_result_ = subprocess.run(shell_command, shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    assert cmd_result_.returncode == 0, f"Return code not 0, Error: \n {cmd_result_.stderr}"
    return cmd_result_


def test_simple():
    """
    simplest test for the cli implementation
    """
    call_cmd(f'python create_jupyter_kernel.py -n test_simple')
    

    app = InstallKernelSpec()
    prefix = os.path.dirname(os.environ['PATH'])
    kernel_dir = os.path.join(prefix, 'share/jupyter/kernels')
    app1 = ListKernelSpecs()
    app1.kernel_spec_manager.kernel_dirs.append(kernel_dir)
    specs = app1.start()
    specs["test_simple"] # test that the environment is indeed created (KeyError if not)
    #@pytest.mark.order(2)
    #def test_delete_test_simple():
    #    #subprocess.run("jupyter kernelspec uninstall test_simple", check=True)
    #    subprocess.run("conda remove --name test_simple --all --yes", check=True)


def test_python_3_9():
    """
    Create an environment with python 3.9 and checks that it is indeed
    the python version installed in the virtual environment.
    """
    call_cmd(f'python create_jupyter_kernel.py -n test_python39 -p 3.9')

    app = InstallKernelSpec()
    prefix = os.path.dirname(os.environ['PATH'])
    kernel_dir = os.path.join(prefix, 'share/jupyter/kernels')
    app1 = ListKernelSpecs()
    app1.kernel_spec_manager.kernel_dirs.append(kernel_dir)
    specs = app1.start()
    python_interpreter_venv_path = specs["test_python39"]['spec']['argv'][0]
    cmd_result = call_cmd(f"{python_interpreter_venv_path} --version")
    assert str(cmd_result.stdout).split(" ")[1][:3]=="3.9"
    
      
def test_mamba_simple():
    """
    Create an environment with mamba.
    Does not actually check that the environment is indeed created with mamba.
    """
    call_cmd(f'python create_jupyter_kernel.py -m -n test_mamba')

    app = InstallKernelSpec()
    prefix = os.path.dirname(os.environ['PATH'])
    kernel_dir = os.path.join(prefix, 'share/jupyter/kernels')
    app1 = ListKernelSpecs()
    app1.kernel_spec_manager.kernel_dirs.append(kernel_dir)
    specs = app1.start()
    specs["test_mamba"] # test that the environment is indeed created (KeyError if not)
    ### Test that is has been created with mamba with the history file in conda/envs/test_mamba/conda-meta"
    cmd_result = subprocess.run("conda info --base", shell=True,stderr=subprocess.PIPE, stdout=subprocess.PIPE) # get conda path 
    conda_path = str(cmd_result.stdout)[2:-3]
    env_path = conda_path+"/"+"envs/test_mamba/conda-meta"
    with open(env_path+"/history", 'r') as file:
        file_text = file.read()
    first_cmd = file_text.split("\n")[1] # first command used to create the env
    env_creator_exec_path = first_cmd.split(" ")[2] # executable used to create the env
    assert "/".join(env_creator_exec_path.split("/")[-3:]) ==  'conda/bin/mamba'
    