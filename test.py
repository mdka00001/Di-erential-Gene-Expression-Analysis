from Annotation import Annotation

a=Annotation(r"D:\BIII\Assignment_5\supplement_assignment5\ex2\human_GO.gaf")

b=Annotation.association(a, r"D:\BIII\Assignment_5\supplement_assignment5\ex2\t_24h_final.tsv")


print(b)