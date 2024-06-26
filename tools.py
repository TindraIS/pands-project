'''
Name: tools.py

Author: Irina Simoes

Description: This file contains a module with all the functions that perform the core tasks on the menu.py.

'''

import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
import helpers
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# _____________________ GET IRIS _____________________
def get_dataset():
    '''
    This function fetches the Iris dataset from the Seaborn library as a DataFrame object.

    I. Get a list of all datasets available in the Seasborn library
       https://github.com/mwaskom/seaborn-data
       https://seaborn.pydata.org/generated/seaborn.get_dataset_names.html

    II. Use the filter() function with a lambda to filter elements in the datasets names list returned by Seaborn 
        containing the 'iris' string. As the previous is wrapped in list, we then access it by indexing the first and only result 
        returned by the lambda function.
        https://seaborn.pydata.org/generated/seaborn.load_dataset.html
        https://www.w3resource.com/python-exercises/lambda/python-lambda-exercise-39.php

    III. Load the Iris dataset which is a DataFrame object by default, as the Seaborn library is closely integrated with pandas 
         data structures. Then we use the return statement to send the DataFrame back to the caller of the function, enabling 
         analysis.py to access the Iris dataset.
         https://seaborn.pydata.org/generated/seaborn.load_dataset.html)]
    '''

    # I.
    # Get a list of all datasets available in the Seasborn library
    datasets_list = sns.get_dataset_names()

    # II.
    # Access the list returned by Seaborn with datasets names
    iris_dataset = list(filter(lambda x: "iris" in x, datasets_list))[0]

    # Print dataset name (uncomment for sanity check) 
    #print(f"Dataset name is: {iris_dataset}")

    # III.
    # Load the Iris dataset as df
    df = sns.load_dataset(iris_dataset)

    # Return the DataFrame object
    return df

# Create a test for the get_dataset() to verify its functionality, intended to run exclusively within tools.py 
# and not when the script is imported into analysis.py as a module
if __name__ == "__main__":
    iris_dataset = get_dataset()
    print("Iris dataset loaded successfully!")    


# _____________________ TXT SUMMARY _____________________
def descriptive_summary(df):
    '''
    This function creates a descriptive statistic summary of the variables in the Iris dataset.

    I. Initialise an empty string to store the summary and then we add overall summary, data types summary & 
        summary header for each species.

    II. Group the DataFrame by species & initialise a counter to be used to loop through them, as demonstrated in one of the lectures.
        Start the for loop - as we are grouping by multiple species, the group name will be a tuple so each group should be unpacked into two variables.
        Each iteration will then generate summary statistics for each species, and concatenate it to the summary container.
        https://realpython.com/pandas-groupby/
        https://realpython.com/python-for-loop/
        https://www.geeksforgeeks.org/how-to-iterate-over-dataframe-groups-in-python-pandas/

    III. Call the save_text_file() function from helpers.py module to save summary in a txt file with writer mode. 
        https://docs.python.org/3/library/functions.html#open
        https://stackoverflow.com/questions/72626730/python-launch-text-file-in-users-default-text-editor
        https://docs.python.org/3/library/os.path.html

    IV. Show message box prompting the user to choose to open the the file or not. As per Python documentation, 
        askokcancel returns a boolean value, so we check if response is True(OK) to save & open the file using 
        the file_path returned by save_text_file() function; if False the txt file will just be saved.
        https://stackoverflow.com/questions/72626730/python-launch-text-file-in-users-default-text-editor
        https://docs.python.org/3/library/tkinter.messagebox.html
    '''

    # I.
    print(f"\nStarting {__name__}/descriptive_summary()")

    # Initialise an empty string to store the summary
    summary = ''

    # Add overall summary, data types summary & summary header for each species
    descriptive_statistics = df.describe(include='all').to_string() 
    summary += f"(1) Overall Descriptive Statistics:\n{descriptive_statistics}\n\n"
    
    missing_values = df.isnull().sum().to_string()
    summary += f"(2) Data Types Summary:\n{missing_values}\n\n"
    
    print(f'\n\tOverall summary computed.')

    # II.
    summary += f"(3) Summary for Each Species:\n\n"

    # Group the DataFrame by species & initialise counter for the below for loop
    df_species = df.groupby('species')
    counter = 0

    # Iterate over each species and generate summary statistics
    # Given we are dealing with strings the '+' sign will append the text to summary variable in each iteration
    for species, group_df in df_species:
        counter += 1
        summary += f"3.{counter} Summary for {species}\n"

        descriptive_statistics = group_df.describe(include='all').to_string() 
        summary += f"a) Descriptive Statistics:\n{descriptive_statistics}\n\n" # Add descriptive statistics summary with pd.describe()
        
        missing_values = group_df.isnull().sum().to_string()
        summary += f"b) Missing Values:\n{missing_values}\n\n"  # Add missing values summary with pd.isnull()
        
        unique_values = group_df.nunique().to_string()
        summary += f"c) Unique Values:\n{unique_values}\n\n"  # Add unique values summary with pd.nunique()
        summary += "\n\n"
    
    print(f'\tSpecies summary computed.')

    # III.
    # Run save txt file function to save the summary in a txt file
    file_path = helpers.save_text_file('results', 'I.variables_summary.txt', summary)
    
    # Display message box with "OK" and "Cancel" buttons
    response = messagebox.askokcancel("Descriptive summary", "A text file with a descriptive summary of each variable will be saved in the results directory. Please click OK to open the file.")

    # IV.
    # If response is True save & open the txt file, otherwise just save the txt file
    if response:
        file_path
        print(f"\tDescriptive summaries added to the txt file.")
        os.startfile(file_path)
        print(f"\tUser opened the file.")
    else:
        file_path
        print(f"\tDescriptive summaries added to the txt file.")
        print(f"\tUser closed the pop-up.")
    
    # https://stackoverflow.com/questions/16676101/print-the-approval-sign-check-mark-u2713-in-python
    print("\n\t\u2713 Descriptive summary function successfully finished.")


