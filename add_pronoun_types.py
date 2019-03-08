import pandas as pd

female = ['she', 'her', 'hers']
subjective = ['she', 'he']
objective = ['her', 'him']

def gender(row):
    if row['Pronoun'] in female: return 'F'
    else: return 'M'

def pronoun_type(row):
    if row['Pronoun'] in subjective: return 'Subjective'
    elif row['Pronoun'] in objective: return 'Objective'
    else: return 'Possessive'

def add_pronoun_types(gap_df):
    gap_df['Pronoun-gender'] = gap_df.apply(gender, axis=1)
    gap_df['Pronoun-type'] = gap_df.apply(pronoun_type, axis=1)

    return gap_df

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add pronoun gender and type to rows.")
    parser.add_argument('gap_tsv', type=str, help='Path to the GAP tsv file')
    parser.add_argument('outfile', type=str, help='Path to the output csv.')
    args = vars(parser.parse_args())

    gap_df = pd.read_csv(args['gap_tsv'], sep='\t')

    new_df = add_pronoun_types(gap_df)
    new_df.to_csv(args['outfile'], sep='\t')
