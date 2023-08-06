## 25th May, 2023
# 10th May, 2023

## Utility functions


import pandas as pd
import numpy as np
import itertools
from scipy.stats import kurtosis
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
import pickle
import os, glob,gc
import pathlib
import string
import matplotlib.pyplot as plt


# Given a list of categorical columns, this
#  function creates all possible combinations
#   of supplied columns(pair of two) and then
#    it creates new columns as concatenation of each pair.
#   Example; cat_cols = [var1,var2,var3]
#    Columns created in dataset: [var1_var2,var1_var3,var2_var3]
#     Existing columns remain as they are

def create_cat_pairwise_cols(df, cat_cols):
    """
    Given a dataframe, df, and a list of categorical
    columns (cat_cols), this function creates all
    combinations (not permutations) of supplied columns in pair
    of two). It then creates new columns in 'df' as
    concatenation of each pair. The resulting dataframe is
    returned.
    Example; cat_cols = [var1,var2,var3]
    Columns created in df: [var1_p_var2,var1_p_var3,var2_p_var3].
    Existing columns continue to remain as they are.
    """
    x = itertools.combinations(cat_cols, 2)
    for i in x:
        # Differentiate permuted column names from names
        #  created as colToProject+"_+intermediaryCol
        t = i[0] + "_p_" + i[1]   # New column name
        df[t]= df[i[0]].astype(str) + "_" + df[i[1]].astype(str)
    return df


def interaction_cols(train, cat_cols, interactingCols, interaction = False):
    new_cols = None
    if (interaction ):
        # All columns including float/int etc
        current_train_columns = train.columns
        # 6.1 Create new columns (combinations of cat columns) in train
        train = create_cat_pairwise_cols(train , interactingCols)
        # 6.12 New columns created. These columns must be latter dropped
        new_cols = list(set(train.columns).difference(set(current_train_columns)))
        # 6.13 Revised cat cols (ie excluding hour etc)
    return train, new_cols


# Permute column names in a colList two at a time
def permute_colList(colNamesList,cMeasures, n=2):
    """
    Given a list of columnnames (colNamesList), the
    function creates tuples after permuting column names.
    PErmutation can either be 2 or 3 at a time.
    cMeasures is a list. See network_features.calCentralityMeasures()
    to learn about elements of cMeasures.
    Example: colNamesList = ["C1", "C2", "C3"]
    Return list is: [("C1", "C2", cMeasures),("C2", "C1", cMeasures),...]
    """
    # Permute 2 at a time
    pc = list(itertools.permutations(colNamesList,n))
    nl = []
    for i in pc:
        # Get back names
        colToProject = i[0]
        if n == 2:
            intermediaryCol = i[1]
            # Create a tuple. Add elements True and False
            # True: Calculate centrality measures
            # False: No clustering
            e = (colToProject,intermediaryCol, cMeasures)
        if n == 3:
            intermediaryCol1 = i[1]
            intermediaryCol2 = i[2]
            e = (colToProject,intermediaryCol1, intermediaryCol2,cMeasures)
        if n >3:
            print("Not possible")

        nl.append(e)
    return nl




# For a particular column, vary threshold percentage to check
#  how many levels remain
def ulevelsPerThreshold(df,colName, threshold_list = [0.00001, 0.0001, 0.0002, 0.001, 0.01, 0.1, 0.15, 0.2]):
    """
    Let total normalized value_counts in df[colName] be 100. Then, if in df[colName] one were to merge all levels whose
    'counts' fall below a threshold then how many levels and their corresponding counts would be left.
    'threshold_list' is a list of percentage values
    """
    unique_levels = []
    # Normalize value counts to 100
    series = df[colName].value_counts()
    series = (series/series.sum()) * 100
    # At percentage 0, level count distribution is as below
    unique_levels.append((0,df[colName].nunique()))
    # For every percentage level i
    for i in threshold_list:
        # Get a series that replaces by False, value_counts below threshold
        #  ie rest above the threshold are True
        uc = (~(series < i))
        # So how many are above threshold + 1 (for merged level)
        uc= uc.sum() + 1
        unique_levels.append((i,uc))
        t = pd.DataFrame.from_records(unique_levels, columns = ['apply %threshold', 'remaining_levels'])
    return t



