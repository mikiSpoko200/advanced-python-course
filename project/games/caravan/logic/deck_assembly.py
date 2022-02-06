# -*- encoding: utf-8 -*-


class DeckComposition:

    def __init__(self, available_cards: list[Card]) -> None:
        self.available_cards = available_cards
        self.selection_position = len(available_cards) // 2  # to begin with pick some card from the middle
        self.SELECT_CARDs: list[int] = [False] * len(available_cards)  # a bit mask basically, might be handy for display

    def add_card(self) -> None:
        self.SELECT_CARDs[self.selection_position] = True

    def remove_card(self) -> None:
        self.SELECT_CARDs[self.selection_position] = False

    def move_selection(self, direction: HorizontalDirection):
        max_index = len(self.available_cards) - 1
        match direction, self.selection_position:
            case HorizontalDirection.LEFT, 0:
                self.selection_position = max_index
            case HorizontalDirection.LEFT:
                self.selection_position -= 1
            case HorizontalDirection.RIGHT, max_index:
                self.selection_position = 0
            case HorizontalDirection.RIGHT:
                self.selection_position += 1

    def accept_deck(self) -> Deck:
        return Deck([card for card, picked in zip(self.available_cards, self.SELECT_CARDs) if picked])
