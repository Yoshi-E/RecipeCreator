import re
import pandas as pd
from gensim import models
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
from NLP import *
import os

#insipired by https://www.meganstodel.com/posts/callbacks/

def find_doc_convergence(topic_num, iteration, log):
    # Regex to bookend log for iteration - choose last occurrence
    end_slice = re.compile(f".*(End of model: {iteration} iterations)")
    end_matches = [end_slice.findall(l) for l in open(log)]
    iteration_end = [i for i, x in enumerate(end_matches) if x]
    if iteration_end:
        iteration_end = iteration_end[-1]
    else:
        iteration_end = 999999999
    start_slice = re.compile(f".*(Start of model: {iteration} iterations)")
    start_matches = [start_slice.findall(l) for l in open(log)]
    start_options = [i for i, x in enumerate(start_matches) if x]
    start_options = [item for item in start_options if item < iteration_end]
    iteration_start = max(start_options)
    iteration_bookends = [iteration_start, iteration_end]
    # Regex to find documents converged figures
    p = re.compile(f".*?\s:\s(\d+)\/\d+.*{iteration}\siteration")
    matches = [p.findall(l) for l in open(log)]
    matches = matches[iteration_bookends[0]:iteration_bookends[1]]
    matches = [m for m in matches if len(m) > 0]
    # Unlist internal lists and turn into numbers
    matches = [m for sublist in matches for m in sublist]
    matches = [float(m) for m in matches]
    return (matches)


def analyseLog(iterations, DIR, MODEL):
    #iterations = [100]

    all_metrics = pd.DataFrame()
    #DIR = "lda_100i50p_Z/"
    #MODEL = "lda_100i50p.model"
    for iteration in tqdm(iterations):
        model = models.ldamodel.LdaModel.load(DIR+MODEL)
        df = pd.DataFrame.from_dict(model.metrics)
        if os.path.exists(DIR+"model_callbacks.log"):
            z = find_doc_convergence(5, iteration, DIR+"model_callbacks.log")
        else:
            z = find_doc_convergence(5, iteration, "model_callbacks.log")
        print(df)
        print("##", len(z), len(df))
        step = int(math.floor(len(z)/len(df)))
        print(step)
        z = z[::step]
        df['docs_converged'] = z[:len(df)]
        df['iterations'] = iteration
        df['topics'] = 5

        df = df.reset_index().rename(columns={'index': 'pass_num'})

        all_metrics = pd.concat([all_metrics, df])

    for metric in ['Coherence', 'Perplexity', 'Convergence', 'docs_converged']:
    
        fig, axs = plt.subplots(1, 1, figsize=(20, 7))
        # Each plot to show results for all models with the same topic number
        for i, topic_number in enumerate([5]):
            filtered_topics = all_metrics[all_metrics['topics'] == topic_number]
            for label, df in filtered_topics.groupby(['iterations']):
                #print(label)
                df.plot(x='pass_num', y=metric, ax=axs, label=label)

            axs.set_xlabel(f"Pass number")
            axs.legend()
            axs.set_ylim([all_metrics[metric].min() * 0.9, all_metrics[metric].max() * 1.1])
        
        if metric == 'docs_converged':
            fig.suptitle('Documents converged', fontsize=20)
        else:
            fig.suptitle(metric, fontsize=20)
        
        fig.savefig(f'{DIR}lda_{metric}.png', dpi=200) 

if __name__ == "__main__":
    analyseLog(iterations=[100], DIR="lda_100i50p_Z/", MODEL="lda_100i50p.model")