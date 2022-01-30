import re
import json
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame


def write_data(fname, dic, del_col):
    with open(fname, "w", encoding="utf-8") as f:
        for k in dic.keys():
            df_k = dic[k].reset_index(drop=True)
            del df_k[del_col]
            if k == "\n":
                k = "Uncategorized\n"
            f.writelines("# " + k)
            df_k.to_markdown(f)
            f.writelines("\n")


if __name__ == "__main__":
    source_list = ["title", "year", "venue",
                   "task", "model", "dataset", "pdf", "code"]
    names = ['sequence_based_models', 'graph_based_models']
    #names = ["graph_based_models"]
    print("#" * 10, "Begin", "#" * 10)

    statistic_dic = {
        names[0]: {
            "years": {},
            "tasks": {},
            "datasets": {},
            "models": {},
        },
        names[1]: {
            "years": {},
            "tasks": {},
            "datasets": {},
            "models": {},
        },
    }

    for name in names:
        print("generating " + name + " markdown files!")

        with open(name + ".md", "r", encoding="UTF-8") as f:
            content = f.readlines()
        lineno = 0
        papers = []
        # parse paper from source.md
        while lineno < len(content):
            if content[lineno][0:5] == "title":  # target title
                paper = []
                for offset in range(0, len(source_list)):
                    content[lineno + offset] = content[lineno + offset].strip(
                        source_list[offset] + ":"
                    )
                    while content[lineno + offset][0] == " ":
                        content[lineno + offset] = content[lineno +
                                                           offset].strip(" ")
                    paper.append(content[lineno + offset])
                papers.append(paper)
            lineno += 1

        # generate dataframe of total paper
        papers_df = pd.DataFrame(papers, columns=source_list)
        papers_df = papers_df.drop_duplicates(subset=["title"])
        # add pdf and code icon

        papers_df["pdf"] = papers_df["pdf"].map(
            lambda x: "[📑](" + x[0:-1] + ")" if x != "\n" else x
        )
        papers_df["code"] = papers_df["code"].map(
            lambda x: "[:octocat:](" + x[0:-1] + ")" if x != "\n" else x
        )

        # sort by year
        year_dic = dict(list(papers_df.groupby(papers_df["year"])))
        year_dic = dict(
            sorted(year_dic.items(), key=lambda item: item[0], reverse=True))
        write_data(name+"/years.md", year_dic, "year")
        for k in year_dic.keys():
            statistic_dic[name]["years"][k] = year_dic[k].shape[0]
        print("Finish sort by years!")

        ############ sort by task ############
        total_tasks = []
        task_dic = {}
        for task_str in list(papers_df["task"]):
            sublist = task_str.split(",")
            for element in range(len(sublist)):
                while(sublist[element][0] == ' '):
                    sublist[element] = sublist[element][1:]
                if(sublist[element][-1] != '\n'):
                    sublist[element] = sublist[element]+'\n'
            total_tasks.extend(sublist)

        total_tasks = list(set(total_tasks))
        for task in total_tasks:
            bool = papers_df["task"].str.contains(task[0:-1])
            tasks_df = papers_df[bool]
            task_dic[task] = tasks_df
        write_data(name + "/tasks.md", task_dic, "task")
        for k in task_dic.keys():
            statistic_dic[name]["tasks"][k] = task_dic[k].shape[0]
        print("Finish sort by tasks!")

        ############ sort by dataset ############
        total_datasets = []
        dataset_dic = {}
        for dataset_str in list(papers_df["dataset"]):
            sublist = dataset_str.split(",")
            for element in range(len(sublist)):
                while(sublist[element][0] == ' '):
                    sublist[element] = sublist[element][1:]
                if(sublist[element][-1] != '\n'):
                    sublist[element] = sublist[element]+'\n'
            total_datasets.extend(sublist)
        total_datasets = list(set(total_datasets))
        print(total_datasets)
        for dataset in total_datasets:
            print(dataset[0:-1])
            bool = papers_df["dataset"].str.contains(dataset[0:-1])
            datasets_df = papers_df[bool]
            dataset_dic[dataset] = datasets_df

        write_data(name + "/datasets.md", dataset_dic, "dataset")
        for k in dataset_dic.keys():
            statistic_dic[name]["datasets"][k] = dataset_dic[k].shape[0]
        print("Finish sort by datasets!")

        ############ sort by model ############
        total_models = []
        model_dic = {}
        for model_str in list(papers_df["model"]):
            sublist = model_str.split(",")
            for element in range(len(sublist)):
                while(sublist[element][0] == ' '):
                    sublist[element] = sublist[element][1:]
                if(sublist[element][-1] != '\n'):
                    sublist[element] = sublist[element]+'\n'
            total_models.extend(sublist)
        total_models = list(set(total_models))
        for model in total_models:
            bool = papers_df["model"].str.contains(model[0:-1])
            models_df = papers_df[bool]
            model_dic[model] = models_df
        write_data(name + "/models.md", model_dic, "model")
        for k in model_dic.keys():
            statistic_dic[name]["models"][k] = model_dic[k].shape[0]
        print("Finish sort by models!")

    # Write markdown files
    with open("README.md", "w", encoding="utf-8") as f:
        categories = ["years", "tasks", "datasets", "models"]
        f.writelines("# Code Understanding Literatures in Deep Learning\n")
        f.writelines("## Sequence-based Models\n")
        for category in categories:
            f.writelines(
                "### [By "+category+"](sequence_based_models/"+category+".md)\n")
            for k in statistic_dic[names[0]][category].keys():
                num = str(statistic_dic[names[0]][category][k])
                k = "Uncategorized\n" if k == "\n" else k
                f.writelines(
                    "- " + k[0:-1] + ":" + num + " paper(s)\n"
                )
        f.writelines("## Graph-based Models\n")
        for category in categories:
            f.writelines(
                "### [By "+category+"](graph_based_models/"+category+".md)\n")
            for k in statistic_dic[names[1]][category].keys():
                num = str(statistic_dic[names[1]][category][k])
                k = "Uncategorized\n" if k == "\n" else k
                f.writelines(
                    "- " + k[0:-1] + ":" + num + " paper(s)\n"
                )
