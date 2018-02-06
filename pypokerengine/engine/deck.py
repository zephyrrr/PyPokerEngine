from random import shuffle as rshuffle
from .card import Card


class Deck:
    """
    Class representing a deck. The first time we create, we seed the static
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it.
    """
    _FULL_DECK = []

    # def __init__(self):
    #     self.shuffle()

    def shuffle(self):
        if self.cheat:
            return
        # and then shuffle
        self.cards = Deck.GetFullDeck()
        rshuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def __str__(self):
        return Card.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck():
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for suit, val in Card.CHAR_SUIT_TO_INT_SUIT.items():
            for rank in Card.STR_RANKS:
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)

    def __init__(self, deck_ids=None, cheat=False, cheat_card_ids=[]):
        self.cheat = cheat
        self.cheat_card_ids = cheat_card_ids
        self.cards = [cid for cid in deck_ids] if deck_ids else self.__setup()

    def draw_card(self):
        return self.draw(1)

    def draw_cards(self, num):
        return self.draw(num)

    def size(self):
        return len(self.cards)

    def restore(self):
        self.cards = self.__setup()

    # def shuffle(self):
    #     if not self.cheat:
    #         rshuffle(self.cards)

    # serialize format : [cheat_flg, chat_card_ids, deck_card_ids]
    def serialize(self):
        return [self.cheat, self.cheat_card_ids, [card for card in self.cards]]

    @classmethod
    def deserialize(self, serial):
        cheat, cheat_card_ids, deck_ids = serial
        return self(deck_ids=deck_ids, cheat=cheat, cheat_card_ids=cheat_card_ids)

    def __setup(self):
        return self.__setup_cheat_deck() if self.cheat else self.__setup_52_cards()

    def __setup_52_cards(self):
        cards = Deck.GetFullDeck()
        rshuffle(cards)
        return cards

    def __setup_cheat_deck(self):
        cards = [cid for cid in self.cheat_card_ids]
        return cards[::1]

    @property
    def deck(self):
        return self.cards
