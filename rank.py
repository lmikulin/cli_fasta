#!/usr/bin/env python

# import modules used here -- sys is a very standard one
import sys

# compare two sequences and return an array of mismatched indexes
def getDiffArray(seq1, seq2):
    diff_list = []
    min_length = min(len(seq1), len(seq2))
    for x in range(0, min_length):
        if not seq1[x] == seq2[x]:
            diff_list.append(x)

    max_length = max(len(seq1), len(seq2))
    for x in range(min_length, max_length):
        diff_list.append(x)

    return diff_list

# given ids, sequences and diff array for two sequences
# print out the diff to stdout
def printDiff(match, key1, key2, seq1, seq2, diff):
    print '\n', key1, ', ', key2, ', match: ', match
    print seq1
    for x in range(len(seq1)):
        if x in diff:
            sys.stdout.write("#")
        else:
            sys.stdout.write(" ")
    print ""
    print seq2
    return match

# build a hash of all the possible comparisons
# the key is (id1, id2) and the value is the diff indexes array
def buildDiffs(sequence_hash, threshold):
    diff_hash = {}
    for key1 in sequence_hash:
        for key2 in sequence_hash:
            if key1 == key2:
                # do nothing - same sequence
                pass
            elif (key1,key2) in diff_hash or (key2,key1) in diff_hash:
                # do nothing - these two sequences have been paired already
                pass
            else:
                diff_hash[(key1,key2)] = getDiffArray(sequence_hash[key1], sequence_hash[key2])

    sorted_keys = sorted(diff_hash, key=lambda tuple: len(diff_hash[tuple]))

    # only print out the matches down to identity threshrold
    for tuple in sorted_keys:
        total = max(len(sequence_hash[tuple[0]]),len(sequence_hash[tuple[1]]))
        match = float(total - len(diff_hash[tuple])) / total
        if match > threshold:
            printDiff(match, tuple[0], tuple[1], sequence_hash[tuple[0]], sequence_hash[tuple[1]], diff_hash[tuple])
        else:
            break

# args are sequences input file and error threshold (0-1 value)
def main():
    if len(sys.argv) < 2:
        print 'please provide the sequence lists file'
        sys.exit()

    print 'input file:', sys.argv[1]

    if len(sys.argv) >= 3:
        threshold = float(sys.argv[2])
        if threshold < 0.0 or threshold > 1.0:
            threshold = 0.0
    else:
        threshold = 0.0

    print 'match threshold: ', threshold

    sequence_hash = {}
    try:
        with open(sys.argv[1], 'rU') as fasta_file:
            for line in fasta_file:   ## iterates over the lines of the file
                if line[0] in (';', '>'):
                    key = line.strip()
                    sequence_hash[key] = ''
                else:
                    sequence_hash[key] += line.strip().rstrip('*')

        buildDiffs(sequence_hash, threshold)

    except Exception as error:
        print "something went wrong... ", error

# this script takes a sequence file and a threshold value
# and outputs the sequences and diffs matches in order
# of best to worst match within the error threshold
if __name__ == '__main__':
    main()
