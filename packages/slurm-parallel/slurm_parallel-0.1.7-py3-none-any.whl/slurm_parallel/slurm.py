import re
import functools
import json
import subprocess
import inspect
import logging
import pathlib
import tempfile
import datetime
import os
import copy
import math
import time
import warnings
from string import Template
from importlib import resources

from tqdm import tqdm
import hyclib as lib

from . import config, utils

logger = logging.getLogger(__name__)
run_script = resources.files('slurm_parallel').joinpath('run.sh')
run_py_script = resources.files('slurm_parallel').joinpath('run.py')
summarize_script = resources.files('slurm_parallel').joinpath('summarize.sh')

allowed_args = {'A', 'account', 'acctg_freq', 'batch', 'bb', 'bbf', 'b', 'begin', 'D', 'chdir', 'cluster_constraint', 'M', 'clusters', 'comment', 'C', 'constraint', 'container', 'container_id', 'contiguous', 'S', 'core-spec', 'cores_per_socket', 'cpu_freq', 'cpus_per_gpu', 'c', 'cpus_per_task', 'deadline', 'delay_boot', 'd', 'dependency', 'm', 'distribution', 'e', 'error', 'x', 'exclude', 'exclusive', 'export', 'export_file', 'extra', 'B', 'extra_node_info', 'get_user_env', 'gid', 'gpu_bind', 'gpu_freq', 'G', 'gpus', 'gpus_per_node', 'gpus_per_socket', 'gpus_per_task', 'gres', 'gres_flags', 'h', 'help', 'hint', 'H', 'hold', 'ignore_pbs', 'i', 'input', 'J', 'job_name', 'kill_on_invalid_dep', 'L', 'licenses', 'mail_type', 'mail_user', 'mcs_label', 'mem', 'mem_bind', 'mem_per_cpu', 'mem_per_gpu', 'mincpus', 'network', 'nice', 'k', 'no_kill', 'no_requeue', 'F', 'nodefile', 'w', 'nodelist', 'N', 'nodes', 'n', 'ntasks', 'ntasks_per_core', 'ntasks_per_gpu', 'ntasks_per_node', 'ntasks_per_socket', 'open_mode', 'O', 'overcommit', 's', 'oversubscribe', 'p', 'partition', 'power', 'prefer', 'priority', 'profile', 'propagate', 'q', 'qos', 'Q', 'quiet', 'reboot', 'requeue', 'reservation', 'signal', 'sockets_per_node', 'spread_job', 'switches', 'test_only', 'thread_spec', 'threads_per_core', 't', 'time', 'time_min', 'tmp', 'tres_per_task', 'uid', 'usage', 'use_min_nodes', 'v', 'verbose', 'V', 'version', 'wait_all_nodes', 'wckey', 'wrap'}

# See https://slurm.schedmd.com/sacct.html#SECTION_JOB-STATE-CODES
STATE_CODES = [
    'BOOT_FAIL',
    'CANCELLED',
    'COMPLETED',
    'DEADLINE',
    'FAILED',
    'NODE_FAIL',
    'OUT_OF_MEMORY',
    'PENDING',
    'PREEMPTED',
    'RUNNING',
    'REQUEUED',
    'RESIZING',
    'REVOKED',
    'SUSPENDED',
    'TIMEOUT',
]

__all__ = ['parallelize']

class StringTemplate(Template):
    delimiter = '%'
    idpattern = "(?a-i:[sF])" # ASCII-only, don't ignore case

