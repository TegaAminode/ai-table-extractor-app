from google import genai
import sys,os

# Set Gemini API Key
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)
# System instruction
class SystemMessage():
    def __init__(self):
        self.instruction = """Extract the table and its data accurately as csv format"""
        self.table_validation = """Check if the table has merged columns, merged rows or both.\n
        Table Validate:\n
        Iterate through these and respond with the answer that exactly suits the table condition.\n
        1. If table has merged columns: Yes, merged column,\n
        2. If table has merged rows: Yes, merged rows\n
        3. If table has both merged columns and merged rows: Yes, merged column and merged rows\n
        4. Else: No, merged rows or merged columns"""

def main(i):
    # Construct class systemMessage
    sysMessage = SystemMessage()
    r,mr = ocr_extractor(i,sysMessage.instruction,sysMessage.table_validation)
    file_names = ['output_merged.csv','output.csv','output_merged_nothing.csv']

    if mr.text  == "Yes, merged column and merged rows":
        print('Saving merged table now...')
        try:
            with open(file_names[0],'w') as file:
                file.write(r.text)
                return f'File Saved as {file_names[0]}'
        except PermissionError:
            sys.exit("Close file")

    elif mr.text == "No, merged rows or merged columns":
        print('Saving now...')
        # Save generated output
        try:
            with open(file_names[1],'w') as file:
                file.write(r.text)
                return f'File Saved as {file_names[1]}'
        except PermissionError:
            sys.exit("Close file")
    else:
        print('Saving now...')
        try:
            with open(file_names[2],'w') as file:
                file.write(r.text)
                return f'File Saved as {file_names[2]}'
        except PermissionError:
            sys.exit("Close file")

# Upload your file
def user_input():
    try:
        if len(sys.argv) == 2:
            uploaded_file = client.files.upload(file=sys.argv[1])
            return uploaded_file
        else:
            return sys.exit("Wrong file")
    except ValueError:
      return exit("Wrong Input")
# Extract table with model
def ocr_extractor(f,instruction,table_validate):
    # Extract simple header table's using AI model
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = [instruction, f]
    )

    # Extract merged rows and columns table
    merged_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[table_validate, f]
    )
    return response,merged_response

if __name__ == '__main__':
    main()
