import pandas as pd
import numpy as np
import pickle

def get_data():
    df = pd.read_excel('data/training_attribute.xlsx')
    #just using Fat Tire data
    df['base beer'] = df['base beer'].str.lower()
    df = df[df['base beer']=='fat tire']
    df['Flavor'] = df['Flavor'].str.lower()
    df['relational attributes'] = df['relational attributes'].str.lower()
    df['Full Name'] = df['Full Name'].str.lower()
    df['Full Name'] = df['Full Name'].replace('billy bletcher','bill bletcher')
    df['Full Name'] = df['Full Name'].replace('matty gilliland','matt gilliland')
    df['Full Name'] = df['Full Name'].replace('philip pollick','phil pollick')
    return df

def get_names_list():
    with open('data/names_list2.pickle', 'rb') as handle:
        names_used_list = pickle.load(handle)
    return names_used_list

def score_training(df,names_used_list):
    flav_count = df.groupby('Flavor')['format'].count()
    flav_count = pd.DataFrame(flav_count)
    #trimming to more than 1200 trainings.
    flav_count = flav_count[flav_count['format']>1200]
    flav_list = np.array(flav_count.index.tolist())
    col_list = ["name"]
    wrong_dict = np.empty_like(names_used_list)
    stacked = names_used_list.copy()

    for flav in flav_list:
        num_right_array = np.empty_like(names_used_list)
        pos_right_array = np.empty_like(names_used_list)
        col_list.append("{}_right".format(str(flav)))
        col_list.append("{}_poss".format(str(flav)))
        for i,name in enumerate(names_used_list):
            temp = df.loc[(df['Full Name']== name) & (df['Flavor']==flav)]
            num_right_array[i] = temp[temp['correct']==1].shape[0]
            pos_right_array[i] = temp.shape[0]
            if num_right_array[i] != pos_right_array[i]:
                if wrong_dict[i]==None:
                    wrong_dict[i] ={flav:list(temp.loc[temp['Incorrect']==1,'relational attributes'])}
                else:
                    wrong_dict[i][flav] = list(temp.loc[temp['Incorrect']==1,'relational attributes'])
        stacked = np.column_stack((stacked,num_right_array,pos_right_array))
    col_list.append('wrong_dict')
    stacked = np.column_stack((stacked,wrong_dict))
    new_df = pd.DataFrame(stacked,columns=col_list)
    return new_df

if __name__ == '__main__':
    df = get_data()
    names_used_list = get_names_list()
    dfs = score_training(df,names_used_list)
    #temp = df.loc[(df['Full Name']== names_used_list[0]) & (df['Flavor']=='dms')]
    #a.extend(temp.loc[temp['Incorrect']==1,'relational attributes'])