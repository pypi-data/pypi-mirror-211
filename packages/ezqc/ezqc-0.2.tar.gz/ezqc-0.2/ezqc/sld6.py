import matplotlib.pyplot as plt
from .color_print import print_color
from collections import Counter

def calculate_sequence_lengths(sequences):
    sequence_lengths = [len(seq) for seq in sequences]
    # Detect warning and failure situations
    if 0 in sequence_lengths:
        print_color("X | Some sequences have zero length.","red")
    if len(set(sequence_lengths)) > 1:
        print_color("- | Not all sequences are of the same length.","yellow")
    else:
        print_color("O | Lengths of Sequences are good","green")
        
    return Counter(sequence_lengths)

def plot_sequence_lengths(sequence_lengths):
    plt.figure()
    plt.bar(sequence_lengths.keys(), sequence_lengths.values())
    plt.title("Sequence Length Distribution")
    plt.xlabel("Sequence Length")
    plt.ylabel("Number of Sequences")
    # Save and/or display the plot
    plt.savefig("ezqc_output/Sequence_Length_Distribution.png")
    # plt.show()

def run_sld6(sequences):
    # print("running function 6: Sequence Length Distribution")
    sequence_lengths = calculate_sequence_lengths(sequences)
    plot_sequence_lengths(sequence_lengths)
    return True

    