# Amended on 6th March, 2023
# Called in average_out_models ver 1.py and in
#    average_out_models ver 1.py and in
def levelsTransformer(df, feature, thresholdValue_count, mapdictpath, action = False):
    """
    Calls: load_dict_from_file(), mergeRareLevels(), save_dict_to_file()
    Called by: Application

    Parameters
    ---------
    df: Dataframe under consideration
    feature: Column whose levels are to be reduced
    thresholdValue_count: If integer, keep only those levels whose value_count
                          exceeds this number. If float, keep only those levels
                          whose percentages are above this value.
    mapdictpath : Dictionary which stores mapping between existing levels
                  and new levels.
    action: The value determines how an integer thresholdValue_count will be 
            interpreted: Either permit those levels whose value_counts() exceed
            this value (action = False) or set max number of unique levels
            to this value (action = True).
    Usage
    -----
    X =  utils.levelsTransformer(X, 'ip',mergethreshold, mapdictpath, action)
    Returns
    ------
    Returns DataFrame with reduced levels for 'feature' column
    """
    # Does this file exist:
    filename = "mapLevelsDict" + "_" + feature +".pkl"
    # If yes read mapping dictinary
    if os.path.exists(mapdictpath+filename):
        #mapdict = load_dict_from_file("mapLevelsDict_device.pkl", mapdictpath)
        mapdict = load_dict_from_file(filename, mapdictpath)
        print("Existing saved dictionary loaded")
    else:
        print("No saved dictionary exists as yet.")
        mapdict = None

    df, mapdict = mergeRareLevels(df,feature, thresholdValue_count, mapdict,'99999' ,  action)

    #if isinstance(thresholdValue_count, int):
        # Update mapping dictionary
    #    df, mapdict = mergeRareLevels(df,feature, thresholdValue_count, mapdict)
    #else:
        # thresholdValue_count is float
    #    df, mapdict = mergeLevels(df,feature, mapdict, thresholdValue_count)

    # Save updated dictionary
    save_dict_to_file(mapdict, filename, mapdictpath)
    return df


# Amended on 6th March, 2023
def mergeRareLevels(df,colName, occurrenceThreshold, model = None, replace_by = '99999', action= False):
    """
    Called by: levelsTransformer()
    Parameters
    ---------
    df: DataFrame
    colName: Columns whose levels are to be examined for rareness
    occurrenceThreshold: This decides if a level is rare and be merged
    model: Mapping of actual levels with merged lavels
    replace_by:  Level names of merged levels
    action: The value determines how an integer occurrenceThreshold will be 
            interpreted: Either permit those levels whose value_counts() exceed
            this value (action = False) or set max number of unique levels
            to this value (action = True).
    Desc
    ----
    A model is a dictionary where 'key' is old_level
    name and value is the new level name ('99999').
    For a level which has high occurrenceThreshold,
    both 'key' and 'value' would be same. If no earlier
    model exist:
        In df[colName] merge all those level-names
        by 'replace_by' whose total count is less
        than or equal to occurrenceThreshold. A
        new model created and returned.
    If a model already exists:
        the model (dict) is updated only to the extent
        of new key. if an existing key in the existing
        model now is to get a new value, that updation
        is NOT carried out.
    Returns
    -------
    model and dataframe modified as per the model.
    """
    # See code examples at the end of this module
    # Get present value_counts of each level
    series = df[colName].value_counts()
    if isinstance(occurrenceThreshold, int):
        if not action:
            # Is any value_count greater than occurrenceThreshold
            cond = series > occurrenceThreshold
        else:
            # Limit number of unique levels to occurrenceThreshold
            series[:occurrenceThreshold] = True
            series[occurrenceThreshold:] = False
            cond = series
    else:
        # occurrenceThreshold is a percentage value
        #  ie occurrenceThreshold%
        cond = ((series/series.sum()) * 100) > occurrenceThreshold
    # Now, get revised replacement values.
    remapped_levels = np.where(cond, series.index, replace_by)
    # Create a dictionary of what is to be replaced with what
    # This will also serve as model for future data
    currentmodel = {i:j for i, j in zip(series.index,remapped_levels)}

    if model is not None:
        # Revise the model as per current. Include new keys only
        #  Let earlier key-value pairs remain as they are:
            
        # First get those model.keys() whose value is not replace_by
        p_keys = []
        for i in model.keys():
            val = model[i]
            if val != replace_by:
                # The value of this key will not be replaced by replace_by
                p_keys.append(i)
               
        #newkeys = set(currentmodel.keys()) - set(model.keys())
        # p_keys were above threshold level in earlier cases
        #  so no need to modify them
        newkeys = set(currentmodel.keys()) - set(p_keys)
        for keys in newkeys:
            model[keys] = currentmodel[keys]
        modelToApply = model
    else:
        modelToApply = currentmodel

    # The following code is very slow
    #df[colName] = df[colName].replace(model)
    # This one using map() is fast
    # https://stackoverflow.com/a/41987136
    df[colName] = df[colName].map(modelToApply.get)
    return df, modelToApply


## Out dated; 7th Dec, 2022
# This function is to be corrected. See mergeRareLevels function.
# Refer: https://stackoverflow.com/a/47418479
# https://milos.ai/2019/01/merging-categories-with-small-frequencies
# Merge all those levels  whose overall percentage occurrence is below a threshold
def mergeLevels(df, colName, mapdict = None, percent_threshold=0.001, replace_by = '99999'):
    """
    in df[colName], merge all those those levels whose overall percentage occurrence is below a percent_threshold
    """
    if mapdict is not None:
        # Replace values as per dictionary
        # The following code is very slow
        # df[colName] = df[colName].replace(model)
        # This one using map() is fast
        # https://stackoverflow.com/a/41987136
        # Get present dictionary.
        d = dict(zip(df[colName],df[colName]))
        # Update it using mapdict
        d.update(mapdict)
        # Perform transformation in df[colName]
        df[colName] = df[colName].map(d.get)
        # This is our existing model
        mapdict = d

    # Generate a pandas series of value counts
    vc_series = pd.value_counts(df[colName])
    # Divide each value_count() by total sum and set to True
    #  all those value_counts() whose percentage is below 'percent_threshold'
    mask = ((vc_series/vc_series.sum()) * 100).lt(percent_threshold)
    # This will be new column name with merged levels
    newColName = colName + "_updated"
    df[newColName] = np.where(df[colName].isin(vc_series[mask].index), replace_by , df[colName])

    if mapdict is not None:
        # Compare df[colName] and df[newColName] to create a dictionary for mappimg
        currentmapdict = dict(zip(df[colName],df[newColName]))
        mapdict.update(currentmapdict)
    else:
        mapdict = dict(zip(df[colName],df[newColName]))

    # Drop the feature from df
    _ =  df.pop(colName)
    # Rename newColName back to colName
    df.rename(columns = {newColName : colName}, inplace = True)
    # 4.3 Replace 'Others' by 999 and change data type
    #train = utils.replace_Others_by_999(train,'ip', 'uint32')
    #utils.save_dict_to_file(mapdict, "mapLevelsDict_ip.pkl", mapdictpath)
    return df, mapdict