@lib.functools.parametrized
def parallelize(func, database=None, table=None, columns=None, max_n_tasks=None, max_n_simul_tasks=None, tmp_dir=None, out_dir=None, out_file=None, time_per_config=30, wait=True, progress_dt=5, **default_kwargs):
    for k in default_kwargs:
        if k not in allowed_args:
            raise KeyError(f"parallelize got an unexpected argument '{k}'")
            
    funcname = func.__name__
    filename = inspect.getsourcefile(func)
    
    if table is None:
        table = funcname

    def run_task(tmp_filename):
        n_tasks = int(os.environ['SLURM_ARRAY_TASK_COUNT'])
        task_id = int(os.environ['SLURM_ARRAY_TASK_ID'])
        
        logger.info(f"Running task {task_id}...")
        
        with open(tmp_filename, 'r') as f:
            configs = json.load(f)
            
        config_indices = range(task_id, len(configs), n_tasks)
        
        logger.info(f"Config indices: {config_indices}")

        for i in config_indices:
            config = configs[i]
            
            result = func(**config)

            logger.info(f"Finished config {i}.")

            if database is not None:
                if table not in database:
                    raise RuntimeError(f"{table=} not found in {database=}.")
                    
                if columns is not None:
                    if isinstance(columns, str):
                        result = {columns: result}
                    else:
                        result = {column: v for v in result}

                database[table].append(config | result)

                logger.info(f"Saved output of config {i}.")
    
    def remote(configs, logging_kwargs=None, max_n_tasks=max_n_tasks, max_n_simul_tasks=max_n_simul_tasks, tmp_dir=tmp_dir, out_dir=out_dir, out_file=out_file, time_per_config=time_per_config, wait=wait, progress_dt=progress_dt, **kwargs):
        for k in kwargs:
            if k not in allowed_args:
                raise KeyError(f"remote got an unexpected argument '{k}'")
                
        if not isinstance(configs, list):
            raise TypeError(f"configs must be a list, but {type(configs)=}.")
            
        n_configs = len(configs)
        
        if n_configs == 0:
            logger.info("No configs to run, returning.")
            return
                
        if logging_kwargs is None:
            logging_kwargs = {}
                
        if max_n_tasks is None:
            completed_process = subprocess.run(
                ['scontrol', 'show', 'config'],
                capture_output=True,
                check=True,
            )
            max_n_tasks = int(re.search('MaxArraySize\s*= (\d*)', completed_process.stdout.decode("utf-8")).group(1))
                
        if tmp_dir is None and 'tmp_dir' in config:
            tmp_dir = config['tmp_dir']

        if out_dir is None:
            out_dir = config['out_dir']

        if out_file is None:
            out_file = config['out_file']
            
        if not isinstance(time_per_config, datetime.timedelta):
            time_per_config = datetime.timedelta(minutes=time_per_config)
            
        if not wait:
            raise NotImplementedError()
            
        if progress_dt < 1:
            warnings.warn("progress_dt less than 1 second, this may potentially cause server performance issues due to frequent polling.")
            
        pathlib.Path(tmp_dir).mkdir(parents=True, exist_ok=True)
        out_dir = StringTemplate(out_dir).safe_substitute(s=pathlib.Path(filename).stem, F=funcname)
        out_dir = pathlib.Path(datetime.datetime.now().strftime(out_dir))
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = StringTemplate(out_file).safe_substitute(s=pathlib.Path(filename).stem, F=funcname)
        
        n_tasks = min(n_configs, max_n_tasks)
        time_per_task = int(math.ceil(n_configs / n_tasks)) * time_per_config
        
        array = f'0-{n_tasks-1}'
        if max_n_simul_tasks is not None:
            array = f'{array}%{max_n_simul_tasks}'
        
        run_kwargs = {
            'c': 2,
            'mem_per_cpu': '2gb',
            'time': lib.datetime.strftime(time_per_task, '%d-%H:%M:%S'),
            'array': array,
            'output': out_dir / out_file,
            'parsable': not wait,
            'wait': wait,
            'job_name': f'{pathlib.Path(filename).stem}_{funcname}',
        } | default_kwargs | kwargs
        run_options = utils.to_cmd_options(**run_kwargs)
        
        logging_kwargs = {
            'capture_warnings': True
        } | logging_kwargs
        logging_options = utils.to_cmd_options(**logging_kwargs)
        
        with tempfile.TemporaryDirectory(dir=tmp_dir) as new_tmp_dir:
            tmp_filename = pathlib.Path(new_tmp_dir) / 'config.json'
            
            with open(tmp_filename, 'w') as f:
                json.dump(configs, f)
                
            logger.debug(f"Saved configs to tmp file {tmp_filename}.")
            
            args = ["sbatch", *run_options, run_script, run_py_script, filename, funcname, tmp_filename, *logging_options]
            logger.debug(f"Invoking subprocess with arguments {args}")
            
            run_PID, success = None, False
            try:
                with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, text=True) as p:
                    for line in p.stdout:
                        match = re.search('Submitted batch job ([0-9]{6})', line)
                        if match is not None:
                            run_PID = match.group(1)
                            break

                    logger.info(f'Submitted batch job {run_PID} for {pathlib.Path(filename).stem}.{funcname}')

                    t0, n_completed = 0, 0
                    with tqdm(total=n_tasks) as t:
                        while True:
                            if (p.poll() is not None) or (time.time() - t0 > progress_dt):
                                summary = subprocess.run([summarize_script, run_PID], capture_output=True, check=True, text=True)
                                state_info = {k.lower(): summary.stdout.count(k) for k in STATE_CODES}

                                t.update(n=(state_info['completed'] - n_completed))
                                n_completed = state_info.pop('completed')
                                t.set_postfix({k: v for k, v in state_info.items() if v > 0})
                                
                                if p.poll() is not None:
                                    break
                                    
                                t0 = time.time()

                    if p.returncode != 0:
                        raise subprocess.CalledProcessError(p.returncode, p.args)
                            
            except Exception as err:
                raise err
                
            else:
                success = True
                
            finally:
                if not success and run_PID is not None:
                    subprocess.run(['scancel', run_PID], check=True)
                    logger.info(f"Ensured batch job {run_PID} for {pathlib.Path(filename).stem}.{funcname} is cancelled.")
    
    func.run_task = run_task
    func.remote = remote
    
    return func
        
