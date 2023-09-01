### Create juypyter kernel

⚠️ This repo is in alpha version. Things are currently not properly documented.

This repo aims at creating and easily adding new kernels to jupyterlab.

It:
- Creates a new virtual environment (with the possibility to give the required dependencies)
- Adds it automatically to jupyterlab kernels

For now, only Python kernels are created with conda and mamba. 
Supporting venv, pyproject.toml, and local editable kernel (pip install -e .) would also be a nice to have. 

### Syntax:

To create and add a python 3.10 kernel named `super_project` run:

```bash
python -m create_jupyter_kernel.py -n the_kernel_name_i_want -p 3.10
```
The `-r` option also alows to install the requirements.txt present in the current folder (it is also possible to provide a path).

This would create a new kernel available in your jupyterlab with Python 3.10.

In the future, it would be nice to be able to :

`$ add_kernel my_new_kernel_name --python=3.2 --mamba=False pandas==0.2 `
`$ 
generate_new_jupyter_kernel
 my_new_kernel_name --python=3.2 --mamba=False pandas==0.2 `