# Count number of unique levels for every feature in df
def uniqueLevelsCount(df, colList = None):
    """
    # Count number of unique levels for every feature in colList of
    # dataframe, df. If colList is not supplied, all columns of df
    # are considered
    """

    if colList is None:
        colList = df.columns.tolist()

    feature_count = []
    for i in colList:
        #print(i, ':', len(train[i].astype(str).value_counts()))
        feature_count.append((i,df[i].nunique()))
    # https://stackoverflow.com/a/10695161
    t = sorted(feature_count, key=lambda x: x[1], reverse=True)
    t = pd.DataFrame.from_records(t, columns = ['feature', 'NoOfLevels'])
    return t





def uLevelsCountBeyondOT(df,colName,occurrenceThreshold=[0,1,2,3,4,5,6]):
    """
    For df[colName], how many unique levels will be left, if one were
    to merge all levels that occur less than 'occurrenceThreshold' times.
    The function will not merge levels.
    """
    series = df[colName].value_counts()
    unique_levels = []
    #unique_levels.append((0,series.shape[0]))
    #print (unique_levels)
    for i in occurrenceThreshold:
        cond = series > i
        unique_levels.append((i,cond.sum()))

    uc = pd.DataFrame.from_records(unique_levels, columns = ['occurrenceThreshold.GrtThan','uniqueLevels'])
    return uc



# Save dictionary to file
def save_dict_to_file(dic, filename, pathToFile):
    """
    Called by: levelsTransformer()
    Given a dictionary and 'filename',
    saves dict as a .pkl file at
    folder: pathToFile.
    """
    filename = pathToFile + filename
    with open(filename, 'wb') as f:
        pickle.dump(dic, f)



# Called by updateLevels(), levelsTransformer()
#   and readAllMappingDict()
def load_dict_from_file(filename, pathToFile):
    """
    Called by: updateLevels(), levelsTransformer(), readAllMappingDict()
    Returns dictionary saved into a pickle file: 'filename'
      'filename' is in folder 'pathToFile'.
    """
    filename = pathToFile + filename
    with open(filename, 'rb') as f:
        loaded_dict = pickle.load(f)
    return loaded_dict



# Called by talkingData_submissiondata_preprocessing.py
def updateLevels(df,mapdictpath, cat_features):
    """
    Given a set of saved dictionaries, that map Existing
    column levels (keys in the dict) to new levels (values
    in the dict), this function updates DataFrame column
    values (levels) as per the mapping specified in the
    correspondng keys of dict.

    """
    # Read all files storing mapping dictionaries
    files = os.listdir(mapdictpath)
    for file in files:
        # split filename only at the first "_"
        # We get the column name wherein levels are
        #  to be mapped/updated
        #  Example" mapLevelsDict_channel_p_ip.pkl
        colName = file.split("_", 1)[1]   # Column 'channel_p_ip.pkl'
        colName = colName.split(".")[0]   # Jettison ''.pkl'; get: 'channel_p_ip'

        if colName in cat_features:
            # Get its datatype
            datatype = df[colName].dtype
            # Read the Dictionary into 'mapdict'
            mapdict = load_dict_from_file(file, mapdictpath)
            # Get all keys
            keys_df = list(df[colName])
            # GEt all keys in mapdict
            keys_mapdict = list(mapdict.keys())
            # mapdict does not have mapping for the following keys:
            not_present_keys = set(keys_df) -set(keys_mapdict)
            # So create default mapping
            values = ['99999']*len(not_present_keys)
            d = dict(zip(not_present_keys, values))
            # Update mapdict with these added mappings
            mapdict.update(d)
            # Perform transformation as per updated dictionary
            df[colName] = df[colName].map(mapdict.get)
            # Reset datatype
            df[colName] = df[colName].astype(datatype)
    return df


# Reads all stored network models
# Called by network_features.transform_from_storedModels()
def readAllStoredModels(pathToReadFrom, prefix = None):
    """
    Called by: network_features.transform_from_storedModels()
    Calls: None
    """
    os.chdir(pathToReadFrom)
    model_dfs = []
    if (prefix is None):
        prefix = "*.pkl"
    else:
        prefix = prefix + "*.pkl"
    for file in glob.glob(prefix):
        df = pd.read_pickle(file)
        model_dfs.append(df)
    return model_dfs



