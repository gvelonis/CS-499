##!/usr/bin/python3

###################################
#          George Velonis         #
#          SNHU, CS-499           #
#  Algorithms and Data Structures #
#           April 4, 2020         #
###################################

from lib.DLinkedList import DLinkedList


# define class to represent each player
# will be the payload of the node
class Player:
    # all data required to initialize a new player
    def __init__(self, name, position, jersey_num, player_rating):
        self.name = name
        self.position = position
        self.jersey_num = jersey_num
        self.player_rating = player_rating

    # returns a string representation of the player
    def __str__(self):
        string = 'Name: %s, Position: %s, Number: %d, Rating: %d' % (
            self.name, self.position, self.jersey_num, self.player_rating)
        return string

    # ensures that player rating is between 0 and 100
    def __setattr__(self, key, value):
        if (key == 'player_rating') and (not (0 <= value <= 100)):
            raise ValueError("Player rating must be between 0 and 100, inclusive")
        else:
            self.__dict__[key] = value


# roster class
class Roster(DLinkedList):
    def __init__(self):
        DLinkedList.__init__(self)

    def __iter__(self):
        for node in DLinkedList.__iter__(self):
            yield node.data

    # adds a new player to the roster
    # argument is a Player object
    def add_player(self, new_player):
        DLinkedList._add_node(self, new_player)

    def add_player_head(self, new_player):
        DLinkedList._add_node_head(self, new_player)

    def insert_player(self, index_player, new_player):
        # iterate through nodes until finding matching index data
        for node in DLinkedList.__iter__(self):
            if node.data == index_player:
                DLinkedList._insert_node(node, new_player)

    # adds a new player to the roster
    # prompts the user for the player's data
    def add_interactive(self):
        name = input('Enter player\'s name: ')
        position = input('Enter player\'s position: ')
        jersey_num = int(input('Enter player\'s jersey number: '))
        player_rating = int(input('Enter player\'s rating: '))
        new_player = Player(name, position, jersey_num, player_rating)
        self.add_player(new_player)

    # removes a player
    # argument is an integer to match jersey_num to
    def remove_player(self, jersey_num):
        for player in self:
            if player.jersey_num == jersey_num:
                DLinkedList._remove_node(self, player)

    # updates player rating
    # first argument is jersey_num to match to
    # second argument is new rating to set
    def update_rating(self, jersey_num, rating):
        for cursor in self:
            if cursor.jersey_num == jersey_num:
                cursor.player_rating = rating

    # prints the current roster
    # optionally set a min and max rating
    def print(self, max_rating=100, min_rating=0):
        print('ROSTER:')
        for cursor in self:
            if min_rating <= cursor.player_rating <= max_rating:
                print(cursor)

    # bubble sort for sorting by name
    def sort_alpha(self):
        swapped = True

        # empty lists (head and tail are None) or length 1 (head and tail are equal) are already sorted
        if self.head == self.tail:
            return

        while swapped:
            swapped = False
            node = self.head

            while node.next is not None:
                if node.data.name > node.next.data.name:
                    DLinkedList._swap_node(self, node)
                    swapped = True
                node = node.next

    # bubble sort for sorting by position
    def sort_position(self):
        swapped = True

        # empty lists (head and tail are None) or length 1 (head and tail are equal) are already sorted
        if self.head == self.tail:
            return

        while swapped:
            swapped = False
            node = self.head

            while node.next is not None:
                if node.data.position > node.next.data.position:
                    DLinkedList._swap_node(self, node)
                    swapped = True
                node = node.next

    # insertion sort algorithm for sorting jersey numbers
    def sort_jersey(self):
        # empty lists (head and tail are None) or length 1 (head and tail are equal) are already sorted
        if self.head == self.tail:
            return

        sorted_roster = Roster()

        for unsorted_player in self:
            # if sorted head is empty, just add this player
            if sorted_roster.head is None:
                sorted_roster.add_player(unsorted_player)
            # if this player goes before current head
            elif unsorted_player.jersey_num < sorted_roster.head.data.jersey_num:
                sorted_roster.add_player_head(unsorted_player)
            # if this player goes after current tail
            elif unsorted_player.jersey_num > sorted_roster.tail.data.jersey_num:
                sorted_roster.add_player(unsorted_player)
            # otherwise this player is inserted somewhere in between
            # iterate through current sorted list until we find insertion point
            else:
                for sorted_player in sorted_roster:
                    if unsorted_player.jersey_num < sorted_player.jersey_num:
                        sorted_roster.insert_player(sorted_player, unsorted_player)
                        break
        return sorted_roster

    # bubble sort for sorting by rating
    def sort_rating(self):
        swapped = True

        # empty lists (head and tail are None) or length 1 (head and tail are equal) are already sorted
        if self.head == self.tail:
            return

        while swapped:
            swapped = False
            node = self.head

            while node.next is not None:
                if node.data.player_rating < node.next.data.player_rating:
                    DLinkedList._swap_node(self, node)
                    swapped = True
                node = node.next


if __name__ == '__main__':
    # initialize roster LL
    roster = Roster()

    # initial input of 5 players
    roster.add_player(Player('Bergie', 'C', 33, 99))
    roster.add_player(Player('Marchand', 'W', 26, 92))
    roster.add_player(Player('Warren', 'W', 18, 78))
    roster.add_player(Player('Chara', 'D', 72, 95))
    roster.add_player(Player('McDonnel', 'D', 88, 78))

    roster.print()

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
        print('sa - Sort roster by name')
        print('sp - Sort roster by position')
        print('sj - Sort roster by jersey number')
        print('sr - Sort roster by rating')
        print('q - Quit')
        print()

        user_cmd = input('Choose an option: ')

        # print roster
        if user_cmd == 'o':
            roster.print()

        # add player to roster
        elif user_cmd == 'a':
            roster.add_interactive()

        # remove player from roster
        elif user_cmd == 'd':
            player_num = int(input('Enter a jersey number: '))
            roster.remove_player(player_num)

        # update player rating
        elif user_cmd == 'u':
            player_num = int(input('Entery a jersey number: '))
            new_rating = int(input('Enter new player rating: '))
            roster.update_rating(player_num, new_rating)

        # prints all players above a certain rating
        elif user_cmd == 'r':
            rating_threshold = int(input('Enter a rating: '))
            roster.print(100, rating_threshold)

        # resorts the roster according to player rating
        elif user_cmd == 'sr':
            roster.sort_rating()

        # resorts the roster according to jersey number
        elif user_cmd == 'sj':
            roster = roster.sort_jersey()

        # resorts the roster according to name
        elif user_cmd == 'sa':
            roster.sort_alpha()

        # resorts the roster according to position
        elif user_cmd == 'sp':
            roster.sort_position()
