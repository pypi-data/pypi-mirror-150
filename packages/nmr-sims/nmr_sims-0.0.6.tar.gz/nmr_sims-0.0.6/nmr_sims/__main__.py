# __main__.py
# Simon Hulse
# simon.hulse@chem.ox.ac.uk
# Last Edited: Mon 28 Feb 2022 12:25:37 GMT

import argparse
import subprocess
import sys

from nmr_sims import ROOT_DIR

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sample experiment specification."
    )

    parser.add_argument("experiment", default="pa", choices=("pa", "jres", "hsqc"))
    args = parser.parse_args()

    experiment_dir = ROOT_DIR.parent
    if args.experiment == "pa":
        path = experiment_dir / "experiments/pa.py"
    elif args.experiment == "jres":
        path = experiment_dir / "experiments/jres.py"
    elif args.experiment == "hsqc":
        path = experiment_dir / "experiments/hsqc.py"

    subprocess.run([sys.executable, path])
