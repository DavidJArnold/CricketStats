import ruamel.yaml as yaml
import glob


def print_match_summary(info) -> None:
    team1 = info['teams'][0]
    team2 = info['teams'][1]
    if 'venue' in info:
        venue = info['venue']
        team_venue = f'{team1} v {team2} at {venue}.'
        if 'city' in info:
            team_venue = f'{team1} v {team2} at {venue}, {info["city"]}.'
    elif 'city' in info:
        venue = info['city']
        team_venue = f'{team1} v {team2} at {venue}.'
    else:
        team_venue = f'{team1} v {team2}.'

    outcome = ''
    if 'winner' in info['outcome']:
        winner = info['outcome']['winner']
        try:
            by = info['outcome']['by']
            if 'runs' in by:
                r_margin = info['outcome']['by']['runs']
                if 'innings' in by:
                    outcome = f'{winner} won by an innings and {r_margin} runs.'
                else:
                    outcome = f'{winner} won by {r_margin} runs.'
            if 'wickets' in by:
                w_margin = info['outcome']['by']['wickets']
                if 'innings' in by:
                    outcome = f'{winner} won by an innings and {w_margin} wickets.'
                else:
                    outcome = f'{winner} won by {w_margin} wickets.'
        except KeyError:
            if info['outcome']['method'] == 'Awarded':
                outcome = f'{winner} were awarded the victory.'
            else:
                raise
    elif 'result' in info['outcome']:
        if info['outcome']['result'] == 'draw':
            outcome = 'The match was drawn.'
        elif info['outcome']['result'] == 'tie':
            outcome = 'The match was tied.'
        elif info['outcome']['result'] == 'no result':
            outcome = 'There was no result.'

    print(team_venue + ' ' + outcome)
    return


ball_wickets = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ball_noballs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ball_wides = [0, 0, 0, 0, 0, 0, 0, 0, 0]

files = [f for f in glob.glob("tests_male/*.yaml")]

## To display a single match (for debugging)
# with open(list(files)[216]) as stream:
#     test = yaml.safe_load(stream)
# print(test['info'])
# print_match_summary(test['info'])

for idx, name in enumerate(files):
    with open(name) as stream:
        try:
            test = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    print(f'Match {idx + 1} out of {len(files)}.')
    print_match_summary(test['info'])

    for innings in list(test['innings']):

        for balls in innings[list(innings)[0]]['deliveries']:
            key = list(balls)[0]

            if 'wicket' in balls[key]:
                ball_wickets[int(str(key).split(".")[-1]) - 1] += 1

            if 'extras' in balls[key]:
                if 'noballs' in balls[key]['extras']:
                    ball_noballs[int(str(key).split(".")[-1]) - 1] += 1
                if 'wides' in balls[key]['extras']:
                    ball_wides[int(str(key).split(".")[-1]) - 1] += 1

    print(ball_wickets)
    print(ball_wides)
    print(ball_noballs)

print('Finished')
