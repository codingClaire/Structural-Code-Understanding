import re
import json
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame

def write_data(fname, dic):
    with open(fname, "w", encoding="utf-8") as f:
        for k in dic.keys():
            df_k=dic[k].reset_index(drop=True)
            f.writelines("# " + k)
            df_k.to_markdown(f)
            f.writelines("\n")

if __name__ == '__main__':
    source_list=["title","year","venue","task","model","dataset","pdf","code"]


    print("#" * 10, "Begin", "#" * 10)

    with open("source.md", "r", encoding="UTF-8") as f:
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
    write_data("categories/years.md",year_dic)
    print("Finish sort by years!")
    