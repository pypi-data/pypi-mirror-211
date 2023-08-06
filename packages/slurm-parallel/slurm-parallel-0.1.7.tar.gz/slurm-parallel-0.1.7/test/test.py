import logging
import time

import sqlalchemy as sa
import dfdb
import hyclib as lib

import slurm_parallel as sp

db = dfdb.Database(database='/home/hc3190/slurm-parallel/test/data/test.db', connect_args={"timeout": 30})
logger = logging.getLogger()

@sp.parallelize(mem_per_cpu='1mb', c=1, partition='ctn')
def print_results():
    df = db['results'].fetch()
    print(df)

@sp.parallelize(database=db, table='results', columns='result', mem_per_cpu='1gb', c=1, partition='ctn')
def func(a, b):
    time.sleep(20)
    # if a == 5:
    #     raise RuntimeError()
    return a + b

def main():
    lib.logging.basic_config()
    logger.setLevel('DEBUG')
    
    if 'results' in db:
        del db['results']
        
    db['results'] = dfdb.TableDef(
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('a', sa.Integer()),
        sa.Column('b', sa.Integer()),
        sa.Column('result', sa.Integer()),
        sa.Column('created', sa.DateTime(), server_default=sa.func.now()),
    )
    
    configs = [
        {'a': 1, 'b': 2},
        {'a': 3, 'b': 4},
        {'a': 5, 'b': 6},
        {'a': 7, 'b': 8},
    ]
    # job = func.remote(configs, wait=False, max_n_tasks=3, logging_kwargs=dict(level='DEBUG'))
    # print_results.remote([{}], wait=False, dependency=f'afterany:{job}')
    
    # func.remote(configs, max_n_tasks=3, logging_kwargs=dict(level='DEBUG'))
    func.remote(configs, max_n_tasks=3, max_n_simul_tasks=2, p='issa', A='issa', logging_kwargs=dict(level='DEBUG'))
    print_results.remote([{}])

if __name__ == '__main__':
    main()