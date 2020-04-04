###################################
#          George Velonis         #
#          SNHU, CS-499           #
#  Algorithms and Data Structures #
#           April 4, 2020         #
###################################

# initialize the dictionary that will hold the players and their ratings
# the key is the players jersey number, the value is the rating
roster = {}

# program requires initial input of 5 players
# for loop will repeat 5 times
# jersey_num is better than just num, player_rating is better than just rating
# because 'num' you don't know what it is for, with 'rating' you don't know what is being rated
for i in range(5):
    jersey_num = int(input('Enter player %d\'s jersey number: \n' % (i + 1)))
    player_rating = int(input('Enter player %d\'s rating: \n\n' % (i + 1)))
    roster[jersey_num] = player_rating

# roster is a dict with is inherently unordered. we can sort the keys and store them in a list
# now the for loop will iterate through the ordered list of dict keys
keys_sorted = sorted(roster.keys())
print('ROSTER')
for key in keys_sorted:
    print('Jersey number: %d, Rating: %d' % (key, roster[key]))

# this is the main while loop, prints the menu of commands then waits for user input
# repeats after each command until the user quits
user_cmd = ''
while user_cmd != 'q':
    print('\nMENU')
    print('a - Add player')
    print('d - Remove player')
    print('u - Update player rating')
    print('r - Output players above a rating')
    print('o - Output roster')
    print('q - Quit')
    print()

    user_cmd = input('Choose an option: \n')

    # uses the same logic as printing the roster at the beginning
    # code could be improved by moving it to a method and calling the method in both places
    # output roster
    if user_cmd == 'o':
        print('\nROSTER')
        keys_sorted = sorted(roster.keys())
        for key in keys_sorted:
            print('Jersey number: %s, Rating: %d' % (key, roster[key]))

    # add player to roster
    elif user_cmd == 'a':
        jersey_num = int(input('Enter new player\'s jersey number: \n'))
        player_rating = int(input('Enter new player\'s rating: \n\n'))
        roster[jersey_num] = player_rating

    # remove player from roster
    elif user_cmd == 'd':
        jersey_num = int(input('Enter a jersey number: '))
        del roster[jersey_num]

    # update player rating
    # exactly the same code as add player. making it a different option is better for users
    # it allows for more clear verbiage and lets the user feel more in control
    elif user_cmd == 'u':
        jersey_num = int(input('Enter a jersey number: '))
        player_rating = int(input('Enter a new rating for player: '))
        roster[jersey_num] = player_rating

    # prints all players above a certain rating
    # does not print players in any order. could be refactored to iterate over a sorted list of keys
    elif user_cmd == 'r':
        rating_threshold = int(input('Enter a rating: '))
        print('\nABOVE', rating_threshold)
        for key in roster:
            if roster[key] > rating_threshold:
                print('Jersey number: %s, Rating: %d' % (key, roster[key]))

# best practices used include proper use of white space between logical sections of code
# code comments explaining why the decisions were made to use data types
# comments explaining algorithms used
# variable names are distinct and descriptive. python practice is to separate words in variable with _