# _____________________ OUTLIERS _____________________
def outliers_summary(df):
    '''
    This function computes a summary of outliers present in the Iris dataset by species, using the Inter Quartile Range (IQR) 
    approach to determine if an entry is an outlier. Given that the IQR measures the middle 50% of the data, outliers are 
    typically defined by statisticians as data points that fall 1.5 times above the third quartile or below the first quartile.
    Therefore, the formulas that define the outliers thresholds are:
            - Lower Bound = Q1 - 1.5 x IQR
            - Upper Bound = Q3 + 1.5 x IQR
    https://www.geeksforgeeks.org/detect-and-remove-the-outliers-using-python/
    https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data/box-whisker-plots/a/identifying-outliers-iqr-rule
    
    I. Create a container for the DataFrame columns names which will be analysed for outliers, filtering out any categorical features.
       https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html
    
    II. Initialise outlier_summary as an empty list to store the outlier information for each species. Then start looping through 
        each unique species in the df, filtering it for the current species. Bearing in mind that all iterations will have to be recorded,
        we create empty arrays(lower/upper_array_agg) which will serve as containers to aggregate the outlier indices.

    III. Compute the IQR calculation for each variable within each species using Numpy's where() function to identify the indices of outliers, 
        which are stored in upper_array and lower_array. Then append each iteration to lower/upper_array_agg.
        https://numpy.org/doc/stable/reference/generated/numpy.where.html
        
    IV. Create a final for loop to iterate through the combined list of variables and their corresponding outlier arrays created with zip().
        If any outliers are found, the arrays are not empty and so the outlier information is appended to the summary list.
        If no outliers are found, a message indicating no outliers is appended to the list.
        https://realpython.com/python-zip-function/

    V.  Compile the outliers_summary list items into one string before writing to file to avoid TypeError: write() argument must be str, not list.
        Then, call the save_text_file() function from helpers.py module to save summary in a txt file with writer mode. 
        https://docs.python.org/3/library/functions.html#open
        https://stackoverflow.com/questions/72626730/python-launch-text-file-in-users-default-text-editor
        https://docs.python.org/3/library/os.path.html

    VI. Show message box prompting the user to choose to open the the file or not. As per Python documentation, 
        askokcancel returns a boolean value, so we check if response is True(OK) to save & open the file using 
        the file_path returned by save_text_file() function; if False the txt file will just be saved.
        https://stackoverflow.com/questions/72626730/python-launch-text-file-in-users-default-text-editor
        https://docs.python.org/3/library/tkinter.messagebox.html
    '''

    # I. 
    print(f"Starting {__name__}/outliers_summary()")
    
    # Get the list of columns names in the DataFrame
    variables = df.select_dtypes(include='number').columns
    
    # II.
    # Initialise an empty list to store outlier information
    outlier_summary = []  

    # Iterate over unique species values
    for species in df['species'].unique():

        # Filter dataframe for the current species
        df_species = df[df['species'] == species]
        print(f'\n\tLooping through {species}...')
        
        outlier_summary.append(f'\n>>> Outlier summary for {species} <<<\n')

        lower_array_agg = []
        upper_array_agg = []

        # III.
        for var in variables: 
            # Calculate the upper and lower limits
            Q1 = df_species[var].quantile(0.25) # The 1st quartile is the value below which 25% of the data can be found
            Q3 = df_species[var].quantile(0.75) # The 3rd quartile is the value below which 75% of the data falls

            # Calculate the IQR, which measures the middle 50% of the data
            IQR = Q3 - Q1

            # Calculate the outlier thresholds as per the above formulas
            # Any data point below/above these values are considered outliers
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            # Create arrays of Boolean values indicating the outlier rows using Numpy's where() function
            # to find indices of all data points where the variable does meet the threshold condition
            upper_array = np.where(df_species[var] >= upper)[0]
            lower_array = np.where(df_species[var] <= lower)[0]

            lower_array_agg.append(lower_array)
            upper_array_agg.append(upper_array)

        # IV.
        # Check if any of the arrays contain outliers and append accordingly to the list.
        # Map and combine the variables and the arrays into a single iterable with zip() and loop through them 
        for var, lower_array, upper_array in zip(variables, lower_array_agg, upper_array_agg):
            
            # If any of the arrays isn't empty, append the outlier information to the list
            if len(lower_array) > 0 or len(upper_array) > 0:
                outlier_summary.append(f'\n\t\tOutliers found for {var}: \n\t\t\tLower bound: {lower_array} \n\t\t\tUpper bound: {upper_array}\n')
                print(f"\t\tOutlier summary for {var} appended to the array.")
            
            # If the arrays are empty, append a message stating so to maintain completeness 
            else:
                outlier_summary.append(f'\n\t\tNo outliers found for {var}\n')
                print(f"\t\tOutlier summary for {var} appended to the array.")

    # V.
    # Compile the list items into one string before writing to file to avoid TypeError: write() argument must be str, not list
    outlier_summary = ''.join(outlier_summary)

    # Run save txt file function to save the summary in a txt file
    file_path = helpers.save_text_file('results', 'II.outliers_summary.txt', outlier_summary)
    
    # Display message box with "OK" and "Cancel" buttons
    response = messagebox.askokcancel("Outlier summary", "A text file with an outlier summary by species will be saved in the results directory. Please click OK to open the file")

    # VI.
    # If response is True save & open the txt file, otherwise just save the txt file
    if response:
        file_path
        print(f"\Outliers summary added to the txt file.")
        os.startfile(file_path)
        print(f"\tUser opened the file.")
    else:
        file_path
        print(f"\tOutliers summary added to the txt file.")
        print(f"\tUser closed the pop-up.")
    
    # https://stackoverflow.com/questions/16676101/print-the-approval-sign-check-mark-u2713-in-python
    print("\n\t\u2713 Descriptive summary function successfully finished.")

