import argparse
import numpy as np
from .pbsq1 import run_pbsq1
from .psqs2 import run_psqs2
from .pbsc3 import run_pbsc3
from .psgc4 import run_psgc4
from .pbnc5 import run_pbnc5
from .sld6 import run_sld6
from .os7 import run_os7
from .ac8 import run_ac8
import os

def parse_fastq_file(file_obj):
    while True:
        header = file_obj.readline().strip()
        if not header:
            break
        sequence = file_obj.readline().strip()
        file_obj.readline()
        quality_str = file_obj.readline().strip()
        yield header, sequence, quality_str

def main():
    logo = r'''
    ███████╗███████╗ ██████╗  ██████╗
    ██╔════╝╚══███╔╝██╔═══██╗██╔════╝
    █████╗    ███╔╝ ██║   ██║██║     
    ██╔══╝   ███╔╝  ██║▄▄ ██║██║     
    ███████╗███████╗╚██████╔╝╚██████╗
    ╚══════╝╚══════╝ ╚══▀▀═╝  ╚═════╝ made by Tinger Shi & Sky Li
    '''
    
    print(logo)

    # Create the argparse object and define the arguments
    parser = argparse.ArgumentParser(description="EZQC FastQ Quality Analyzer")
    parser.add_argument('seqs', metavar='SEQ', nargs='+', help='input .fastq file(s)')

    # Parse the command-line arguments 
    args = parser.parse_args()

    directory_name = "ezqc_output"
    # Get the current working directory
    current_directory = os.getcwd()
    # Create a path for the new directory
    new_directory_path = os.path.join(current_directory, directory_name)

    # Create the directory if it doesn't already exist
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
        print(f"Directory '{directory_name}' created successfully!")
    else:
        print(f"Directory '{directory_name}' already exists.")

    total_num = 0
    pass_num = 0

    # Process each .fastq file
    for file_path in args.seqs:
        print(f"Processing file: {file_path}")
        total_num += 1
        headers = []
        sequences = []
        quality_strings = []

        with open(file_path, 'r') as fastq_file:
            for header, sequence, quality_str in parse_fastq_file(fastq_file):
                headers.append(header)
                sequences.append(sequence)
                quality_strings.append(quality_str)
        # average_length_each_sequence = int(np.average([len(x) for x in quality_strings]))

    results = [
        run_pbsq1(quality_strings),
        run_psqs2(quality_strings),
        run_pbsc3(sequences),
        run_psgc4(sequences),
        run_pbnc5(sequences),
        run_sld6(sequences),
        run_os7(sequences),
        run_ac8(sequences)
    ]
    if all(results): 
        pass_num += 1
    print(f"All fastq file analyzied, {pass_num}/{total_num} passed all tests.")

if __name__ == '__main__':
    main()
