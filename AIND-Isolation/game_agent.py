"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def winner_or_loser(game, player):
    ''' Return winner or loser of the game
        Boiler plate function called from all heuristics
    '''
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return None

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
 
    return bonus_improved_score(game, player)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    #return favor_edges(game, player)  # got max ~68%
    # return weighted_difference_heuristic(game, player)  # got 64% - 71%
    return weighted_moves_ratio(game, player)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
 
    return favor_center_heuristic(game, player)

def custom_score_4(game, player):
    '''  Additional custom function
    '''
    return weighted_difference_heuristic(game, player)


def central(game, move):
    '''  Get distance of move (row,col) from center of the game board
    '''
    y, x = move   # row, col;  h, w of the move
    cw, ch = game.width / 2., game.height / 2. 

    return float( (ch - y)**2 + (cw - x)**2 )


def bonus_improved_score(game, player):
    '''  Improved score - difference from center
    '''
    rv = winner_or_loser(game, player)
    if rv is not None:
        return rv

    self_moves = len(game.get_legal_moves(player))
    opponent   = game.get_opponent(player)
    opp_moves  = len(game.get_legal_moves(opponent))

    self_location = game.get_player_location(player)

    return float( self_moves - opp_moves - central(game, self_location))

def favor_edges_heuristic(game, player):
    '''  Return +ve coefficient the more the player is towards edges. 
    '''

    rv = winner_or_loser(game, player)
    if rv is not None:
        return rv

    opponent     = game.get_opponent(player)
    center       = game.width / 2.

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(opponent)

    own_delta_x  = abs(center - own_location[0])
    own_delta_y  = abs(center - own_location[1])

    opp_delta_x  = abs(center - opp_location[0])
    opp_delta_y  = abs(center - opp_location[1])

    own_moves    = len(game.get_legal_moves(player))
    opp_moves    = len(game.get_legal_moves(opponent))

    return float(5 * (own_moves - opp_moves) + 
                (own_delta_x + own_delta_y) - (opp_delta_x + opp_delta_y))

def favor_center_heuristic(game, player):
    ''' Return -ve coefficient the more the player is towards center
    '''

    rv = winner_or_loser(game, player)
    if rv is not None:
        return rv

    opponent     = game.get_opponent(player)
    center       = game.width / 2.

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(opponent)

    own_delta_x  = abs(center - own_location[0])
    own_delta_y  = abs(center - own_location[1])

    opp_delta_x  = abs(center - opp_location[0])
    opp_delta_y  = abs(center - opp_location[1])

    own_moves    = len(game.get_legal_moves(player))
    opp_moves    = len(game.get_legal_moves(opponent))

    return float(5 * (own_moves - opp_moves) - 
                (own_delta_x + own_delta_y) + (opp_delta_x + opp_delta_y))

def weighted_difference_heuristic(game, player):
    ''' Return a difference b/w Self Moves^2 - Opponent Moves^2, weighted by 1.5
    '''
    rv = winner_or_loser(game, player)
    if rv is not None:
        return rv

    opponent     = game.get_opponent(player)

    own_moves    = len(game.get_legal_moves(player))
    opp_moves    = len(game.get_legal_moves(opponent))

    return float( 1.5 * own_moves ** 2 -   opp_moves ** 2)