def outliers_cleanup(df):
    '''
    Using the same logic as outliers_summary(df), this function removes the outliers present in the Iris dataset for each of the species.
    '''

    # I.
    print(f"Starting {__name__}/outliers_cleanup()")
    
    # Get the list of columns names in the DataFrame
    variables = df.select_dtypes(include='number').columns

    # Initialise empty array to store indices of outlier rows
    outlier_indices = []

    # Iterate over unique species in the DataFrame
    for species in df['species'].unique():
        
        # Filter dataframe for the current species
        df_species = df[df['species'] == species]
        print(f'\n\tLooping through {species}...')

        for var in variables: 
            # Calculate the upper and lower limits
            Q1 = df_species[var].quantile(0.25)  # The 1st quartile is the value below which 25% of the data can be found
            Q3 = df_species[var].quantile(0.75)  # The 3rd quartile is the value below which 75% of the data falls

            # Calculate the IQR, which measures the middle 50% of the data
            IQR = Q3 - Q1

            # Calculate the outlier thresholds as per the above formulas
            # Any data point below/above these values are considered outliers
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            # Use Numpy's where function to get [indices] of upper/lower outliers & combined them
            upper_outliers = np.where(df_species[var] >= upper)[0]
            lower_outliers = np.where(df_species[var] <= lower)[0]
            all_outliers = np.concatenate((upper_outliers, lower_outliers))
            
            # II.
            # Collect all indices by mapping local indices in df_species back to the global indices in the original df 
            # with iloc
            # https://www.geeksforgeeks.org/python-extracting-rows-using-pandas-iloc/
            global_outliers = df_species.iloc[all_outliers].index
            
            # Collect global outlier indices with extend() method to add multiple elements to a list
            # Tried appending but it didn't work as it would add the entire list as a single element, 
            # instead of adding each element of variable being looped to the list individually
            # https://www.geeksforgeeks.org/append-extend-python/
            outlier_indices.extend(global_outliers)
    
    # III.
    # Drop outliers from the original df
    df = df.drop(index=outlier_indices)
    
    # IV.
    # Run 'save_csv_file' function to save the cleaned DataFrame as a CSV file
    file_path = helpers.save_csv_file('results', 'II.dataframe_cleaned.csv', df)
    
    # Display message box with "OK" and "Cancel" buttons
    response = messagebox.askokcancel("Outliers cleanup", "A CSV file containing the Iris dataset without outliers will be saved in the results directory. Please click OK to open the file.")

    # V.
    # If response is True save & open the CSV file, otherwise just save the CSV
    if response:
        file_path
        print(f"\tOutliers summary added to the txt file.")
        os.startfile(file_path)
        print(f"\tUser opened the file.")
    else:
        file_path
        print(f"\tOutliers summary added to the txt file.")
        print(f"\tUser closed the pop-up.")
    
    # https://stackoverflow.com/questions/16676101/print-the-approval-sign-check-mark-u2713-in-python
    print("\n\t\u2713 Descriptive summary function successfully finished.")

    return df
        

