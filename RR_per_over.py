import ruamel.yaml as yaml
import glob


def extract_over_data(game):
    output = []
    # iterate through the innings' in the match
    for innings in list(game['innings']):
        # empty arrays which hold over-by-over information
        r_over = [0 for idx in range(0, 20)]  # runs in each over
        b_over = [0 for idx in range(0, 20)]  # balls in each over
        w_over = [0 for idx in range(0, 20)]  # wickets in each over

        # iterate through the balls in the innings
        for ball in innings[list(innings)[0]]['deliveries']:
            key_name = list(ball.keys())[0]  # delivery in the form a.b, 1.2 is the second ball in the second over
            delivery = int(str(key_name).split('.')[-1])  # the b part, the ball in the over
            over = int(str(key_name).split('.')[0])  # the number of completed overs

            r_over[over] += ball[key_name]['runs']['total']  # add runs scored on this ball to over total
            b_over[over] += 1  # add one to count of balls in the over
            if 'wicket' in ball[key_name]:
                w_over[over] += 1  # add to the wicket count
                # NOTE: Doesn't handle two wickets falling on the same ball

        for overs in range(len(r_over)):  # iterate over overs in the innings
            if b_over[overs] > 0:  # if balls were bowled in an over
                OVER = overs + 1  # over number
                RR = r_over[overs] / b_over[overs]  # run-rate for this over
                N_BALLS = b_over[overs]  # balls bowled in the over
                RUNS = r_over[overs]  # runs scored in the over
                WICKETS = w_over[overs]  # wickets taken in the over
                GROUND = game['info']['venue']  # ground the game was played at
                DATE = game['info']['dates'][0]  # date the game was played
                INNINGS = 1 if list(innings)[0] == '1st innings' else 2  # first or second innings
                BATTING_TEAM = innings[list(innings)[0]]['team']  # batting team
                BOWLING_TEAM = [S for S in game['info']['teams'] if S != BATTING_TEAM][0]  # bowling team

                output.append([OVER, RR, N_BALLS, RUNS, WICKETS, GROUND, DATE, INNINGS, BATTING_TEAM, BOWLING_TEAM])

    return output


def match_processing(match):
    with open(match) as stream:
        try:
            game = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    processed_match = extract_over_data(game)
    return processed_match


# files = [f for f in glob.glob("bbl/*.yaml")]

the_match = glob.glob('bbl/524915.yaml')[0]

output = match_processing(the_match)
for o in output:
    print(o)
