import pandas as pd

# Read the CSV files
students_df = pd.read_csv('students.csv')
datafull_df = pd.read_csv('datafull.csv')

# Print column names to verify the presence of 'Registration' column
print("students_rows.csv columns:", students_df.columns)
print("datafull.csv columns:", datafull_df.columns)

# Check if 'Registration' column exists in both dataframes
if 'Registration' in students_df.columns and 'Registration' in datafull_df.columns:
    # Convert 'Registration' columns to uppercase to handle case sensitivity
    students_df['Registration'] = students_df['Registration'].str.upper()
    datafull_df['Registration'] = datafull_df['Registration'].str.upper()

    # Merge the dataframes on the 'Registration' column
    merged_df = pd.merge(students_df, datafull_df, on='Registration', how='inner')

    # Select the relevant columns (assuming 'Email' and 'Name' are the column names for email addresses and names)
    result_df = merged_df[['Registration', 'Email', 'Name']]

    # Save the result to a new CSV file
    result_df.to_csv('new2.csv', index=False)

    print("New CSV file 'new2.csv' created successfully.")
else:
    print("Error: 'Registration' column not found in one or both CSV files.")