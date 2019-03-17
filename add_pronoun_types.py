import pandas as pd

female = ['she', 'her', 'hers']
subjective_pronouns = ['she', 'he']
objective_pronouns = ['her', 'him']
possessive_pronouns = ['her', 'hers', 'his']

def gender(row):
    if row['Pronoun'].lower() in female: return 'F'
    else: return 'M'

def objective(row):
    return row['Pronoun'].lower() in objective_pronouns

def subjective(row):
    return row['Pronoun'].lower() in subjective_pronouns

def possessive(row):
    return row['Pronoun'].lower() in possessive_pronouns

def add_pronoun_types(gap_df):
    gap_df['Pronoun-gender'] = gap_df.apply(gender, axis=1)
    gap_df['Pronoun-Objective'] = gap_df.apply(objective, axis=1)
    gap_df['Pronoun-Subjective'] = gap_df.apply(subjective, axis=1)
    gap_df['Pronoun-Possessive'] = gap_df.apply(possessive, axis=1)

    return gap_df

if __name__=="__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add pronoun gender and type to rows.")
    parser.add_argument('gap_tsv', type=str, help='Path to the GAP tsv file')
    parser.add_argument('outfile', type=str, help='Path to the output csv.')
    args = vars(parser.parse_args())

    gap_df = pd.read_csv(args['gap_tsv'], sep='\t')

    new_df = add_pronoun_types(gap_df)
    new_df.to_csv(args['outfile'], sep='\t', index=False)
