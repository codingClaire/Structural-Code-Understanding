import re
import json
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

def write_data(fname, dic,del_col):
    with open(fname, "w", encoding="utf-8") as f:
        for k in dic.keys():
            df_k=dic[k].reset_index(drop=True)
            del df_k[del_col]
            if(k=="\n"):
                k="Uncategorized\n"
            f.writelines("# " + k)
            df_k.to_markdown(f)
            f.writelines("\n")

if __name__ == '__main__':
    source_list=["title","year","venue","task","model","dataset","pdf","code"]
    names=['sequence_based_models','graph_based_models']

    print("#" * 10, "Begin", "#" * 10)

    for name in names:
        print("generating "+name+" markdown files!")

        with open(name+".md", "r", encoding="UTF-8") as f:
            content = f.readlines()
        lineno=0
        papers=[]
        # parse paper from source.md
        while(lineno < len(content)):
            if(content[lineno][0:5]=="title"): # target title
                paper=[]
                for offset in range(0,len(source_list)):
                    content[lineno+offset]=content[lineno+offset].strip(source_list[offset]+":")
                    while(content[lineno+offset][0]==' '):
                        content[lineno+offset]=content[lineno+offset].strip(' ')
                    paper.append(content[lineno+offset])
                papers.append(paper)
            lineno+=1
        
        # generate dataframe of total paper
        papers_df=pd.DataFrame(papers,columns=source_list)
        papers_df=papers_df.drop_duplicates(subset=["title"])
        # add pdf and code icon

        papers_df["pdf"]=papers_df["pdf"].map(lambda x: "[📑]("+x[0:-1]+")" if x!="\n" else x)
        papers_df["code"]=papers_df["code"].map(lambda x: "[:octocat:]("+x[0:-1]+")" if x!="\n" else x)
        
        # sort by year
        year_dic=dict(list(papers_df.groupby(papers_df["year"])))
        year_dic=dict(sorted(year_dic.items(),key=lambda item:item[0],reverse=True))
        write_data(name+"/years.md",year_dic,"year")
        print("Finish sort by years!")

        # sort by task
        task_dic=dict(list(papers_df.groupby(papers_df["task"])))
        write_data(name+"/tasks.md",task_dic,"task")
        print("Finish sort by tasks!")

        # sort by model
        #model_dic=dict(list(papers_df.groupby(papers_df["model"])))
        #write_data(name+"/models.md",model_dic,"model")
        #print("Finish sort by models!")

        # sort by dataset
        dataset_dic=dict(list(papers_df.groupby(papers_df["dataset"])))
        write_data(name+"/datasets.md",dataset_dic,"dataset")
        print("Finish sort by datasets!")