import math
from scipy.special import erfinv

def elo_win_probability(elo1: float, elo2: float, C: int=400):
    """
    Returns the probability of player with elo1 winning against
    player with elo2.
    
    References
    ----------
    https://en.wikipedia.org/wiki/Elo_rating_system

    Parameters
    ----------
    elo1 : float
        The elo of player 1
    elo2 : float
        The elo of player 2
    C : int
        The elo relativity constant, usually 400

    Returns
    -------
    probability : float
        The probability that player 1 will win against player 2, range 0 to 1
    """
    
    # raw
    # qa = math.pow(10, elo1 / C)
    # qb = math.pow(10, elo2 / C)
    # return min(max(qa / (qa + qb), 0), 1)

    # simplified
    return min(max(1.0 / (1.0 + math.pow(10, -(elo1 - elo2) / C)), 0), 1)

def compute_elo_adjustment_2(elo1: float, elo2: float, outcome: float, K: int = 32):
    """
    Returns the adjustment to the elo of player with elo1 based 
    on the outcome of the match against player with elo2.

    References
    ----------
    https://en.wikipedia.org/wiki/Elo_rating_system

    Parameters
    ----------
    elo1 : float
        The elo of player 1
    elo2 : float
        The elo of player 2
    outcome : float
        0 if player 1 lost, 0.5 if draw, 1 if player 1 won
    K : int
        The elo calculation K-factor, max +/- change in elo per game, usually 32

    Returns
    -------
    delta_elo : float
        The change in player 1's elo based on the outcome of the match
    """
    
    p1_win_probability: float = elo_win_probability(elo1, elo2)
    new_elo1: float = elo1 + K * (outcome - p1_win_probability)
    delta_elo: float = new_elo1 - elo1
    return delta_elo

def compute_elo_adjustment_n(elos: list[float], scores: list[int], K: int = 32):
    """
    Returns the adjustment factor for n players given the set of scores.
    Each player can win, draw, or lose against each other player.
    The resulting change in elo is the sum of the result against each opponent.

    Parameters
    ----------
    elos : list[float]
        A list of the elo of each player being considered
    scores : list[int]
        A list of the score of each player, matching order of elos
    K : int
        The elo calculation K-factor, max +/- change in elo per game, usually 32

    Returns
    -------
    delta_elos : list[float]
        The change in each player's elo based on the outcome of the match
    """
    
    player_count: int = len(elos)
    mod_K: float = K / (player_count - 1)
    delta_elos: float = [0] * player_count
    winning_score: int = max(scores)

    for player1 in range(player_count):
        for player2 in range(player_count):
            if player1 == player2:
                continue

            # any losers lose to winners and draw with other losers / any winners win over losers and draw with other winners
            player1_win: bool = scores[player1] == winning_score
            player2_win: bool = scores[player2] == winning_score
            outcome: float = 0 if player2_win and not player1_win else 1 if player1_win and not player2_win else 0.5

            delta_elo: float = compute_elo_adjustment_2(elos[player1], elos[player2], outcome, mod_K)
            delta_elos[player1] += delta_elo

    return delta_elos

def compute_inverse_error(e: float) -> float:
    """
    Returns the inverse error of e.

    Parameters
    ----------
    e : float
        The input value

    Returns
    -------
    inverse_error : float
        The inverse error of e
    """
    
    return math.sqrt(2) * erfinv(2 * e - 1)

def compute_elo_error_margin(wins: int, draws: int, losses: int, confidence: float=0.95, C: int=400) -> float:
    """
    Returns the Elo error margin for a set of results.

    References
    ----------
    https://en.wikipedia.org/wiki/Elo_rating_system
    https://stackoverflow.com/a/31266328
    https://github.com/cutechess

    Parameters
    ----------
    wins : int
        The number of wins
    draws : int
        The number of draws
    losses : int
        The number of losses
    confidence : float
        The confidence level, usually 0.95
    C : int
        The elo relativity constant, usually 400

    Returns
    -------
    error_margin : float
        The Elo error margin
    """
    
    total: int = wins + draws + losses
    if total == 0:
        # no games, no confidence
        return math.inf

    win_rate: float = wins / total
    draw_rate: float = draws / total
    loss_rate: float = losses / total
    win_draw_factor: float = win_rate + (draw_rate / 2)

    win_deviation: float = win_rate * math.pow(1 - win_draw_factor, 2)
    draw_deviation: float = draw_rate * math.pow(0.5 - win_draw_factor, 2)
    loss_deviation: float = loss_rate * math.pow(0 - win_draw_factor, 2)
    total_deviation: float = math.sqrt(win_deviation + draw_deviation + loss_deviation) / math.sqrt(total)

    minimum: float = win_draw_factor + compute_inverse_error(1 - confidence) * total_deviation
    maximum: float = win_draw_factor + compute_inverse_error(confidence) * total_deviation

    if minimum == 0 or maximum == 0:
        # cannot compute confidence due to division by zero
        return math.inf

    min_recip: float = 1 / minimum
    max_recip: float = 1 / maximum
    if min_recip <= 1 or max_recip <= 1:
        # cannot compute confidence due to zero/negative log
        return math.inf

    min_log: float = -C * math.log10(min_recip - 1)
    max_log: float = -C * math.log10(max_recip - 1)

    return abs((max_log - min_log) / 2)
