from sklearn.pipeline import Pipeline
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
import os
from PIL import Image
import cv2
from tqdm import tqdm
from tabulate import tabulate
from feature_engine.encoding import *
import klib

def bivar_dis(df, fea_list, mode='Line'):
    """
    Plot bivar_dis for a feature list in df.
    Detailed explanation
    Args:
        df: train in dataframe
        fea_list: [['fea1', 'fea2'], ['fea1', 'fea2'], ['fea1', 'fea2']]
    Returns:
        nothing
    """
    ncols = 3
    nrows = (len(fea_list) + ncols - 1) // ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, nrows * 5), constrained_layout=True)
    axs = axs.reshape(nrows, -1)  # Ensure axs is always 2-dimensional

    for idx, (fea1, fea2) in enumerate(fea_list):
        row, col_idx = divmod(idx, ncols)

        if pd.api.types.is_numeric_dtype(df[fea1]):
            if mode == 'Bar':
                sns.histplot(data=df, x=fea1, hue=fea2, multiple="dodge", shrink=.8, ax=axs[row, col_idx])
            elif mode == 'Line':
                sns.kdeplot(data=df, x=fea1, hue=fea2, ax=axs[row, col_idx])

        elif pd.api.types.is_string_dtype(df[fea1]):
            if mode == 'Bar':
                sns.histplot(data=df, x=fea1, hue=fea2, multiple="dodge", shrink=.8, ax=axs[row, col_idx])
            elif mode == 'Line':
                sns.histplot(data=df, x=fea1, hue=fea2, element="poly", ax=axs[row, col_idx])
        else:
            print(f"Unsupported feature types: {fea1}, {fea2}")
            continue

        axs[row, col_idx].set_title(f"{fea1} vs {fea2}")

    # Remove unused subplots
    for idx in range(len(fea_list), nrows * ncols):
        row, col_idx = divmod(idx, ncols)
        fig.delaxes(axs[row, col_idx])

    plt.show()

    
    

def univar_dis(train_df, collist, mode='bar'):
    """
    Plot distribution for a feature list in df.
    Detailed explanation
    Args:
        train_df: train dataset in dataframe
        collist: ['fea1','fea2' etc,.]
    Returns:
        nothing
    """
    num_list, cata_list, other_list = generate_lists(train_df, collist)
    
    # Plot the distribution for numerical features
    klib.dist_plot(train_df[num_list])

    # Plot the distribution for categorical features
    if cata_list!=[]:
        if mode == 'bar':
            plot_categorical_distribution(train_df, cata_list)
        elif mode == 'pie':
            plot_categorical_pie_charts(train_df, cata_list)

    # Print the other features
    print("Other features: ", other_list)

def generate_lists(df, collist):
    num_list = []
    cata_list = []
    other_list = []

    for col in collist:
        if df[col].nunique() > 10 and pd.api.types.is_numeric_dtype(df[col]):
            num_list.append(col)
        elif df[col].nunique() <= 10 and (pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_string_dtype(df[col])):
            cata_list.append(col)
        else:
            other_list.append(col)
    return num_list, cata_list, other_list



def plot_categorical_distribution(df, cata_list):
    ncols = 3
    nrows = (len(cata_list) + ncols - 1) // ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, nrows * 5), constrained_layout=True)

    # Adjust for 1D and 2D axs array.
    if nrows == 1:
        axs = axs[np.newaxis, :]
    elif ncols == 1:
        axs = axs[:, np.newaxis]
        
    for idx, col in enumerate(cata_list):
        row, col_idx = divmod(idx, ncols)
        sns.countplot(x=col, data=df, ax=axs[row, col_idx])
        axs[row, col_idx].set_title(f"{col} Distribution")

    # Remove unused subplots
    for idx in range(len(cata_list), nrows * ncols):
        row, col_idx = divmod(idx, ncols)
        fig.delaxes(axs[row, col_idx])

    plt.show()
    
def plot_categorical_pie_charts(df, cata_list):
    ncols = 3
    nrows = (len(cata_list) + ncols - 1) // ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(15, nrows * 5), constrained_layout=True)

    # Adjust for 1D and 2D axs array.
    if nrows == 1:
        axs = axs[np.newaxis, :]
    elif ncols == 1:
        axs = axs[:, np.newaxis]

    for idx, col in enumerate(cata_list):
        row, col_idx = divmod(idx, ncols)
        df[col].value_counts().plot.pie(autopct='%1.1f%%', ax=axs[row, col_idx]) #e
        axs[row, col_idx].set_ylabel('')
        axs[row, col_idx].set_title(f"{col} Distribution")

    # Remove unused subplots
    for idx in range(len(cata_list), nrows * ncols):
        row, col_idx = divmod(idx, ncols)
        fig.delaxes(axs[row, col_idx])

    plt.show()