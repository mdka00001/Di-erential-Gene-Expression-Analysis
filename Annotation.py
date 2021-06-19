import pandas as pd
import csv
import operator
import math
from scipy.stats import hypergeom
class Annotation:
    def __init__(self, path):
        with open(path, 'r') as handle:
            table=csv.reader(handle, delimiter="\t")
            df=pd.DataFrame(table)
            data=df.iloc[12:,]
            data.reset_index(inplace=True)
            new_data=data.drop(columns="index")
            
            filter_data=new_data[new_data[0]=="UniProtKB"]
            filter_data2=filter_data[filter_data[8]=="P"]
            self.uniprot_df=filter_data2[[0,1,2,4,8]]
            self.uniprot_df.columns=["Database", "Accession", "Gene/Protein", "GO_identifier", "Annotation"]
            
    def association(self, path):
        with open(path, "r") as handle2:
            table2=csv.reader(handle2, delimiter="\t")
            df2=pd.DataFrame(table2)
            new_header=df2.iloc[0]
            df2=df2[1:]
            df2.columns=new_header
            df2["p_adj"]=df2["p_adj"].astype(float)
            df3 =df2[df2["p_adj"] < 0.05]
            
            asso_2hr=pd.DataFrame()


            for i in df3["Symbol"]:
                asso_2hr_2=self.uniprot_df[self.uniprot_df["Gene/Protein"]==i]
                asso_2hr=pd.concat([asso_2hr, asso_2hr_2], axis=0)
            
            
            


            

            word=asso_2hr["GO_identifier"].to_numpy()  
            frequency={}

            for i in word:
                if i in frequency:
                    frequency[i] += 1
                else:
                    frequency[i] = 1
            mx = max(frequency.items(), key=operator.itemgetter(1))[0]
            mn = min(frequency.items(), key=operator.itemgetter(1))[0]
            
           
            most_common=asso_2hr.loc[asso_2hr["GO_identifier"]==mx]
            least_common=asso_2hr.loc[asso_2hr["GO_identifier"]==mn]

            most_common.to_csv("most_common_24h.tsv", sep="\t")

            
            

            """number of genes in main database N"""
            gene_main=self.uniprot_df["Gene/Protein"].to_numpy()
            gene_freq={}
            for i in gene_main:
                if i in gene_freq:
                    gene_freq[i]+=1
                else:
                    gene_freq[i]=1

            """number of genes in test database n"""
            gene_main1=asso_2hr["Gene/Protein"].to_numpy()
            gene_freq1={}
            for i in gene_main1:
                if i in gene_freq1:
                    gene_freq1[i]+=1
                else:
                    gene_freq1[i]=1
            
            #N_comb_n=math.comb(len(gene_freq), len(gene_freq1))


            p=[]

            go=[]

            go_main=self.uniprot_df["GO_identifier"].to_numpy()
            go_test=asso_2hr["GO_identifier"].to_numpy()
            for i in go_test:
                m_df=self.uniprot_df[self.uniprot_df["GO_identifier"]==i]
                k_df=asso_2hr[asso_2hr["GO_identifier"]==i]
                m_df2=m_df["Gene/Protein"].to_numpy()
                k_df2=k_df["Gene/Protein"].to_numpy()
                m={}
                k={}
                go.append(i)
                for j in m_df2:
                    if j in m:
                        m[j] += 1
                    else:
                        m[j] = 1
                for l in k_df2:
                    if l in k:
                        k[l] += 1
                    else:
                        k[l] = 1
                 
                #m_comb_k=math.comb((len(m), len(k)))
                N_m=len(gene_freq)-len(m)
                n_k=len(gene_freq1)-len(k)
                #Nm_comb_nk=math.comb(N_m, n_k)
                val=hypergeom.pmf(len(k), len(gene_freq), len(m), len(gene_freq1), loc=0)
                p.append(val)
            
            go_p1=pd.DataFrame(go)
            go_p2=pd.DataFrame(p)
            go_p=pd.concat([go_p1, go_p2], axis=1)
            go_p.columns=["GO_annotation", "P_val"]



            p_adj=[]

            for i in go_p["P_val"]:
                bon=[1]
                bon.append(i*len(go_p["P_val"]))
                min_val=min(bon)
                p_adj.append(min_val)
            p_adj_df=pd.DataFrame(p_adj)
            p_adj_df.columns=["Adj_p"]

            go_p=pd.concat([go_p, p_adj_df], axis=1)
            go_final=go_p.sort_values(by=['Adj_p'], ascending=True)
            go_final2=go_final.head(20)
            go_final2.to_csv("t_24_hyper.tsv",sep="\t")
            freq=pd.DataFrame.from_dict(frequency, orient='index')

            freq.to_csv("GO_freq_24.tsv", sep="\t")


