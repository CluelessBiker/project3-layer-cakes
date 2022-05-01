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


# This function is based on the 'Love Sandwiches' walk through.
def obtain_user_ratings():
    """
    Obtain all user ratings, and return data as a list of lists.
    """
    ratings = SHEET.worksheet('ratings')
    columns = []
    for ind in range(1, 4):
        column = ratings.col_values(ind)
        columns.append(column[1:])

    return columns


# This function is from the 'Love Sandwiches' walk through.
def calculate_average_rating(data):
    """
    Taking the information generated in the obtain_user_ratings function
    And returning an average for all ratings inputted thus far.
    """
    average_rating = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        average_rating.append(round(average))

    return average_rating


def main():
    """
    Call all program functions.
    """
    recipes_ratings()
    # obtain_user_ratings()


print("Welcome to Layer Cakes. Let's get started!\n")
main()
user_ratings = obtain_user_ratings()
calculate_average_rating(user_ratings)

