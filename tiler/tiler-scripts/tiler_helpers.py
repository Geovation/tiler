import os

def check_environ_vars():
    ## Check all environment variables are defined
    env_vars = ['DB_NAME', 'DB_USER', 'DB_PORT', 'DB_HOST', 'DB_PASSWORD']
    for env_var in env_vars:
        if env_var not in os.environ:
            raise ValueError("Necessary environment variable not set not: ", env_var) 


def check_file(FILE_NAME):
    if not os.path.isfile(FILE_NAME):
        raise IOError(FILE_NAME + " does not exist")
