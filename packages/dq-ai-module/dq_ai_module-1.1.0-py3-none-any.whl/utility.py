# Refactored code
import openai
import sys
import pandas as pd
import subprocess
import re
# from api import settings


class DQAI:
    def __init__(self, key):
        openai.api_key = key

    def invoke(self, data, file):
        prompt = (
                f"Analyze the given dataset and generate Data Quality rules specific to the data:\n\n{data}\n\n"
                f"Write Python code for the Rules to execute:\n"
                f"1. Create a function called 'applyRules' that takes the data as input and outputs the errors found based on the rules. Ensure the function handles different data types, including 'float' objects, and doesn't raise any errors. Include error handling mechanisms such as try-except blocks to handle any unexpected issues during execution.\n"
                f"2. Save the output to a CSV file called 'rulesapplication.csv' in the current directory.\n"
                f"3. Import necessary libraries if required.\n"
                f"4. Take input_file as {file}\n"
                f"5. Use '#' before every line except the python code.\n"
                f"6. Be specific with the errors and give proper details of errors.\n"
                f"7. Ensure the generated code checks for the correct data type before performing comparisons and includes error handling mechanisms to avoid raising any errors during execution.\n"
                f"8. Use #~ sign before rules comment\n"
        )
        generated_text = self.generate_code(prompt)
        self.save_and_execute_code(generated_text)

        rules = self._get_rules_from_file("generated_code.py")
        result = {"0": rules, "1": pd.read_csv("rulesapplication.csv")}
        return result

    def invoke_from_dataset(self, data):
        prompt = (
            f"Analyze the given dataset and generate Data Quality rules specific to the data:\n\n{data}\n\n"
            f"Write Python code for the Rules to execute:\n"
            f"1. Create a function called 'applyRules' that takes the data as input and outputs the errors found based on the rules. Ensure the function handles different data types, including 'float' objects, and doesn't raise any errors. Include error handling mechanisms such as try-except blocks to handle any unexpected issues during execution.\n"
            f"2. Save the output to a CSV file called 'rulesapplication.csv' in the current directory.\n"
            f"3. Import necessary libraries if required.\n"
            f"4. Do not mention the input file since you are providing only the dataset.\n"
            f"5. Use '#' before every line except the python code.\n"
            f"6. Be specific with the errors and give proper details of errors.\n"
            f"7. Ensure the generated code checks for the correct data type before performing comparisons and includes error handling mechanisms to avoid raising any errors during execution.\n"
            f"8. Use #~ sign before rules comment\n"
        )
        generated_text = self.generate_code(prompt)
        self.save_and_execute_code(generated_text)

        rules = self._get_rules_from_file("generated_code.py")
        result = {"0": rules, "1": pd.read_csv("rulesapplication.csv")}
        return result
    
    def generate_code(self, prompt):
        messages = [
            {"role": "system", "content": "You are a Quality analyst. Use '#' before every line except the python code.\n"},
            {"role": "user", "content": prompt}
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            messages=messages,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response['choices'][0]['message']['content']

    def save_and_execute_code(self, generated_text):
        with open("generated_code.py", "w") as output_file:
            output_file.write(generated_text)
        print("Generated rules and code saved in 'generated_code.py'")

        print("\nExecuting the generated code...\n")
        subprocess.run([sys.executable, "generated_code.py"])

    @staticmethod
    def _get_rules_from_file(generated_code_file):
        with open(generated_code_file, "r") as f:
            comments = [line for line in f.readlines() if line.startswith('#~')]
        return comments