# Read a single specified stored model
#  Just for debugging purposes.
def readStoredModel(pathToReadFrom, modelfile):
    os.chdir(pathToReadFrom)
    return pd.read_pickle(modelfile)




def xg_impt_features(model, df_columns, filename = None, master=None):
    """
    Given an xgboost classifier model & data col
    names, the function returns two lists of cols,
    one of impt features and the other of 
    unimportant features. Feature importances
    areby 'gain' as against default 'weight'
    in plot_importance() function of xgboost.
   
    Parameters
    ----------
    model: xgboostclassifier model trained on dataframe df
    df_columns: Column names of df. Sequence
                is important: df_columns = list(df.columns)
    master: Folder where impt feature sequence is saved
            File name: fe_1.txt          
    Returns
    -------
    fe_1 : List of columns having features imp > 0 in descending order
    fe_0 : List of columns having features imp of 0.0
    """
    # Sorted index are in descending order of impt
    sorted_idx = model.feature_importances_.argsort()[::-1]
    fe = pd.DataFrame(
                       model.feature_importances_[sorted_idx],
                       index = df_columns[sorted_idx],
                       columns =['imp']
                     )
    # Columns with zero feature impt
    fe_0 = list(fe.loc[fe['imp'] == 0.0, :].index)
    # Columns greater than than zero feature impt
    # fe_1 is in descending order
    fe_1 = list(fe.loc[fe['imp'] > 0.0, :].index)
    print("Order of feature importance is by 'gain'")
    # Save to file
    if filename is not None:
        # Also save these features
        filename = pathlib.Path(master) / filename
        with open(filename,'w') as tfile:
            tfile.write('\n'.join(fe_1))
    return fe_1, fe_0
   



# https://stackoverflow.com/a/44674459
# ToDO REMOVE zero variance threshold   <=== *****
def rem_corr_features(data, threshold):
    """
    Desc
    ----
    Function drops features which have pearson's corr
    value more than or equal to the threshold. Absolute
    value of theshold is taken.
    Parameters
    ----------
    data : DataFrame from whom highly corr
           features are to be removed
    threshold : Corr threshold beyond which a 
                feature will be dropped
    Returns
    -------
    un_corr_data : DataFrame with highly corr
                   features dropped
    """
    un_corr_data = data.copy()
    col_corr = set() # Set of all the names of deleted columns
    # Consider both +ve and -ve correlations
    corr_matrix = un_corr_data.corr().abs()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i, j] >= threshold) and (corr_matrix.columns[j] not in col_corr):
                colname = corr_matrix.columns[i] # getting the name of column
                col_corr.add(colname)
                if colname in un_corr_data.columns:
                    del un_corr_data[colname] # deleting the column from the un_corr_data

    return un_corr_data





# Reads all mapping dictionaries
def readAllMappingDict(pathToReadFrom):
    """
    Reads files stored in .pkl format from folder
    pathToReadFrom. Each file is a dictionary.
    Dictioary maps existing levels of a column
    to new levels(if any). Returns list of dictionaries.
    """
    os.chdir(pathToReadFrom)
    dicts = []
    for filename in glob.glob("*.pkl"):
        sk = load_dict_from_file(filename, pathToReadFrom)
        dicts.append(sk)
    return dicts



# Reduce memory usage
def reduce_mem_usage(data, fromIndex = 0):
    """
    Parameters
    ----------
    data: Pandas dataframe
    fromIndex: Transform to float32 from index fromIndex
    Desc
    ----
    The function changes data types from float64 to float32
    of all features of DataFrame, data, from index 'fromIndex'
    Returns
    -------
    Returns complete pandas dataframe with datatypes changed
    of desired columns
   
    """
    gc.collect()
    print(f"Current memory usage is: {data.memory_usage().sum()/1000000} MB")  # 9404.2MB/11163MB
    data.iloc[:,fromIndex:] = data.iloc[:,fromIndex:].astype('float32')
    print(f"Memory usage after transformation is: {data.memory_usage().sum()/1000000} MB")  # 4734.6MB
    return data


def add_stats(df):
    """
    Given a dataframe with all numeric features,
    this function creates more numeric features,
    row-wise, as: std, mean, median,min, max
    and kurtosis. Returns modified dataFrame.
    """
    df['std'] = np.std(df,axis = 1)
    df['mean'] = np.mean(df, axis = 1)
    df['median'] = np.median(df,axis = 1)
    df['min'] = np.min(df,axis = 1)
    df['max'] = np.max(df,axis =1)
    df['kurtosis'] = kurtosis(df.values, axis =1 )
    return df







# Generate data using sklearn's make_classification
def generateSklearnData(X,y, test_size = 0.25, bins = 20, genColName = True):
    """
    The function discretises X assuming all features in X
    have continuous values. Discretisation of all features 
    is perfomed as per number of 'bins' specified. 
    We then have two datasets: original and discretised.
    Both original and discretised versions continue to have 
    the same row-orderings. And hence returned sample of continuous
    data corresponds to returned sample of discrete data.
    
    The functon assumes that X,y have been generated by one of
    sklearn's make datasets algorithm and hence do not have
    header. The function assigns a header.
    
    Parameters
    ----------
    

    Returns
    -------
    orig_train : pandas DataFrame
        Has continuous features
    orig_test : pandas DataFrame
        HAs continuous features
    train_train : pandas DataFrame
        Has discrete features
    train_test : pandas DataFrame
        Has discrete features

    """
    X_data = np.array(X)
    y_data = np.array(y)
    colnames = list(X.columns)
    
    orig_train, orig_test,train_binned,test_binned = transformToCatFeatures(X_data,y_data, test_size, bins, colnames, genColName)
    return orig_train, orig_test, train_binned, test_binned    







