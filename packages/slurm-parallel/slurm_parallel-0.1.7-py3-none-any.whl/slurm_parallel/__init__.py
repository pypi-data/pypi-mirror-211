import hyclib as lib

config = lib.config.load_package_config('slurm_parallel')

del lib

from .slurm import *