# _____________________ HISTOGRAM _____________________
def generate_histogram(df, file_name):
    '''
    This function saves a histogram subplot of each variable in the Iris flower dataset as a PNG file.
    '''

    print(f"Starting {__name__}/generate_histogram()")

    # I. 
    # Get the list of columns names in the DataFrame
    variables = df.select_dtypes(include='number').columns
    species = df['species'].unique()

    # Dynamically calculate the number of rows and columns for the subplots
    num_variables = len(variables)       # Check how many variables the dataset contains
    num_rows = (num_variables + 1) // 2  # Ensure there are at least 2 plots per row
    num_columns = 2                      # Create 2 columns
    
    # II.
    # Create subplots
    fig, axes = plt.subplots(num_rows, num_columns, figsize=(14, 8))
    
    # Plot histograms for each variable
    # https://matplotlib.org/stable/gallery/color/named_colors.html#list-of-named-colors
    # Flatten the axes array
    axes = axes.flatten()

    # Create a dict object mapping colours to the different species
    # https://stackoverflow.com/questions/70356069/defining-and-using-a-dictionary-of-colours-in-a-plot
    colors = {'setosa': 'black', 'versicolor': 'orange', 'virginica': 'green'}

    # Refactor the same looping logic as in def outliers_summary(df):
    # use zip() to map each element from the variables list to the corresponding item from the axes list, combining them into a single iterable;
    # use enumerate() to add an index to these pairs.
    # During each iteration index is the current loop counter, col is the current variable, and ax is the current subplot axis.
    for index, (col, ax) in enumerate(zip(variables, axes)):
        for spec in species:
            # Filter dataframe for the current species
            df_species = df[df['species'] == spec]
            # Plot the histogram
            ax.hist(df_species[col], bins=10, color=colors[spec], alpha=0.5, label=spec, edgecolor='black')
        ax.set_title(col)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.legend(title='Species')
    
        print(f"\tHistograms have been computed.")

        # Cleanup the remainder unused subplots
        # https://napsterinblue.github.io/notes/python/viz/subplots/
        if index + 1 >= num_variables:
            [ax.set_visible(False) for ax in axes.flatten()[index+1:]]
            break
    
    # Adjust layout & set subplot suptitle
    plt.suptitle("\nDistribution of Variables in the Iris Dataset\n",fontsize=14)
    plt.tight_layout()

    # III.
    # Call 'save_csv_file' function from helpers.py module to save the plot as a PNG
    file_path = helpers.save_plot('results', file_name, fig)
    
    # Display message box with "OK" and "Cancel" buttons
    response = messagebox.askokcancel("Generate histograms", "A histogram of each variable will be plotted and saved in the results directory. Please click OK to open the file.")

    # IV.
    # If response is True save & open the PNG, otherwise just save the PNG
    if response:
        file_path
        print(f"\tPlot saved as PNG.")
        plt.show()
        print(f"\tUser opened the plot.")
    else:
        file_path
        print(f"\tPlot saved as PNG")
        print(f"\tUser closed the pop-up.")
    
    # https://stackoverflow.com/questions/16676101/print-the-approval-sign-check-mark-u2713-in-python
    print("\n\t\u2713 Histogram function successfully finished.")

