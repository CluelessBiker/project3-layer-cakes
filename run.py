"""
Import section
"""
import sys
import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('layer-cakes')


def title_and_rating(title, rating):
    """
    Return a list of Recipe titles & ratings together.
    """
    print(' Below you shall find a list of available recipes,')
    print(' along with their user ratings.\n')

    for title, rating in zip(title, rating):
        print(colored(
            (f' Recipe title: {title}\n User rating: {rating} / 5 stars\n'),
            'cyan'))

    print(' Enter "1" if you would like  to try a new recipe.')
    print(' Enter "2" if you would like to submit a rating for a recipe you')
    print(' have already tried.\n')


# This function is based on the 'Love Sandwiches' walk through.
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


def index_titles():
    """
    Function to index available recipe titles
    """
    titles = recipe_titles()
    index = 1
    for title in titles:
        print(colored((f' {index}. {title}'), 'cyan'))
        index += 1


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


# This code was rewritten with the help of a friend, Nick Ludlam.
def calculate_average_rating(data):
    """
    Taking the information generated in the obtain_user_ratings function
    And returning an average for all ratings inputted thus far.
    """
    average_rating = []
    for column in data:
        rating_count = 0
        rating_total = 0

        for num in column:
            if num:
                rating_count += 1
                rating_total += int(num)

        average = rating_total / rating_count
        average_rating.append(round(average, 2))

    return average_rating


def rate_or_retrieve():
    """
    Function to determine which option the user would like to proceed with.
    They may either rate a recipe they have tried.
    Or try a new recipe.
    """
    option = input(" Make your selection, 1 recipe or 2 rating:\n ")
    if option == '1':
        retrieve_recipe()
    elif option == '2':
        submit_rating()
    else:
        print(colored(
            ('\n Invalid choice. You may only choose 1 or 2\n'), 'red'))
        return rate_or_retrieve()


def retrieve_recipe():
    """
    Function to display recipe names once more,
    and allow the user to select a recipe to retrieve.
    """
    print('\n Select the recipe you would like to retrieve.')
    print(' Choose the recipe by the numberical value.\n')

    index_titles()

    selection = input('\n Please select a recipe to retrieve:\n ')

    if selection == '1':
        ingredients_list('chocolate quinoa')
    elif selection == '2':
        ingredients_list('pistachio')
    elif selection == '3':
        ingredients_list('pumpkin')
    else:
        print(colored(('\n Invalid choice.'), 'red'))
        print(colored(
            (' You may only choose one of the listed options.\n'), 'red'))
        return retrieve_recipe()

    print(colored(('\n Happy baking!'), 'magenta'))
    quit_repeat()


def ingredients_list(recipe):
    """
    Function to return an indredients list & full recipe instructions.
    """
    ingredients = SHEET.worksheet(recipe)

    all_rows = []
    for ind in range(1, 5):
        all_col = ingredients.col_values(ind)
        all_rows.append(all_col[1:])

    ingredient = all_rows[0]
    quantity = all_rows[1]
    unit = all_rows[2]
    instructions = all_rows[3]

    print(colored(('\n Ingredients list:\n'), 'magenta'))
    for (ingredient, quantity, unit) in zip(ingredient, quantity, unit):
        print(colored((f' {ingredient} - {quantity}{unit}'), 'cyan'))

    print(colored(('\n Instructions:\n'), 'magenta'))
    for instruction in instructions:
        print(colored((instruction), 'cyan'))


def submit_rating():
    """
    Function to display recipe names once more,
    and allow the user to select a title to rate.
    """
    print('\n Select the recipe you would like to rate.')
    print(' Choose the recipe by the numberical value.')
    print(' Enter a rating between 1-5. Whole numbers ONLY.')
    print(' 1 being the worst, 5 the best.\n')

    index_titles()

    selection = input('\n Please select a recipe to submit a rating for:\n ')
    update_rating = SHEET.worksheet('ratings')

    if selection == '1':
        input_rating = user_ratings()
        update_rating.append_row([input_rating[0], '', ''])
    elif selection == '2':
        input_rating = user_ratings()
        update_rating.append_row(['', input_rating[0], ''])
    elif selection == '3':
        input_rating = user_ratings()
        update_rating.append_row(['', '', input_rating[0]])
    else:
        print(colored(('\n Invalid choice.'), 'red'))
        print(colored(
            (' You may only choose one of the listed options.\n'), 'red'))
        return submit_rating()

    print('\n Thank you for your submission!')
    quit_repeat()


# Assistance came from my fellow student, Mats Simonsson, credited in README.
def user_ratings():
    """
    Accepts the user input to determine if the rating is valid.
    To be used within the 'submit_rating' function.
    """
    rating = []
    while True:
        try:
            star_rating = int(input(' Submit your rating: \n '))
            break
        except ValueError:
            print(colored(
                (' \nYou must enter a number between 1 and 5'), 'red'))
            continue
    if star_rating <= 5:
        rating.append(star_rating)
        return rating
    else:
        print(colored((' \nYou must enter a number between 1 and 5'), 'red'))
        user_ratings()

    return rating


def quit_repeat():
    """
    Function to allow the user to either quit the program,
    or restart it
    """
    print('\n Enter: "R" to restart the application.')
    print('\n Enter: "Q" to quit the application.\n')
    option = input(" Enter your selection:\n ").upper()
    if option == 'R':
        main()
    elif option == 'Q':
        sys.exit('\n Thank you & Good bye!')
    else:
        print(colored((' \nInvalid choice. Enter: R or Q only.\n'), 'red'))
        return quit_repeat()


def main():
    """
    Call all program functions.
    """
    user_ratings = obtain_user_ratings()
    average_rating = calculate_average_rating(user_ratings)
    recipe_name = recipe_titles()
    title_and_rating(recipe_name, average_rating)
    rate_or_retrieve()


print(colored(("\n Welcome to Layer Cakes. Let's get started!"), 'yellow'))
print(colored((" Welcome to Layer Cakes. Let's get started!"), 'cyan'))
print(colored((" Welcome to Layer Cakes. Let's get started!\n"), 'magenta'))
main()
