import math

def elo_win_probability(elo1: float, elo2: float, C: int=400):
    """
    Returns the probability of player with elo1 winning against
    player with elo2.
    
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
    
    See Also
    --------
    https://en.wikipedia.org/wiki/Elo_rating_system
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
    
    p1_win_probability = elo_win_probability(elo1, elo2)
    new_elo1 = elo1 + K * (outcome - p1_win_probability)
    delta_elo = new_elo1 - elo1
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
    
    player_count = len(elos)
    mod_K = K / (player_count - 1)
    delta_elos = [ 0 for _ in range(player_count)]
    winning_score = max(scores)

    for player1 in range(player_count):
        for player2 in range(player_count):
            if player1 == player2:
                continue

            # any player can win/draw/lose to any other player by score
            # outcome = 0 if scores[player1] < scores[player2] else 1 if scores[player1] > scores[player2] else 0.5

            # any losers lose to winners and draw with other losers / any winners win over losers and draw with other winners
            player1_win = scores[player1] == winning_score
            player2_win = scores[player2] == winning_score
            outcome = 0 if player2_win and not player1_win else 1 if player1_win and not player2_win else 0.5

            delta_elo = compute_elo_adjustment_2(elos[player1], elos[player2], outcome, mod_K)
            delta_elos[player1] += delta_elo

    return delta_elos
