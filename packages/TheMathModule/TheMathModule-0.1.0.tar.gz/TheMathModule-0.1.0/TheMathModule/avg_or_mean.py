
import pandas as pd


list=df['column'].tolist()



def avg_or_mean(dataframe,col):
    List=dataframe[col].tolist()
    tsum=0
    for n in List:
        tsum=tsum+n
    avg=tsum/len(List)
    return 'The mean is ' + str(avg)


