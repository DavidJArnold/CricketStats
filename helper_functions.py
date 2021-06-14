# This file contains some useful code to be used by other files

def match_summary(info) -> str:
    """Returns a clean display of the match results given the info section of a cricsheet yaml file (TEST MATCHES
    ONLY). This file builds up a string bit-by-bit."""

    # Team information is always included
    team1 = info['teams'][0]
    team2 = info['teams'][1]

    # extract city and stadium information, sometimes there is one or the other, or both, possibly neither
    if 'venue' in info:
        venue = info['venue']
        # We only have the stadium
        team_venue = f'{team1} v {team2} at {venue}.'
        if 'city' in info:
            # We have stadium and city
            team_venue = f'{team1} v {team2} at {venue}, {info["city"]}.'
    elif 'city' in info:
        venue = info['city']
        # We only have the city
        team_venue = f'{team1} v {team2} at {venue}.'
    else:
        # We don't have any information about location
        team_venue = f'{team1} v {team2}.'

    # Now construct outcome string
    # We can have a win or a draw/tie/no result
    if 'winner' in info['outcome']:
        # there is a winner
        winner = info['outcome']['winner']  # this team won
        if 'by' in info['outcome']:  # a normal win
            by = info['outcome']['by']
            if 'runs' in by:  # a win by some number of runs
                margin = info['outcome']['by']['runs']  # the margin in runs
                win_type = 'run' if margin == 1 else 'runs'  # the type of margin
            elif 'wickets' in by:  # a win by some number of wickets
                margin = info['outcome']['by']['wickets']
                win_type = 'wicket' if margin == 1 else 'wickets'
            # now format the outcome string
            if 'innings' in by:
                outcome = f'{winner} won by an innings and {margin} {win_type}.'
            else:
                outcome = f'{winner} won by {margin} {win_type}.'
        else:
            # the win is awarded in some strange way (i.e. England v Pakistan 2006, Pakistan abandoned the game after
            # being accused of ball-tampering, England were later awarded the win)
            if info['outcome']['method'] == 'Awarded':
                outcome = f'{winner} were awarded the victory.'
            else:
                # If the parsing is inadequate or something strange has happened.
                # TODO: Make this an exception raising an error
                outcome = f'{winner} won but I don''t know how.'
    elif 'result' in info['outcome']:
        # If the match wasn't won by a team, there are three options
        if info['outcome']['result'] == 'draw':
            outcome = 'The match was drawn.'
        elif info['outcome']['result'] == 'tie':
            outcome = 'The match was tied.'
        elif info['outcome']['result'] == 'no result':
            outcome = 'There was no result.'

    # format the final string with the venue, team, and result information, and return it
    return team_venue + ' ' + outcome
