import pandas as pd

def create_single_match_data(gap_df):
    a_only = gap_df.drop(["B", "B-offset", "B-coref"], axis=1)
    part1 = a_only.rename(columns={"A": "Name", "A-offset": "Name-offset", "A-coref": "Coref"})
    b_only = gap_df.drop(["A", "A-offset", "A-coref"], axis=1)
    part2 = b_only.rename(columns={"B": "Name", "B-offset": "Name-offset", "B-coref": "Coref"})
    full_df = pd.concat([part1, part2])

    return full_df

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Change the GAP coreference data to single matching.")
    parser.add_argument('gap_tsv', type=str, help='Path to the GAP tsv file')
    parser.add_argument('outfile', type=str, help='Path to the output csv.')
    args = vars(parser.parse_args())

    gap_df = pd.read_csv(args['gap_tsv'], sep='\t')

    single_match_df = create_single_match_data(gap_df)
    single_match_df.to_csv(args['outfile'], sep='\t')