# Generate data using sklearn's make_classification
def generateClassificationData(n_samples = 10000, n_features = 10, n_informative = 5,
                               n_classes = 2,n_clusters_per_class = 3, class_sep = 0.5,
                               weights= [0.5,0.5], test_size = 0.25, bins = 20, 
                               flip_y = 0.01, hypercube = True, seed = 42,genColName = True):
    """
    The function generates data for classification task using 
    sklearn's make_classification(). All features generted by 
    make_classification() have continuous values. After data 
    is generated, we discretise all features as per number of
    'bins' specified. We then have two datasets: original and 
    discretised. Both the datasets are shuffled and split into
    train and test data. 
    Note that both the datasets continue to have the same 
    row-orderings. And hence returned sample of continuous
    data corresponds to returned sample of discrete data.
    
    Parameters
    ----------
    For description of parameters, please see sklearn's documentation

    Returns
    -------
    orig_train : pandas DataFrame
        Has continuous features
    orig_test : pandas DataFrame
        HAs continuous features
    train_train : pandas DataFrame
        Has discrete features
    train_test : pandas DataFrame
        Has discrete features

    """
    X, y = make_classification(
                                n_samples=n_samples,  # row number
                                n_features=n_features, # feature numbers
                                n_informative= n_informative, # The number of informative features
                                n_redundant = 0, # The number of redundant features
                                n_repeated = 0, # The number of duplicated features
                                n_classes = n_classes, # The number of classes 
                                n_clusters_per_class= n_clusters_per_class,#The number of clusters per class
                                random_state = 42 ,# random seed
                                class_sep = class_sep,
                                flip_y = flip_y
                             )
    
    X_data = np.array(X)
    y_data = np.array(y)
    
    orig_train, orig_test,train_binned,test_binned = transformToCatFeatures(X_data,y_data, test_size, bins, genColName)
    return orig_train, orig_test, train_binned, test_binned    


 
def transformToCatFeatures(X_data,y_data, test_size = 0.25, bins= 20,  colnames = None, genColName = True):
    
    """
    Given a DataFrame X_data having only continuous features, 
    and y_data the target, the function bins each feature. 
    The resulting dataframe as also the original is partitioned
    into train/test as per specified test_size.
    Parameters
    ----------
    X_data : A pandas DataFrame (data features)
    y_data : A pandas series (data target)
    test_size : How data is to be partitioned into train/test
               The default is 0.25.
    bins : Number of bins into which each column of X
           will be discretised. The default is 20.
    genColName : Should new column names be generated?
                 The default is True.

    Returns
    -------
    orig_train : train sample taken from X 
    orig_test : test sample taken from X
    train_binned : train sample but binned 
                   taken from X
    test_binned : test sample but binned
                  taken from X

    """
    
    if not genColName:
        colnames = colnames
    
    
    orig = pd.DataFrame(X_data)
    train = orig.copy()
    # Generate integer levels
    for i, j in enumerate(train.columns):
        k = ( (i+1) * 4)    # generate an integer as a unique prefix for this iteration
        g = []              # Will contain levels (names)
        # Generate as many level-names as number of bins for jth column
        for i in range(bins):   # For each one of bins (levels)
            g.append(str(k) +str(i+1))   # g conatins a list of names for levels
        
        # for 'j' column, cut it into bins and assign each bin a label 
        # No of bins and o of labels must be same.
        train[j] = pd.cut(train[j], bins, labels = g)  
    
    if genColName:
        # Also generate new column names
        alphabet = string.ascii_lowercase    
        colnames = ["f" + alphabet[i] for i in range(len(train.columns)) ]
        
    train.columns = colnames
    orig.columns = colnames
    train['target'] = y_data
    orig['target'] = y_data
    
    # Shuffle data
    h = train.index.values
    np.random.shuffle(h)
    train = train.loc[h]
    orig = orig.loc[h]
    
    # Pick top 1-test_size rows
    train_binned = train.iloc[ int(train.shape[0] * test_size) :, : ]
    test_binned  = train.iloc[ :int(train.shape[0] * test_size)  , : ]
    
    # Pick bottom test_size rows
    orig_train = orig.iloc[ int(train.shape[0] * test_size) :, : ]
    orig_test = orig.iloc[ :int(train.shape[0] * test_size)  , : ]
    
    return orig_train, orig_test, train_binned, test_binned    
        

