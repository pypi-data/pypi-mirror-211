#!/usr/bin/env python

import os,sys
import json
import argparse
import numpy as np
from geometric.nifty import ang2bohr
from geometric.molecule import Molecule
from geometric.ase_engine import EngineASE

def parse_args(*args):
    parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter, fromfile_prefix_chars='@')

    grp_univ = parser.add_argument_group('universal', 'Relevant to every job')
    grp_univ.add_argument('input', type=str, help='REQUIRED positional argument: Quantum chemistry or MM input file for calculation\n ')
    grp_univ.add_argument('--nt', type=int, default=1, help='Specify number of threads for running in parallel\n(for TeraChem this should be number of GPUs)')

    grp_software = parser.add_argument_group('software', 'Options specific for certain software packages')
    grp_software.add_argument('--ase-class', type=str, default='xtb.ase.calculator.XTB', help='ASE calculator import path, eg. "ase.calculators.lj.LennardJones"')
    grp_software.add_argument('--ase-kwargs', type=str, default='{"method":"GFN2-xTB"}', help='ASE calculator keyword args, as JSON dictionary, eg. {"param_filename":"path/to/file.xml"}')

    grp_help = parser.add_argument_group('help', 'Get help')
    grp_help.add_argument('-h', '--help', action='help', help='Show this help message and exit')

    args_dict = {}
    for k, v in vars(parser.parse_args(*args)).items():
        if v is not None:
            args_dict[k] = v

    return args_dict

def main():
    args = parse_args(sys.argv[1:])
    M = Molecule(args["input"])[0]
    ase_class_name = args["ase_class"]
    ase_kwargs = args["ase_kwargs"]
    os.environ["OMP_NUM_THREADS"] = "%i" % args["nt"]
    engine = EngineASE.from_calculator_string(M, ase_class_name, **json.loads(ase_kwargs))
    coords = M.xyzs[0].flatten()*ang2bohr
    result = engine.calc_new(coords, '.')
    with open("run_ase_energy.txt", "w") as f:
        print("% 18.12e\n" % result['energy'], file=f)
    np.savetxt("run_ase_grad.txt", result['gradient'].reshape(-1, 3), fmt="% 18.12e")
        
if __name__ == '__main__':
    main()
