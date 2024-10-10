# DBFunctionApp

### Run Local
1. Install Azure Core Tools using the link: https://github.com/Azure/azure-functions-core-tools
2. Install Python version 3.11 here: https://www.python.org/downloads

3. Put local.settings.json and certificate to database to your root directory
4. Open the directory terminal
5. Create the virtual environment (.venv) and install dependencies using commands
   ```
   py -3.11 python -m venv .venv
   .venv/Scripts/activate
   pip install -r requirements.txt
   ```
7. Make sure you are in the root folder
8. Run the command `func start`

You can edit the function using Visual Studio Code.
For GET Request, you can use your browser
For POST Request, please kindly use Postman