#### NOT USED MAy BE DELETED
# Given a feature 'colName', merge all infrequent levels that occur below
#   an 'occurrenceThreshold'. For example merge all those levels into one whose
#    value_counts() is below 10 ('occurrenceThreshold')
def fmergeRareLevels(df,colName, occurrenceThreshold, replace_by = '99999'):
    """
    In df[colName] merge all those levels into 'replace_by' whose total count
    is less than or equal to occurrenceThreshold.
    """
    x = df[colName].value_counts().reset_index().rename(columns = {'index' : 'levels', 'device' : 'countOfLevels'})
    levelsWithlowCount = x.loc[x['countOfLevels'] <= occurrenceThreshold, 'levels']
    df[colName] = df[colName].replace(to_replace = levelsWithlowCount.values, value = replace_by )
    gc.collect()
    return df




def old_mergeRareLevels(df,colName, occurrenceThreshold, model = None, replace_by = '99999'):
    """
    Called by: levelsTransformer()
    Returns: model and dataframe modified as per the model
             A model is a dictionary wher 'key' is old_level
             and value is the new level. For a level which
             has high occurrenceThreshold, both 'key' and 'value'
             would be same.
    If no earlier model exist:
        In df[colName] merge all those levels to 'replace_by' whose total count
        is less than or equal to occurrenceThreshold.

    This code has a problem. We take two samples of df: df1, df2. In df1,
    a level, say, 'xyz' occurs very frequently and hence is unchanged. But
    in df2, 'xyz' occurs infrequently, and therefore gets changed to 999.
    This should not happen.
    How to update a dictionary only by adding new key:value pairs and NOT
    modify earlier ones.
    """
    if model is not None:
        # Get present dictionary
        # Unless changed, values in a column
        #  get mapped to same values
        d = dict(zip(df[colName],df[colName]))
        # Update it using model
        d.update(model)
        # Perform transformation
        df[colName] = df[colName].map(d.get)
        # This is our present model
        model = d

    series = df[colName].value_counts()
    cond = series > occurrenceThreshold
    replacement_values = np.where(cond, series.index, replace_by)
    # A dictionary of what is to be replaced with what
    # This will also serve as model for future data
    currentmodel = {i:j for i, j in zip(series.index,replacement_values)}
    # The following code is very slow
    #df[colName] = df[colName].replace(model)
    # This one using map() is fast
    # https://stackoverflow.com/a/41987136
    df[colName] = df[colName].map(currentmodel.get)
    if model is not None:
        # Compare df[colName] and df[newColName] to create a dictionary for mappimg
        model.update(currentmodel)
    else:
        model = currentmodel
    return df,model


# This function is redundant. Not needed. May be deleted
# Replaces value 'replace_by' with 99999 and sets datatype
def replace_Others_by_99999(df,colName, data_type, replace_by = '99999'):
    """
    Replace 'Others' in df[colName] by replace_by and also set datatype to data_type
    The function does not check if level '99999' already exists or not
    """
    df[colName] = df[colName].replace({'Others' : replace_by})
    # Check is 'Others' at all exists
    f = (df[colName] == replace_by).sum()
    if f >0 :
        df[colName] = df[colName].astype(data_type)
    return df

# Added on 2nd April, 2023
 # Refer: https://stackoverflow.com/a/31799225
def removeLowVarCols(df,threshold = 0.05, pca = False):
    """
    Remove columns from pandas DataFrame having variance below threshold
    Parameters
    ----------
    df: Pandas DataFrame
    threshold: Float value
    Returns
    -------
    DataFrame with columns having low threshold dropped
    """
    if (pca) :
        pc = PCA(n_components = 0.95)
        out_pc = pc.fit_transform(df)
        c_names = [ "c" + str(i) for i in range(out_pc.shape[1])]
        out_pc = pd.DataFrame(out_pc, columns = c_names)
    else:
         if (threshold != 0):
             out_pc = df.drop(df.std()[df.std() < threshold].index.values, axis=1)
    return out_pc


# Added on 11th April
def binFeatures(df, bins= 20, ):
    for i, j in enumerate(df.columns):
        k = ( (i+1) * 4)    # generate a unique prefix for every iteration
        g = []              # Will contain label names
        for i in range(bins):   # For each one of bins (levels)
            g.append(str(k) +str(i+1))   # g conatins a list of names for levels
            
        df[j] = pd.cut(df[j], bins, labels = g)  
    return df    
    

# rng is randomstate
# rng = np.random.RandomState(123)
def randomsample(ar, perstratasize, rng):
    fact = ar
    idx_arr = np.hstack(
         (
            rng.choice(np.argwhere(fact == 0).flatten(), perstratasize, replace=False),
            rng.choice(np.argwhere(fact == 1).flatten(), perstratasize, replace=False),
            rng.choice(np.argwhere(fact == 2).flatten(), perstratasize, replace=False),
            rng.choice(np.argwhere(fact == 3).flatten(), perstratasize, replace=False),
            rng.choice(np.argwhere(fact == 4).flatten(), perstratasize, replace=False),
            rng.choice(np.argwhere(fact == 5).flatten(), perstratasize, replace=False),
            rng.choice(np.argwhere(fact == 6).flatten(), perstratasize, replace=False),
         )
      )
    tar = np.arange(len(ar))
    tr_ar = list(set(tar).difference(set(idx_arr)))
    return np.array(tr_ar),idx_arr    # train/test arrays






