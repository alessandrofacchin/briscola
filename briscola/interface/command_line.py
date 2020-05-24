class UserInterface(object):

    def __init__(self):
        pass

    @staticmethod
    def show_state(hand_cards, played_card, middle_card):
        print('Current state:\n\r\tPlayer Cards:')
        for idx, card in enumerate(hand_cards):
            print('\t\t%d) %s' % (idx, card.get_name()))
        print('\tOn the table:')
        if played_card:
            print('\t\t%s' % (played_card.get_name()))
        else:
            print('\t\tNothing')
        print('\tMiddle card:')
        if middle_card:
            print('\t\t%s' % (middle_card.get_name()))
        else:
            print('\t\tNothing')

    @staticmethod
    def get_choice() -> int:
        return int(input('Enter Card Number: \n\r\t'))
