import re


def run_first_task(lines: list[str]):
    # TODO: pass whole source file instead of list of lines
    counter = 0
    pairs = lines[:lines.index("")]
    sequences = lines[lines.index("") + 1 :]

    for seq in sequences[:1]:
        print("\nsequence:", seq,"\n")
        # find all the pairs that include any of the numbers in seq
        # go through the relevant pairs and check with regex if the order is correct
            # continue if not, find middle item otherwise
        numbers = [int(x) for x in seq.split(",")]
        valid = True

        for item in numbers:
            relevant_pairs = [pair for pair in pairs if str(item) in pair]
            print("item:",item,"pairs",relevant_pairs)
            for p in relevant_pairs:
                first, second = [n for n in p.split("|")]
                print(first, second )
                # match = re.search(rf"{first}.*{second}", seq)
                # print('match',match)
        #         if match is None:
        #             print('NINCS MECS')
        #             valid = False
        #             break

        # if valid:        
        #     middle = seq.split(",")[len(seq.split(",")) / 2]
        #     print(middle)
        #     # counter += 