# StackOverflow: https://stackoverflow.com/a/24953575
def plotResults(results, metric):
    """
    Desc
    ----
    
    Plots learning curve after xgboost modeling

    Parameters
    ----------
    results : xgboost results object
    metric : Metric of interest

    Returns
    -------
    None.

    """
    
    ## Plotting results
    epochs = len(results["validation_0"][metric])
    x_axis = range(0, epochs)
    # plot log loss
    fig, ax = plt.subplots(figsize=(12,12))
    ax.plot(x_axis, results["validation_0"][metric], label="Train")
    ax.plot(x_axis, results["validation_1"][metric], label="Test")
    # Set major axis ticks for x and y
    major_x_ticks = np.arange(0, 500, 25)
    major_y_ticks = np.arange(0.9, 1.01, 0.005)
    
    #grid_points = [0.89,0.90,0.91,0.92,0.93,0.94,0.95, 0.955, 0.96,0.97,0.98,0.99,1.0]
    ax.yaxis.set_ticks(major_y_ticks)
    ax.xaxis.set_ticks(major_x_ticks)
    
    ax.grid(True, alpha = 0.5)
    ax.legend()
    plt.ylabel(metric)
    plt.xlabel("No of iterations")
    plt.title("Plot of "+ metric)
    plt.show()


# Plot results of two modeling on the same plot
def plotMulResults(results1, results2, metric, lt_iterations = 500):
    """
    Desc
    -----
    
    Plots learning curves from two different xgboost modeling results

    Parameters
    ----------
    results1 : xgboost results object from Ist modeling
    results2 : xgboost results object from IInd modeling
    metric : Metric being evaluated
    lt_iterations : X-axis iterations limit. The default is 500.

    Returns
    -------
    None.

    """
    ## Plotting results
    epochs = len(results1["validation_0"][metric][:lt_iterations])
    x_axis = range(0, epochs)
    # plot log loss
    fig, ax = plt.subplots(figsize=(12,12))
    ax.plot(x_axis, results1["validation_0"][metric][:lt_iterations], label="Train1")
    ax.plot(x_axis, results1["validation_1"][metric][:lt_iterations], label="Test1")

    ax.plot(x_axis, results2["validation_0"][metric][:lt_iterations], label="Train2")
    ax.plot(x_axis, results2["validation_1"][metric][:lt_iterations], label="Test3")

    # Set major axis ticks for x and y
    major_x_ticks = np.arange(0, lt_iterations, 25)
    major_y_ticks = np.arange(0.9, 1.01, 0.005)
    
    grid_points = [0.89,0.90,0.91,0.92,0.93,0.94,0.95, 0.955, 0.96,0.97,0.98,0.99,1.0]
    ax.yaxis.set_ticks(major_y_ticks)
    ax.xaxis.set_ticks(major_x_ticks)
    
    ax.grid(True, alpha = 0.5)
    ax.legend()
    plt.ylabel(metric)
    plt.xlabel("No of iterations")
    plt.title(f"Plot of {metric} for {lt_iterations} iterations")
    plt.show()
    
    
def bootstrap_sample(df)    :
    """
    Desc
    -----
    Return bootstrap samples of
    df, pandas dataframe.
    Parameters
    ----------
    df : Pandas DataFrame

    Returns
    -------
    A bootstrap sample of the dataframe
    
    """
    k = np.arange(df.shape[0])
    rows= np.random.choice(k, size = len(k), replace = True)
    return (df.loc[rows].copy()).reset_index()



# Ref: https://stackoverflow.com/a/4529901/3282777
def savePythonObject(pythonObject, filename, filePath = None ):
    
    """
    Saves any python object to disk
    File is saved to filePath. Restore it
    using restorePythonObject()
    Parameters
    ----------
    filename : pickle file for dumping
    Returns
    -------
    None.
    """
    # Current dir is the default filePath
    if filePath is None:
        filePath = pathlib.Path.cwd()
        path = filePath / filename
    else:
        path = pathlib.Path(filePath) / filename
    with open(path, 'wb') as outp:
        pickle.dump(pythonObject, outp, pickle.HIGHEST_PROTOCOL)

     
     

 # It restores an earlier saved python object
def restorePythonObject(filename, filePath = None):
     """
     Called by: None
     Calls: None
     Restores an earlier saved python object
     in pickle format by savePythonObject()
     Parameters
     ----------
     filename : Pickle file having python-object
     filePath : Folder where filename is placed
                Default is modelsPath

     Returns
     -------
     Python-object

     """
     if filePath is None:
        filePath = pathlib.Path.cwd()
        path = filePath / filename
     else:
        path = pathlib.Path(filePath) / filename

     with open(path, 'rb') as inp:
         ct = pickle.load(inp)
     return ct    



