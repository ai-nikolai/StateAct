text="""
=====================
-FINAL RESULTS-LOCAL-deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
---------------------
s=0, N=100
=====================0-actonly
[0.0, 0.5, 0.75, 0.25, 0.5, 1.0, 1.0, 1.0, 1.0, 0.3333333333333333, 1.0, 0.6, 1.0, 1.0, 0.0, 0.25, 1.0, 1.0, 0.5, 0.5, 0.6666666666666666, 1.0, 0.3333333333333333, 1.0, 0.5, 0.6, 0, 0.3333333333333333, 0.1, 1.0, 1.0, 0.75, 0.75, 0.1, 0.25, 0.5, 0.5, 1.0, 0.5, 0.6666666666666666, 1.0, 0.75, 0.0, 1.0, 0.6666666666666666, 1.0, 0.5, 1.0, 1.0, 0.1, 0.5, 1.0, 0.6666666666666666, 1.0, 0.75, 1.0, 1.0, 0.5, 0.6666666666666666, 0.0, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 0.05, 1.0, 0, 0.75, 0.6666666666666666, 0.0, 0, 0.6666666666666666, 1.0, 1.0, 0.5, 0.6666666666666666, 0, 0.75, 0.1, 0.6666666666666666, 0.6666666666666666, 0, 0.6, 1.0, 1.0, 0, 0.3333333333333333, 1.0, 0.25, 1.0, 0.5, 0.6666666666666666, 1.0, 1.0, 0.5, 0.6666666666666666, 1.0, 0.5]
(0.6408333333333331, 0.38, 0.0)
time.struct_time(tm_year=2025, tm_mon=2, tm_mday=12, tm_hour=2, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=43, tm_isdst=0)
time.struct_time(tm_year=2025, tm_mon=2, tm_mday=12, tm_hour=3, tm_min=3, tm_sec=18, tm_wday=2, tm_yday=43, tm_isdst=0)
[5, 4, 5, 4, 4, 6, 6, 5, 6, 5, 5, 6, 4, 5, 5, 5, 6, 6, 5, 4, 4, 5, 5, 6, 6, 5, 15, 12, 5, 4, 4, 5, 5, 6, 5, 5, 6, 4, 5, 5, 6, 4, 4, 6, 5, 4, 5, 6, 4, 4, 4, 6, 5, 5, 5, 5, 5, 5, 6, 6, 5, 5, 5, 6, 4, 6, 4, 5, 15, 5, 5, 5, 15, 4, 5, 6, 4, 4, 15, 6, 5, 5, 8, 15, 6, 6, 5, 15, 4, 6, 4, 5, 6, 4, 5, 4, 9, 5, 4, 5]
5.73
"""

def parse_results(text=None):
    # Extract agent type
    agent_type = text.split('=====================')[2].split('\n')[0].strip()
    
    # Extract model name
    model_name = text.split('-FINAL RESULTS-LOCAL-')[1].split('\n')[0]
    model_name = ''.join(c if c.isalnum() else '_' for c in model_name)
    
    # Extract middle score
    scores = text.split('(')[1].split(')')[0].split(',')
    middle_score = float(scores[1])
    
    return (agent_type, model_name, middle_score)

def write_results_to_csv(folderpath, filename):
    import os
    import csv
    
    results = []
    for file in os.listdir(folderpath):
        if file.endswith('.txt'):
            with open(os.path.join(folderpath, file), 'r') as f:
                text = f.read()
                try:
                    results.append(parse_results(text))
                except:
                    continue
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Agent Type', 'Model Name', 'Middle Score'])
        writer.writerows(results)


if __name__=="__main__":
    write_results_to_csv("./results/v5_16K","v5_16K_full_results.csv")