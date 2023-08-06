import argparse
import logging

import hyclib as lib

from slurm_parallel.utils import import_from_file_path

def main():
    parser = argparse.ArgumentParser('run.py')
    parser.add_argument('filename', type=str)
    parser.add_argument('funcname', type=str)
    parser.add_argument('tmp_file', type=str)
    parser.add_argument('--level', type=str, choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO')
    parser.add_argument('--format', type=str, default='%(levelname)s: %(name)s: %(message)s')
    parser.add_argument('--capture-warnings', action='store_true')
    
    args = parser.parse_args()
    
    lib.logging.basic_config(level=args.level, format=args.format, capture_warnings=args.capture_warnings)
    
    module, _ = import_from_file_path(args.filename)
    
    getattr(getattr(module, args.funcname), 'run_task')(args.tmp_file)

if __name__ == '__main__':
    main()