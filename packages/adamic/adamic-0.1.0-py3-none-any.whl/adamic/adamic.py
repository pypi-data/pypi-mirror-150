import pandas as pd
import os

def initialize_data_dictionary(dataFrame):
    """
    Creates a shell of data dictionary. Output = Python dict.
    """
    data_dict = {}

    col_names = dataFrame.columns

    for col in col_names:

        data_dict[col] = {
            'Definition': str(""),
            'Type': str(dataFrame[col].dtype),
            'No. of Observations': str(len(dataFrame[col])),
            'Max': "",
            'Min': "",
            'Unique': ""
        }
    
        if dataFrame[col].dtype in ['object', 'bool']:
            data_dict[col]['Max'] = "NA"
        else:
            data_dict[col]['Max'] = str(dataFrame[col].max())

        if dataFrame[col].dtype in ['object', 'bool']:
            data_dict[col]['Min'] = "NA"
        else:
            data_dict[col]['Min'] = str(dataFrame[col].min())

        if len(dataFrame[col].unique()) > 20:
            data_dict[col]['Unique'] = str("Unique values > 20")
        else:
            data_dict[col]['Unique'] = str(dataFrame[col].unique())
    
    pd_dict = pd.DataFrame(data_dict)    

    return pd_dict

def add_dictionary_definition(data_dictionary_df):
    """
    Prompts user to supply definitions for data dictionary. Output = transposed pandas dataframe.
    """

    dict_cols = data_dictionary_df.columns
    definition = 'Definition'

    for col in dict_cols:
        data_dictionary_df[col][definition] = input(f'Define the "{col}" variable. Press "Enter" once done or if you want to define later.')

    pd_dict_transposed = data_dictionary_df.transpose()

    return pd_dict_transposed

def output_dataframe(pd_dict_transposed):
    """
    Prepares output file after user specifies extension preference. Output = .csv,.json, or .xslx file.
    """
    
    project_name = input("What's your project's name?")
    output_type = input("What file extension for your data dictionary? Enter 'csv', 'json', or 'excel'")
        
    if output_type in ["json","JSON","Json",".json","'json'"]:
        file = f'{project_name}_data_dictionary.json'
        json_output = pd_dict_transposed.to_json(file)
        print("Your data dictionary is available at: ", str(os.getcwd() + "/" + file))
        
    elif output_type in ["Excel","excel","EXCEL",".xlsx","'excel'"]:
        file = f'{project_name}_data_dictionary.xlsx'
        json_output = pd_dict_transposed.to_excel(file, sheet_name="Data Dictionary")
        print("Your data dictionary is available at: ", str(os.getcwd() + "/" + file))
        
    else:
        file = f'{project_name}_data_dictionary.csv'
        csv_output = pd_dict_transposed.to_csv(file, encoding='utf-8')
        print("Your data dictionary is available at: ", str(os.getcwd() + "/" + file))
        
def create_data_dictionary(dataFrame):
    """
    Wrapper function to execute the main three functions.
    """
    
    initialized_dict = initialize_data_dictionary(dataFrame)
    defined_dict = add_dictionary_definition(initialized_dict)
    output_dataframe(defined_dict)