def weighted_moves_ratio(game, player):
    '''  Ratio of Own Moves / Opponent Moves
    '''
    rv = winner_or_loser(game, player)
    if rv is not None:
        return rv

    opponent     = game.get_opponent(player)

    own_moves    = len(game.get_legal_moves(player))
    opp_moves    = len(game.get_legal_moves(opponent))

    if own_moves == 0: return float('-inf')
    if opp_moves == 0: return float('inf')

    return float(1.5 * own_moves / opp_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def active_player(self, game):
        '''  Return True if game is self, else return False
        '''
        return game.active_player == self 

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # call the recursive helper; return its move value
        (move, score) =  self._minimax_move(game, depth)
        return move

    def _minimax_move(self, game, depth):
        ''' Minimax implementation
            Returns (move, score) using recursion
        '''

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves() 
        
        best_move = (-1 , -1)
        if legal_moves is not None and len(legal_moves) > 0:
            best_move = legal_moves[0]

        if depth == 0:  # or not legal_moves:
            return ( best_move, self.score(game, self) )

        optimal_func =  None
        

        # 0 - find who is active player
        if self.active_player(game):   # i.e. WE are the active player --> MAXimize the score
            # for MAX - find the max value
            best_result = float("-inf")
            optimal_func    =  max

        else:    # Opponent is active player --> MINimize score 
            # for MIN - find the min value
            best_result = float("inf")
            optimal_func    = min

        for move in legal_moves:
            next_state = game.forecast_move(move)
            _, score = self._minimax_move(next_state, depth-1)  # recurse - for next game state
            if optimal_func(best_result, score) == score:
                best_move, best_result = move, score
                    
        return (best_move, best_result)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if legal_moves is not None and len(legal_moves) > 0:
            best_move = legal_moves[0]
        
        depth = 1 

        try:
            new_move = best_move 
            while True:
                new_move = self.alphabeta(game, depth)
                best_move = new_move
                depth += 1

        except SearchTimeout:
            pass
        
        return best_move

    def active_player(self, game):
        ''' Return True if self == game
        '''
        return game.active_player == self

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # ## Run the recursive alphabeta
        (move, score) = self._alphabeta_recursive(game, depth, alpha, beta, self.active_player(game))
        
        return move
        
        # return self._test_alphabeta(game, depth, alpha, beta)   ## Didnt work that great

    
    def _test_alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf") ):
        '''  ALTERNATE AlphaBeta -- to reduce forfeits. 
            Uses self.min_value() and self.max_value()
        '''
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = (-1, -1)
        best_value = float('-inf')

        legal_moves = game.get_legal_moves()

        for move in legal_moves:
            # get new value for new state of game
            new_value = max(best_value, self.min_value(game.forecast_move(move), depth-1, alpha, beta ))
            if new_value > best_value:
                best_value = new_value
                best_move  = move 

            if best_value >= beta:
                return best_move
            alpha = max(alpha, best_value)
        
        return best_move

    def min_value(self, game, depth, alpha, beta):
        ''' Return MIN
        '''
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        min_value = float('inf')

        legal_moves = game.get_legal_moves()
        # return current state of game
        if depth == 0 or not legal_moves:
            return self.score(game, self)

        for move in legal_moves:
            min_value = min(min_value, self.max_value(game.forecast_move(move), depth-1, alpha, beta))
            # check
            if min_value <= alpha:
                return min_value
            # update beta
            beta = min(beta, min_value)

        return min_value

    def max_value(self, game, depth, alpha, beta):
        '''  Return MAX
        '''

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        max_value = float('-inf')

        legal_moves = game.get_legal_moves()
        # return current state of game
        if depth == 0 or not legal_moves:
            return self.score(game, self)    # current utility of the game

        for move in legal_moves:
            max_value = max(max_value, self.min_value(game.forecast_move(move), depth-1, alpha, beta))

            # check
            if max_value >= beta:
                return max_value

            # update alpha
            alpha = max(alpha, max_value)

        return max_value
    
    def _alphabeta_recursive(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing=True):
        '''  Main implementation of  Depth-limited AlphaBeta recursively
             Returns (move, value) tuple for every depth

             This now completely eliminates forfeits

        ''' 
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        # best_move   = legal_moves[0] if legal_moves is not None else (-1, -1)

        best_move = (-1, -1)
        if legal_moves is not None and len(legal_moves) > 0:
            best_move = legal_moves[0]

        if depth <= 0:
            return best_move, self.score(game, self)

        # best_move = None
        if maximizing:      # Maximize for Self
            best_value = float("-inf")
            for move in legal_moves:
                # get next game state
                next_state = game.forecast_move(move)
                # get next game score
                _, value = self._alphabeta_recursive(next_state, depth-1, alpha, beta, False)
                # check alpha
                alpha = max(alpha, value)
               
                if value > best_value:
                    best_value, best_move = value, move
                
                if alpha >= beta:
                    break
        else:           # Minimize for Opponent
            best_value = float('inf')
            for move in legal_moves:
                # get next game state
                next_state = game.forecast_move(move)
                # get next game score
                _, value = self._alphabeta_recursive(next_state, depth-1, alpha, beta, True)
                ## check beta
                beta = min(beta, value)
                
                if value < best_value:
                    best_value, best_move = value, move 

                if alpha >= beta:
                    break
        
        return best_move, best_value
