import pandas as pd

def create_single_match_data(gap_df):
    part1 = gap_df.rename(columns={"A": "Name", "A-offset": "Name-offset", "A-coref": "Coref",
                                   "B": "Other-name", "B-offset": "Other-offset", "B-coref": "Other-coref"})
    part2 = gap_df.rename(columns={"B": "Name", "B-offset": "Name-offset", "B-coref": "Coref",
                                   "A": "Other-name", "A-offset": "Other-offset", "A-coref": "Other-coref"})

    full_df = pd.concat([part1, part2], sort=False)

    return full_df

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Change the GAP coreference data to single matching.")
    parser.add_argument('gap_tsv', type=str, help='Path to the GAP tsv file')
    parser.add_argument('outfile', type=str, help='Path to the output csv.')
    args = vars(parser.parse_args())

    gap_df = pd.read_csv(args['gap_tsv'], sep='\t')

    single_match_df = create_single_match_data(gap_df)
    single_match_df.to_csv(args['outfile'], sep='\t', index=False)
