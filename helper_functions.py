# This file contains some useful code to be used by other files
import datetime
import ruamel.yaml as yaml


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


def bbl_innings_info(game, innings):
    GROUND = game['info']['venue']  # ground the game was played at
    if GROUND == 'Western Australia Cricket Association Ground':
        GROUND = 'W.A.C.A. Ground'
    elif GROUND == 'Brisbane Cricket Ground, Woolloongabba':
        GROUND = 'Brisbane Cricket Ground'
    if isinstance(game['info']['dates'][0], datetime.date):
        date_dt = game['info']['dates'][0]
    elif isinstance(game['info']['dates'][0], str):
        date_dt = datetime.datetime.strptime(game['info']['dates'][0], '%Y-%m-%d').date()
    DATE = date_dt.isoformat()
    SEASON = int((date_dt - datetime.date(2010, 8, 1)) / datetime.timedelta(
        days=365))  # which bbl season? 2011/12 season is season 1
    INNINGS = 1 if list(innings)[0] == '1st innings' else 2  # first or second innings
    BATTING_TEAM = innings[list(innings)[0]]['team']  # batting team
    BOWLING_TEAM = [S for S in game['info']['teams'] if S != BATTING_TEAM][0]  # bowling team

    return GROUND, DATE, SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM


def bbl_extract_over_data(game):
    output = []

    # iterate through the innings' in the match
    for innings in list(game['innings']):
        # empty arrays which hold over-by-over information
        r_over = [0 for _ in range(0, 20)]  # runs in each over
        b_over = [0 for _ in range(0, 20)]  # balls in each over
        legal_balls = [0 for _ in range(0, 20)]  # legal balls in each over (excluding wides/no balls)
        w_over = [0 for _ in range(0, 20)]  # wickets in each over

        # information about the innings
        GROUND, DATE, SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM = bbl_innings_info(game, innings)

        # iterate through the balls in the innings
        for ball in innings[list(innings)[0]]['deliveries']:
            key_name = list(ball.keys())[0]  # delivery in the form a.b, 1.2 is the second ball in the second over
            over = int(str(key_name).split('.')[0])  # the number of completed overs

            r_over[over] += ball[key_name]['runs']['total']  # add runs scored on this ball to over total
            b_over[over] += 1  # add one to count of balls in the over
            legal_balls[over] += 1
            if 'extras' in ball[key_name]:
                if 'wides' in ball[key_name]['extras'] or 'noballs' in ball[key_name]['extras']:
                    legal_balls[over] -= 1
            if 'wicket' in ball[key_name]:
                w_over[over] += 1  # add to the wicket count
                # NOTE: Doesn't handle two wickets falling on the same ball

        for overs in range(len(r_over)):  # iterate over overs in the innings
            if b_over[overs] > 0:  # if balls were bowled in an over
                OVER = overs + 1  # over number
                RR = r_over[overs] / b_over[overs]  # run-rate for this over
                N_BALLS = b_over[overs]  # balls bowled in the over
                N_LEGAL_BALLS = legal_balls[over]  # legal balls bowled in the over
                RUNS = r_over[overs]  # runs scored in the over
                WICKETS = w_over[overs]  # wickets taken in the over

                output.append([OVER, RR, N_BALLS, N_LEGAL_BALLS, RUNS,
                               WICKETS, GROUND, DATE, SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM])

    return output


def bbl_extract_wicket_data(game):
    output = []

    # iterate through the innings' in the match
    for innings in list(game['innings']):

        # information about the innings
        GROUND, DATE, SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM = bbl_innings_info(game, innings)

        # iterate through the balls in the innings
        for ball in innings[list(innings)[0]]['deliveries']:
            key_name = list(ball.keys())[0]  # delivery in the form a.b, 1.2 is the second ball in the second over

            if 'wicket' in ball[key_name]:
                OVER, BALL = [int(s) for s in str(key_name).split('.')]  # the number of completed overs
                PLAYER = ball[key_name]['wicket']['player_out']
                METHOD = ball[key_name]['wicket']['kind']
                print(f"{PLAYER} {METHOD} {OVER}.{BALL}")

                output.append([OVER, BALL, PLAYER, METHOD,
                               GROUND, DATE, SEASON, INNINGS, BATTING_TEAM, BOWLING_TEAM])

    return output


def bbl_match_processing(match):
    with open(match) as stream:
        try:
            game = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    processed_match = bbl_extract_over_data(game)
    return processed_match


def bbl_wicket_processing(match):
    with open(match) as stream:
        try:
            game = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    processed_match = bbl_extract_wicket_data(game)
    return processed_match
