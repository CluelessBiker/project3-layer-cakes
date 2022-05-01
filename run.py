import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('layer-cakes')

def recipes_ratings():
    """
    Displays the available recipes to choose from along with their user ratings,
    """
    print('Below you shall find a list of available recipes, along with their ratings.\n')
    print('Please select from the available options to continue.\n')


def main():
    """
    Call all program functions.
    """
    print(recipes_ratings())


print("Welcome to Layer Cakes. Let's get started!\n")
main()

