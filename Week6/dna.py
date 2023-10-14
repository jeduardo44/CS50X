import csv
import sys


def main():
    if len(sys.argv) != 3:
        sys.exit("Invalid number of command line arguments")

    # TODO: Read database file into a variable

    csv_file = sys.argv[1]
    data = []  # Initialize an empty list to store the dictionaries
    with open(csv_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    sequences = {}
    for i in data[0]:
        sequences[i] = 0
    del sequences["name"]

    # TODO: Read DNA sequence file into a variable

    file_path = sys.argv[2]
    file_contents = ""
    with open(file_path, "r") as file:
        file_contents = file.read()

    # TODO: Find longest match of each STR in DNA sequence

    for i in sequences:
        sequences[i] = longest_match(file_contents, i)
    # TODO: Check database for matching profiles

    for i in range(len(data)):
        match = False
        for j in sequences:
            if sequences[j] == int(data[i][j]):
                match = True
            else:
                match = False
                break
        if match:
            name = data[i]["name"]
            return print(name)

    return print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
