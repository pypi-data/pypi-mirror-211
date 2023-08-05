# -*- coding: utf-8 -*-

from dicencards.dice import BunchOfDice, UNLIMITED_REROLL, BUST, BEST_OF_DICE, D4, D6, D8, D10, D12

from dicencards.cards import Color, Suite, Rank, Card, BasicValueModel, ValueModel, Deck

ON_MAX_REROLL = UNLIMITED_REROLL
ON_MIN_REROLL = 0

QUALITY = 'QUALITY'
SUCCESS = 'SUCCESS'
FAIL = 'FAIL'
FUMBLE = 'FUMBLE'
RAISE = 'RAISE'
RAISE_COUNT = 'RAISE_COUNT'

RAISE_STEP = 5

FAIR = 5

TRAIT_DIE_TYPE_CARD_RANK_MAP = {
    Rank.TWO: D4,
    Rank.THREE: D6,
    Rank.FOUR: D6,
    Rank.FIVE: D6,
    Rank.SIX: D6,
    Rank.SEVEN: D6,
    Rank.EIGHT: D6,
    Rank.NINE: D8,
    Rank.TEN: D8,
    Rank.JACK: D8,
    Rank.QUEEN: D10,
    Rank.KING: D10,
    Rank.ACE: D12,
    Rank.JOKER: D12
}

TRAIT_COORDINATION_CARD_COLOR_MAP = {
    Suite.CLUBS: 1,
    Suite.DIAMONDS: 2,
    Suite.HEARTS: 3,
    Suite.SPADES: 4,
}


class DeadLandsValueModel(BasicValueModel):

    def __init__(self):
        super().__init__()
        self.model[Rank.JOKER] = len(self.model) + 1


def check(dice_type: int, number_of_dice: int, target: int):
    bunch = BunchOfDice(number_of_dice, dice_type)
    result = bunch.roll(ON_MAX_REROLL, ON_MIN_REROLL)
    if result[BUST] >= number_of_dice / 2:
        result[QUALITY] = FUMBLE
    elif result[BEST_OF_DICE] < target:
        result[QUALITY] = FAIL
    elif result[BEST_OF_DICE] >= target:
        result[QUALITY] = SUCCESS
        raise_count = (result[BEST_OF_DICE] - target) // RAISE_STEP
        result[RAISE_COUNT] = raise_count
        if raise_count > 0:
            result[QUALITY] = RAISE
    return result


def build_deck():
    cards: list[Card] = []
    excluded_ranks = (Rank.ONE, Rank.KNIGHT, Rank.JOKER)
    for suite in list(Suite):
        for rank in list(Rank):
            if rank not in excluded_ranks:
                card = Card(rank, suite)
                cards.append(card)
    cards.append(Card(Rank.JOKER, color=Color.BLACK))
    cards.append(Card(Rank.JOKER, color=Color.RED))
    deck: Deck = Deck(cards)
    deck.shuffle()
    return deck


def trait_from_card(card):
    die_type = TRAIT_DIE_TYPE_CARD_RANK_MAP[card.rank].side_count
    if card.rank == Rank.JOKER:
        # Les règles ne fournissent aucunes instructions en ce qui concerne la coordination lors du tirage d'un Joker
        coordination = D4.roll()
    else:
        coordination = TRAIT_COORDINATION_CARD_COLOR_MAP[card.suite]
    return BunchOfDice(coordination, die_type)


def character_draw():
    deck: Deck = build_deck()
    hand = deck.draw(12)
    # print(' |'.join(str(c) for c in hand))
    value_model = DeadLandsValueModel()
    hand = value_model.sort(hand, ValueModel.DESC)
    print(' |'.join(str(c) for c in hand))
    # On garde les 10 meilleures cartes sans écarter les "2"
    i = len(hand) - 1
    while len(hand) > 10:
        card: Card = hand[i]
        if card.rank != Rank.TWO:
            del hand[i]
        i = i - 1

    print(' |'.join(str(c) for c in hand))

    trait_dice = []
    for card in hand:
        trait_dice.append(trait_from_card(card))

    print(' | '.join(str(d) for d in trait_dice))
