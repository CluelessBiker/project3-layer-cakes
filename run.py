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
        average_rating.append(round(average, 2))

    return average_rating


def recipe_titles():
    """
    Function to return a lit of the available recipes titles to choose from.
    """
    recipes = SHEET.worksheet('ratings')
    titles = []
    for ind in range(1, 4):
        title = recipes.col_values(ind)
        titles.append(title[0])

    return titles


def title_and_rating(title, rating):
    """
    Return a list of Recipe titles & ratings together.
    """
    print('Below you shall find a list of available recipes, along with their user ratings.\n')
    
    for title, rating in zip(title, rating):
        print(f'Recipe title: {title}\nUser rating: {rating} / 5 stars\n')

    print('Enter [ 1 ] if you would like to try a new recipe.\n')
    print('Enter [ 2 ] if you would like to submit a rating for a recipe you have already tried.\n')


def rate_or_retrieve():
    """
    Function to determine which option the user would like to proceed with.
    They may either rate a recipe they have tried.
    Or try a new recipe.
    """
    option = input("What'll it be?? [ 1 ] or [ 2 ]:\n")
    if option == '1':
        print("function not yet defined")
    elif option == '2':
        submit_rating()
    else:
        print('Invalid choice. You may only choose 1 or 2\n')
        return rate_or_retrieve()


def submit_rating():
    """
    Function to display recipe names once more, and allow the user to select a title to rate.
    """
    print('\nYou may select one of the following recipes to rate:\n')
    titles = recipe_titles()
    index = 1            
    for title in titles:   
        print(index, title)
        index += 1



def main():
    """
    Call all program functions.
    """
    user_ratings = obtain_user_ratings()
    average_rating = calculate_average_rating(user_ratings)
    recipe_name = recipe_titles()
    title_and_rating(recipe_name, average_rating)
    rate_or_retrieve()
    # submit_rating()
    
    
print("Welcome to Layer Cakes. Let's get started!\n")
main()


