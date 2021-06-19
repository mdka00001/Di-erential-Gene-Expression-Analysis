import pandas as pd
import numpy as np
import csv
from scipy import stats

class DEG:
    def __init__(self, path):
        with open(path, "r") as file_handler:
            table=csv.reader(file_handler, delimiter="\t")
            data_str=pd.DataFrame(table)
            columns=data_str.iloc[0]
            data_str=data_str.drop(labels=0, axis=0)
            df=pd.DataFrame()
            for i in range(2,20):
                df[i]=data_str[i].astype(float)
    
    

            df.columns=columns[2:20]
            df_ind=data_str[[0,1]]
            df_ind.columns = ["ProbeID", "Symbol"]
            df_final=pd.concat([df_ind, df], axis=1)
    
    
    
            air_2hr=df_final.iloc[:, [0,1,2,3,4]]
            air_4hr=df_final.iloc[:, [0,1,5,6,7]]
            air_24hr=df_final.iloc[:, [0,1,8,9,10]]
            smoke_2hr=df_final.iloc[:, [0,1,11,12,13]]
            smoke_4hr=df_final.iloc[:, [0,1,14,15,16 ]]
            smoke_24hr=df_final.iloc[:, [0,1,17,18,19]]
            """mean calculation"""
            avg=pd.DataFrame()
            avg["air_mean_2hr"]=air_2hr.mean(axis=1)
            avg["air_mean_4hr"]=air_4hr.mean(axis=1)
            avg["air_mean_24hr"]=air_24hr.mean(axis=1)
            avg["smoke_mean_2hr"]=smoke_2hr.mean(axis=1)
            avg["smoke_mean_4hr"]=smoke_4hr.mean(axis=1)
            avg["smoke_mean_24hr"]=smoke_24hr.mean(axis=1)
            """var calculation"""
            avg["air_var_2hr"]=air_2hr.var(axis=1)
            avg["air_var_4hr"]=air_4hr.var(axis=1)  
            avg["air_var_24hr"]=air_24hr.var(axis=1)
            avg["smoke_var_2hr"]=smoke_2hr.var(axis=1)
            avg["smoke_var_4hr"]=smoke_4hr.var(axis=1)
            avg["smoke_var_24hr"]=smoke_24hr.var(axis=1)
            
            """log fold change"""
            avg["log_fold_change_2hr"] = np.log2(avg["smoke_mean_2hr"]/avg["air_mean_2hr"])
            avg["log_fold_change_4hr"] = np.log2(avg["smoke_mean_4hr"]/avg["air_mean_4hr"])
            avg["log_fold_change_24hr"] = np.log2(avg["smoke_mean_24hr"]/avg["air_mean_24hr"])
            avg=pd.concat([df_ind[["ProbeID","Symbol"]], avg], axis=1)

            """t-test"""
            
            
            tts1=[]
            tts2=[]
            tts3=[]
            for index, rows in df_final.iterrows():
                
                air_2h=[rows.Air_2h_A, rows.Air_2h_B, rows.Air_2h_C]
                smoke_2h=[rows.Smoke_2h_A, rows.Smoke_2h_B, rows.Smoke_2h_C]
                test1=stats.ttest_ind(air_2h, smoke_2h, equal_var=True)
                tts1.append(test1)

                air_4h=[rows.Air_4h_A, rows.Air_4h_B, rows.Air_4h_C]
                smoke_4h=[rows.Smoke_4h_A, rows.Smoke_4h_B, rows.Smoke_4h_C]
                test2=stats.ttest_ind(air_4h, smoke_4h, equal_var=True)
                tts2.append(test2)

                air_24h=[rows.Air_24h_A, rows.Air_24h_B, rows.Air_24h_C]
                smoke_24h=[rows.Smoke_24h_A, rows.Smoke_24h_B, rows.Smoke_24h_C]
                test3=stats.ttest_ind(air_24h, smoke_24h, equal_var=True)
                tts3.append(test3)

                
                
            pval_2=pd.DataFrame(tts1)
            pval_2.columns=["statistics", "pval_2hr"]
            pval_4=pd.DataFrame(tts2)
            pval_4.columns=["statistics", "pval_4hr"]
            pval_24=pd.DataFrame(tts3)
            pval_24.columns=["statistics", "pval_24hr"]

            avg.reset_index(inplace=True)
            avg_final=pd.concat([avg, pval_2["pval_2hr"], pval_4["pval_4hr"], pval_24["pval_24hr"]], axis=1)

            """bonferonni"""

            p_adj_2h=[]

            for i in pval_2["pval_2hr"]:
                bon=[1]
                bon.append(i*len(pval_2["pval_2hr"]))
                min_val=min(bon)
                p_adj_2h.append(min_val) 
           
            p_adj_4h=[]

            for i in pval_4["pval_4hr"]:
                bon=[1]
                bon.append(i*len(pval_4["pval_4hr"]))
                min_val=min(bon)
                p_adj_4h.append(min_val)  

            p_adj_24h=[]

            for i in pval_24["pval_24hr"]:
                bon=[1]
                bon.append(i*len(pval_24["pval_24hr"]))
                min_val=min(bon)
                p_adj_24h.append(min_val) 
            
            p_adj_2h_df=pd.DataFrame(p_adj_2h)
            p_adj_2h_df.columns=["p_adj_2hr"]
            p_adj_4h_df=pd.DataFrame(p_adj_4h)
            p_adj_4h_df.columns=["p_adj_4hr"]
            p_adj_24h_df=pd.DataFrame(p_adj_24h)
            p_adj_24h_df.columns=["p_adj_24hr"]

            avg_final=pd.concat([avg_final, p_adj_2h_df["p_adj_2hr"], p_adj_4h_df["p_adj_4hr"], p_adj_24h_df["p_adj_24hr"]], axis=1)

            
            #cols=[]

            #for col in avg_final:
                #cols.append(col)
            #print(cols)


            t_2h=avg_final[["ProbeID", 'Symbol', 'log_fold_change_2hr', 'pval_2hr', 'p_adj_2hr']]
            t_2h.columns=["ProbeID", 'Symbol', 'log_fold_change', 'pval', 'p_adj']
            t_2h_final=t_2h.sort_values(by=['p_adj'], ascending=True)
            t_2_10=t_2h_final.head(10)

            t_4h=avg_final[["ProbeID", 'Symbol', 'log_fold_change_4hr', 'pval_4hr', 'p_adj_4hr']]
            t_4h.columns=["ProbeID", 'Symbol', 'log_fold_change', 'pval', 'p_adj']
            t_4h_final=t_4h.sort_values(by=['p_adj'], ascending=True)
            t_4_10=t_4h_final.head(10)

            t_24h=avg_final[["ProbeID", 'Symbol', 'log_fold_change_24hr', 'pval_24hr', 'p_adj_24hr']]
            t_24h.columns=["ProbeID", 'Symbol', 'log_fold_change', 'pval', 'p_adj']
            t_24h_final=t_24h.sort_values(by=['p_adj'], ascending=True)
            t_24_10=t_24h_final.head(10)

            t_2_10.to_csv("t_2h_final.tsv",sep="\t")
            t_4_10.to_csv("t_4h_final.tsv",sep="\t")
            t_24_10.to_csv("t_24h_final.tsv",sep="\t")



            
            


            


            


            
