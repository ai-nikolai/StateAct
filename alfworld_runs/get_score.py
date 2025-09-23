import pandas as pd
import argparse

def load_results(trial_name):
    file_path = f'game_logs/alfworld_eval_{trial_name}/alfworld_results.csv'
    df = pd.read_csv(file_path)
    return df

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--trial_name', type=str, required=True, help='Name of the trial')
    args = parser.parse_args()
    df = load_results(args.trial_name)

    df = df.astype({"success":int})
    overall_score = df["success"].mean()
    num_items = df["success"].count()
    num_successful = df["success"].sum()

    print(f"Overall (mean) Score: {overall_score:.6f} with {num_successful} successful env and a total of {num_items} envs.")





    






