def main():
    
    import os
    import sys
    import subprocess
    import argparse
    import configparser
    import datetime
    import random
    import pandas as pd

    image = 'iszatt/phusion:0.0.1'

    # No commands given prompt
    if len(sys.argv) == 1:
        print('No commands given? \nUse -h or --help for more information')
        sys.exit(1)

    # Finding the user
    result = subprocess.run(['id', '-un'], stdout=subprocess.PIPE)
    login = result.stdout.decode().strip()

    # Did you know prompt
    prompts = [
        "My (J.Iszatt) favourite bacteriophage is a Silviavirus named Koomba-kaat_1",
        "This container attempts to infer data from 50 of its closest matches using blast",
        "The data used to create the blast database within this container comes from Inphared (see README)",
        "This container requires input from PhageOrder, if phages could not be ordered then they are excluded (sorry)",
        "The data this container provides may be used to generate phage cocktails with different tail fiber proteins",
        "We include phylogenetic inference because tail fibers are not a sole dictator of host range",
        "We include the integrase scan because those phages are much more likely to be lysogenic",
        "Please email me at joshiszatt@gmail.com for collaborations",
    ]
    random_prompt = random.choice(prompts)

    # Functions
    def valid_dir(dir_path):
        if not os.path.isdir(dir_path):
            raise argparse.ArgumentTypeError(
                f"{dir_path} is not a valid directory path")
        if not os.access(dir_path, os.R_OK):
            raise argparse.ArgumentTypeError(
                f"{dir_path} is not a readable directory")
        return dir_path

    # Parsing arguments
    parser = argparse.ArgumentParser(description=image)

    # Input/output options
    parser.add_argument('-i', '--input', required=True, type=valid_dir,  help='Path to PhageOrder output')
    parser.add_argument('-o', '--output', required=True, type=valid_dir, help='Direct output to specified location')
    parser.add_argument('--cluster', type=int, default=1, help='Clustering threshold (default=1)')

    # Adding flags
    parser.add_argument('-v', '--version', action="store_true", help='Print the version of the container this will activate')
    parser.add_argument('--show_console', action="store_true", help='Include this flag to write output to console')
    parser.add_argument('--manual', action="store_true", help='Enter container interactively')

    # Finish parsing arguments
    args = parser.parse_args()

    # Printing version
    if args.version:
        print(image)
        sys.exit(1)

    # Obtaining absolute paths
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    # Printing command variables
    print(
        f"Program run: {image}",
        f"Input file: {input_path}",
        f"Output file: {output_path}",
        ">>>",
        f"Did you know:",
        f"{random_prompt}",
        ">>>",
        sep='\n'
        )

    if args.show_console:
        docker = "docker run"
    else:
        docker = "docker run -d"

    # Running docker
    if args.manual:

        os.system(f"docker exec -it \
            $(docker run -d \
            -v {input_path}:/craft/input \
            -v {output_path}:/craft/output \
            {image} sleep 1d) bash")

    else:

        command = ["%s -v %s:/craft/input -v %s:/craft/output %s /craft/bin/phagecraft.sh %s" %
                (docker, input_path, output_path, image, args.cluster)]
        result = subprocess.Popen(command, shell=True)
        print(command)
