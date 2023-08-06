import pytest
import argparse
import os
import numpy as np
from ezqc.pbsq1 import run_pbsq1
from ezqc.psqs2 import run_psqs2
from ezqc.pbsc3 import run_pbsc3
from ezqc.psgc4 import run_psgc4
from ezqc.pbnc5 import run_pbnc5
from ezqc.sld6 import run_sld6
from ezqc.os7 import run_os7
from ezqc.ac8 import run_ac8


def test_addition():
    assert 2 + 2 == 4


# with open ("tests/SRR020192.fastq",'r') as file_obj:
#     header = file_obj.readline().strip()
#     if not header:
#         break
#     sequence = file_obj.readline().strip()
#     file_obj.readline()
#     quality_str = file_obj.readline().strip()
#     yield header, sequence, quality_str

# file.close()

# # Create the argparse object and define the arguments
# parser = argparse.ArgumentParser(description="EZQC FastQ Quality Analyzer")
# parser.add_argument('seqs', metavar='SEQ', nargs='+', help='input .fastq file(s)')

# # Parse the command-line arguments 
# args = parser.parse_args()

# directory_name = "ezqc_output"
# # Get the current working directory
# current_directory = os.getcwd()
# # Create a path for the new directory
# new_directory_path = os.path.join(current_directory, directory_name)

# # Create the directory if it doesn't already exist
# if not os.path.exists(new_directory_path):
#     os.makedirs(new_directory_path)
#     print(f"Directory '{directory_name}' created successfully!")
# else:
#     print(f"Directory '{directory_name}' already exists.")

# total_num = 0
# pass_num = 0

# # Process each .fastq file
# for file_path in args.seqs:
#     print(f"Processing file: {file_path}")
#     total_num += 1
#     headers = []
#     sequences = []
#     quality_strings = []

#     with open(file_path, 'r') as fastq_file:
#         for header, sequence, quality_str in parse_fastq_file(fastq_file):
#             headers.append(header)
#             sequences.append(sequence)
#             quality_strings.append(quality_str)
    # average_length_each_sequence = int(np.average([len(x) for x in quality_strings]))

# def function1():
    
# def function2():
    
# def function3():
    
# def function4():
    