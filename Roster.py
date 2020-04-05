###################################
#          George Velonis         #
#          SNHU, CS-499           #
#  Algorithms and Data Structures #
#           April 4, 2020         #
###################################


# define class for each linked list node
class Node:
    def __init__(self):
        self.prev_node = None
        self.next_node = None


# define node child class to represent each player
class Player(Node):
    def __init__(self, name, position, jersey_num, player_rating):
        Node.__init__(self)
        self.name = name
        self.position = position
        self.jersey_num = jersey_num
        self.player_rating = player_rating

    def __str__(self):
        string = 'Name: %s, Position: %s, Number: %d, Rating: %d' % (
            self.name, self.position, self.jersey_num, self.player_rating)
        return string


# define the class for the linked list
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_node(self, node):
        # if head is None, list is empty and node should be both head and tail
        if self.head is None:
            self.head = node
            self.tail = node
            return
        # otherwise, set current tail's next to the new node, the new node's previous to current tail
        # then update current tail to the new node
        self.tail.next_node = node
        node.prev_node = self.tail
        self.tail = node

    def __iter__(self):
        cursor = self.head
        while cursor is not None:
            node = cursor
            cursor = cursor.next_node
            yield node


# roster class
class Roster(LinkedList):
    def __init__(self):
        LinkedList.__init__(self)

    def add_player(self, new_player):
        LinkedList.add_node(self, new_player)

    def add_interactive(self):
        name = input('Enter player\'s name: ')
        position = input('Enter player\'s position: ')
        jersey_num = int(input('Enter player\'s jersey number: '))
        player_rating = int(input('Enter player\'s rating: '))
        new_player = Player(name, position, jersey_num, player_rating)
        self.add_player(new_player)

    def remove_player(self, jersey_num):
        for cursor in self:
            if cursor.jersey_num == jersey_num:
                cursor.prev_node.next_node = cursor.next_node
                cursor.next_node.prev_node = cursor.prev_node

    def update_rating(self, jersey_num, rating):
        for cursor in self:
            if cursor.jersey_num == jersey_num:
                cursor.player_rating = rating

    def print(self, max_rating=100, min_rating=0):
        print('ROSTER:')
        for cursor in self:
            if min_rating <= cursor.player_rating <= max_rating:
                print(cursor)

    # TODO: implement sorting functions
    def sort_alpha(self):
        pass

    def sort_position(self):
        pass

    def sort_jersey(self):
        pass

    def sort_rating(self):
        pass


if __name__ == '__main__':
    # initialize roster LL
    roster = Roster()

    # program requires initial input of 5 players
    # statically define initial 5 for testing
    player = Player('Bergie', 'C', 33, 99)
    roster.add_node(player)
    player = Player('Marchand', 'W', 26, 92)
    roster.add_node(player)
    player = Player('Warren', 'W', 18, 78)
    roster.add_node(player)
    player = Player('Chara', 'D', 72, 95)
    roster.add_node(player)
    player = Player('McDonnel', 'D', 88, 78)
    roster.add_node(player)

    # iterate through adding players to roster
    # for i in range(5):
    #     roster.add_interactive()

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
        # does not print players in any order. could be refactored to iterate over a sorted list of keys
        elif user_cmd == 'r':
            rating_threshold = int(input('Enter a rating: '))
            roster.print(100, rating_threshold)