def pcaAndConcat(vec_train, vec_test, n_components = 2, scaleData = True):
    """
    Calls: 
    Called by: main method as needed    
    
    
    Desc
    ----
    Given a dictionray of dataframes, the function performs PCA
    on each dataframe and outputs a concatenated dataframe. 
    This it does for both the dictionaries and outputs two dataframes. 
    
    Parameters
    ----------
    
    vec_train: Dictionary of Dataframes. It would contain unit vectors
               for each cat col of train data.
               
    vec_test:  Dictionary of Dataframes. It would contain unit vectors
               for each cat col of test data.         
               
    n_components: No of PCA components. Default is 2.
    scaleData: boolean; Should data be centered and scaled before PCA?
               Default is True.
    
    Returns
    -------
    
    Concated dataframes and two dictionaries. Each dictionary is of 
    DataFrames, as before, except that evry DataFrame that was input
    is replaced by its PCA version with as many columns as n_components.
    Two dictionaries returned are mainly for debugging purposes.

    """
    
    # Do not alter original dataframes
    vt = vec_train.copy()
    ve = vec_test.copy()

    # What all columns exist?
    rt = list(vt.keys())
    
    # For every col in rt
    # StandardScale before PCA
    if scaleData:
        for key in rt:
            print(f"Performing PCA for {key} for train data")
            # Instantiate PCA
            pca = PCA(n_components = n_components)
            ss = StandardScaler()
            # Perform PCA of train DataFrame of unit vectors
            k = pca.fit_transform(ss.fit_transform(vec_train[key]))
            vt[key] = pd.DataFrame(k, columns = ['pc' + key+ str(i) for i in range(n_components)])
            print(f"Performing PCA for {key} for test data")
            # Transform test data now
            k = pca.transform(ss.transform(vec_test[key]))
            ve[key] = pd.DataFrame(k, columns = ['pc' + key +str(i) for i in range(n_components)])
    else:
        for key in rt:
            print(f"Performing PCA for {key} for train data")
            # Instantiate PCA
            pca = PCA(n_components = n_components)
            # Perform PCA of train DataFrame of unit vectors
            k = pca.fit_transform(vec_train[key])
            vt[key] = pd.DataFrame(k, columns = ['pc' + key+ str(i) for i in range(n_components)])
            print(f"Performing PCA for {key} for test data")
            # Transform test data now
            k = pca.transform(vec_test[key])
            ve[key] = pd.DataFrame(k, columns = ['pc' + key +str(i) for i in range(n_components)])
    
    obj_tr = [ vt[rt[i]]  for i in range(len(rt))]
    obj_te = [ ve[rt[i]]  for i in range(len(rt))]
    print("Concatenating train data")
    cc_tr = pd.concat(obj_tr, axis = 1)
    print("Concatenating test data")
    cc_te = pd.concat(obj_te, axis = 1)
    print("Done......")
    return cc_tr,cc_te,  vt ,ve, 



############################ BEGIN ###################











######################








# Fill NA in Data Frame based upon
#  merged level
"""
def fillNAs(df):
    for i in df.columns:
        df[]
"""

#### Demo dataframe to test functions
_data1 = {'var1': ['a','b','c','a','a','b','a','b','b'],
          'var2': ['x','y','y','z','y','y','x', 'y','y'],
          'var3':['xx','xy','yz','yz','xy','xy','xy', 'yz','xx'],
          'var4':['t','s','s','s','s','t','t', 's','s'],
          'var5':['sx','xt','sx','xt','xg','xg','xt', 'sx','sx'],
          'var6':['xyz','xyz','yzx','yzx','zxy','zxy','xyz', 'yzx','zxy'],
          'var7':['xxn','xyn','xxn','xxn','xyn','xym','xym', 'xxn','xym']
         }

_df_original = pd.DataFrame(_data1)
_df_original


_demo = { 'var1' : ['a','a','b','a','b','a','a','c']*1000 ,
          'var2' : ['x','x','x','y','x','x','y','z']*1000 ,
          'var3' : ['x','x','x','y','x','y','y','z']*1000 ,
        }

_df_org = pd.DataFrame(_demo)

##############33###################


d1 = {'a' : 'a', 'b' : 'b', 'c' : 'other', 'd' : 'other'}
d2 = {'f' : 'f', 'g' : 'g', 'c' : 'other', 'e' : 'other'}  # Only 'c':'other' is common
d3 = {'k' : 'k', 'l' : 'l'}
d4 = {'a' : 'gh', 'b' : 'b', 'c' : 'other', 'd' : 'other'} # Same as d1 but 'a' : 'gh'
d1.update(d2)
d1
d1.update(d4)
d1     # {'a': 'gh', 'b': 'b', 'c': 'other', 'd': 'other'}


d1.update(d3)
d1
################################
# Extract of code used in mergeRareLevels()
series = _df_org.value_counts('var1')
series
occurrenceThreshold = 1005
cond = series > occurrenceThreshold
cond
replace_by = '999999'
replacement_values = np.where(cond, series.index, replace_by)
replacement_values
currentmodel = {i:j for i, j in zip(series.index,replacement_values)}
currentmodel
oldmodel = {'a' : 'a', 'h' : '99', 'c' : 'c' }

newkeys = set(currentmodel.keys()) - set(oldmodel.keys())
newkeys
for keys in newkeys:
    oldmodel[keys] = currentmodel[keys]

oldmodel

_df_org['var1'] = _df_org['var1'].map(oldmodel.get)
_df_org['var1'].value_counts()

"""
MergeLevels
Problem: Let earlier discovered levels be: a,a,a,b,b,c. Let
transformation be: a=>a, b=>b, c=>99. Let levels in the new
samples be: c,c,c,d,d,a. Then transformation will be:
c=>c,d=>d,a=99.
Solution to the problem is to take large random samples.
"""






######################################3