def generate_histogram_options(df,df_cleaned):
    '''
    Helper function triggered by menu.py (button IV in the GUI), displaying a message box which prompts the user 
    to generate histograms for each variable using either the original DataFrame (df) or the cleaned DataFrame (df_cleaned) 
    without outliers. Depending on the user's choice, it calls the generate_histogram() function with the corresponding DataFrame.
    '''

    response = messagebox.askyesno("Generate histogram", "Would you like to generate the histogram without the outliers?")

    if response:
        generate_histogram(df_cleaned, 'IV.histograms_cleaned.png')
    else:
        generate_histogram(df, 'IV.histograms_original.png')


# _____________________ PAIRPLOT _____________________
def generate_pairplot(df, file_name):
    '''
    This function outputs a scatter plot of each pair of variables of the Iris dataset.
    '''

    # I.
    print(f"Starting {__name__}/generate_pairplot()")

    # Plot a pairplot to analyse the interaction between the different variables
    # https://python-charts.com/correlation/pairs-plot-seaborn/
    sns.pairplot(df, hue="species", corner=False, kind="reg", plot_kws={'line_kws':{'color':'black'}})

    # Adjust layout & set subplot suptitle
    plt.suptitle("Attribute Pairs by Species\n\n", fontsize=14)
    plt.tight_layout()

    print(f"\tHistograms have been computed.")

    # II.
    # Call 'save_plot' function from helpers.py module to save the plot as a PNG
    save_plot = helpers.save_plot('results', file_name, plt)
    
    # Display message box with "OK" and "Cancel" buttons
    response = messagebox.askokcancel("Generate pair scatter plot", "A scatter plot of each pair of variables will be created and saved in the results directory. Please click OK to open the file.")

    # III.
    # If response is True save & open the PNG, otherwise just save the PNG
    if response:
        save_plot
        print(f"\tPlot saved as PNG.")
        plt.show()
        print(f"\tUser opened the plot.")
    else:
        save_plot
        print(f"\tPlot saved as PNG")
        print(f"\tUser closed the pop-up.")
    
    # https://stackoverflow.com/questions/16676101/print-the-approval-sign-check-mark-u2713-in-python
    print("\n\t\u2713 Pairplot function successfully finished.")

def generate_pairplot_options(df,df_cleaned):
    '''
    Helper function triggered by menu.py (button III in the GUI), displaying a message box which prompts the user 
    to generate pair scatter plots using either the original DataFrame (df) or the cleaned DataFrame (df_cleaned) without outliers. 
    Depending on the user's choice, it calls the generate_pairplot() function with the corresponding DataFrame.
    '''

    response = messagebox.askyesno("Generate pair plot", "Would you like to generate the pair scatter plot without the outliers?")

    if response:
        generate_pairplot(df_cleaned, 'III.pairplot_cleaned.png')
    else:
        generate_pairplot(df, 'III.pairplot_original.png')


