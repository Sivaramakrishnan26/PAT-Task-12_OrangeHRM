from pages.login_page import LoginPage
from datetime import datetime
import pandas as pd
import pytest
import os


def get_login_data():
    login_data = []
    # Read the Excel file into a DataFrame
    df = pd.read_excel('data/login_data.xlsx')  # Update the path to your Excel file if needed

    # Iterate through the rows of the DataFrame and extract username and password
    for index, row in df.iterrows():
        username = row['USERNAME']
        password = row['PASSWORD']
        login_data.append((username, password))

    return login_data


def update_excel(username, password, test_result, tester_name):
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    file_path = 'data/login_data.xlsx'
    temp_file_path = 'data/login_data_temp.xlsx'

    try:
        # Load the existing Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return

    # Ensure necessary columns are present and of type string
    for col in ["DATE", "TIME OF TEST", "NAME OF TESTER", "TEST RESULT"]:
        if col not in df.columns:
            df[col] = ""  # Add missing columns with empty strings

    df["DATE"] = df["DATE"].astype(str)
    df["TIME OF TEST"] = df["TIME OF TEST"].astype(str)
    df["NAME OF TESTER"] = df["NAME OF TESTER"].astype(str)
    df["TEST RESULT"] = df["TEST RESULT"].astype(str)

    # Update the DataFrame with the test result for the matching username and password
    record_found = False
    for index, row in df.iterrows():
        if row["USERNAME"] == username and row["PASSWORD"] == password:
            df.at[index, "DATE"] = current_date
            df.at[index, "TIME OF TEST"] = current_time
            df.at[index, "NAME OF TESTER"] = tester_name
            df.at[index, "TEST RESULT"] = test_result
            record_found = True
            break

    if not record_found:
        print(f"No matching record found for username: {username} and password: {password}")
        return

    try:
        # Save the updated DataFrame to a temporary file
        with pd.ExcelWriter(temp_file_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        # Replace the original file with the temporary file
        os.replace(temp_file_path, file_path)
    except Exception as e:
        print(f"Error writing to the Excel file: {e}")
        # Optionally, handle the temporary file cleanup here
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@pytest.mark.usefixtures("setup")
class TestLogin:
    @pytest.mark.parametrize("username, password", get_login_data())
    def test_login(self, username, password):
        login_page = LoginPage(self.driver)
        login_page.login(username, password)

        # Replace 'Tester_Name' with the actual tester's name or get it dynamically
        tester_name = "Sivaramakrishnan T"

        # Check if the login was successful by verifying the presence of 'dashboard' in the URL
        if "dashboard" in self.driver.current_url:
            update_excel(username, password, "Passed", tester_name)
        else:
            update_excel(username, password, "Failed", tester_name)

        # Assert that the login was successful
        assert "dashboard" in self.driver.current_url