# _____________________ PCA _____________________
def perform_PCA(df, file_name):
    '''
    This function computes a PCA and reduces the 4-dimensional Iris dataset to 2 dimensions/features, outputing 
    a scatter plot of the principal components making it easier to understand how are species distributed.
    https://www.turing.com/kb/guide-to-principal-component-analysis
    https://towardsdatascience.com/a-step-by-step-introduction-to-pca-c0d78e26a0dd
    https://builtin.com/machine-learning/pca-in-python
    https://saturncloud.io/blog/what-is-sklearn-pca-explained-variance-and-explained-variance-ratio-difference
    
    I. Standardise the range of variables to analyse the contribution of each variable equally. This calculation
       categorises the variables that are dominating the other variables of small ranges, preventing a biased result. 
       The goal is to mimic a normal distribution by having a mean of 0 and a standard deviation of 1.
       https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html

    II. Compute the PCA, reducing the dataset to 2 components/variables

    III. Create new DataFrame with the variables created by sklearn when computing the PCA, concatenating it along the columns 
         with the original df containing only the species column. Since both DataFrames have same number of rows and are concatenated 
         along the columns, the original df filtered for species is added as a new column to pca_df. Therefore, this concat aligns 
         the species datapoints with the respective PCA based on the index.

    IV. Compute a scatter plot to visualise the PCA with a for loop through each species in the DataFrame, applying the same logic as 
        in generate_histogram() function.

    V.  Call the save_plot function from helpers.py module to save plot as a PNG file.
        https://docs.python.org/3/library/os.path.html
    
    VI. Show message box prompting the user to choose to open the the file or not. As per Python documentation, 
        askokcancel returns a boolean value, so we check if response is True(OK) to save & open the plot with plt.show(); if False the plot will just be saved.
        https://docs.python.org/3/library/tkinter.messagebox.html
        https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/tkMessageBox.html
    '''

    # I.
    # Standardise the data by scaling features into a normal distribution
    columns = df.select_dtypes(include='number').columns
    columns_array = df.loc[:, columns].values                       # Create a Numpy array containing the values of columns var before transformation as it doesn't support pandas DataFrames
    columns_array = StandardScaler().fit_transform(columns_array)   # Standardise the data with sklearn StandardScaler()

    # II.
    # Compute the PCA, reducing the dataset to 2 components/variables
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(columns_array)

    # III.
    # Create new DataFrame with the variables created by sklearn when computing the PCA
    pca_df = pd.DataFrame(data=principal_components, columns=['PCA_1', 'PCA_2'])
    pca_df = pd.concat([pca_df, df[['species']]], axis=1)
    print(f"\PCA has been computed & stored in a DataFrame.")

    # IV. 
    # Visualize the PCA result
    # Create a dict object mapping colours to the different species
    # https://stackoverflow.com/questions/70356069/defining-and-using-a-dictionary-of-colours-in-a-plot
    colors = {'setosa': 'black', 'versicolor': 'orange', 'virginica': 'green'}
    species = df['species'].unique()

    # Define plot size
    plt.figure(figsize=(8, 6))

    # Loop through each species in the DataFrame, applying the same logic as in generate_histogram()
    for spec in species:
        # Filter dataframe for the current species
        df_species = pca_df['species'] == spec
        plt.scatter(pca_df.loc[df_species, 'PCA_1'],
                    pca_df.loc[df_species, 'PCA_2'],
                    color=colors[spec])

    # Format scatterplot
    plt.legend(species)
    plt.xlabel('Principal Component #1')
    plt.ylabel('Principal Component #2')
    plt.title('Principal Component Analysis with 2 Elements\n')

    print(f"\tHistograms have been computed.")

    # II.
    # Call 'save_plot' function from helpers.py module to save the plot as a PNG
    file_path = helpers.save_plot('results', file_name, plt)
    
    # Display message box with "OK" and "Cancel" buttons
    response = messagebox.askokcancel("Principal Componenent Analysis", "A scatter plot of the computed PCA will be created and saved in the results directory. Please click OK to open the file.")

    # III.
    # If response is True save & open the PNG, otherwise just save the PNG
    if response:
        file_path
        print(f"\tPlot saved as PNG.")
        plt.show()
        print(f"\tUser opened the plot.")
    else:
        file_path
        print(f"\tPlot saved as PNG")
        print(f"\tUser closed the pop-up.")
    
    # https://stackoverflow.com/questions/16676101/print-the-approval-sign-check-mark-u2713-in-python
    print("\n\t\u2713 Pairplot function successfully finished.")

def perform_PCA_options(df,df_cleaned):
    '''
    Helper function triggered by menu.py (button V in the GUI), displaying a message box which prompts the user 
    to generate a scatter plot with the PCA using either the original DataFrame (df) or the cleaned DataFrame (df_cleaned) without outliers. 
    Depending on the user's choice, it calls the generate_pairplot() function with the corresponding DataFrame.
    '''

    response = messagebox.askyesno("Compute PCA", "Would you like to perform the PCA without the outliers?")

    if response:
        perform_PCA(df_cleaned, 'V.PCA_cleaned.png')
    else:
        perform_PCA(df, 'V.PCA_original.png')