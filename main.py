import ruamel.yaml as yaml
import glob
from helper_functions import match_summary

# initialise counting arrays for actions happening on specific balls
ball_wickets = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ball_noballs = [0, 0, 0, 0, 0, 0, 0, 0, 0]
ball_wides = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# the list of match files in the folder tests_male
files = [f for f in glob.glob("tests_male/*.yaml")]

# To display a single match (for debugging), use the following:
# with open(list(files)[216]) as stream:
#     test = yaml.safe_load(stream)
# print(test['info'])
# print_match_summary(test['info'])

# iterate through each match
for idx, name in enumerate(files):
    # open match file and attempt to parse yaml
    with open(name) as stream:
        try:
            test = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # print a summary of the match information
    print(f'Match {idx + 1} out of {len(files)}.')
    print(match_summary(test['info']))

    # iterate through the innings' in the match
    for innings in list(test['innings']):
        # iterate through the balls in the innings
        for balls in innings[list(innings)[0]]['deliveries']:
            # the delivery information is the only key-value pair in the ball field
            # the key is in the format 23.4, meaning 4th ball of the 24th over (0.1 is the first ball of the innings)
            key = list(balls)[0]

            # did a wicket fall?
            if 'wicket' in balls[key]:
                # add 1 to the count of wickets for the appropriate ball number
                ball_wickets[int(str(key).split(".")[-1]) - 1] += 1

            # was there an extra?
            if 'extras' in balls[key]:
                if 'noballs' in balls[key]['extras']:
                    ball_noballs[int(str(key).split(".")[-1]) - 1] += 1
                if 'wides' in balls[key]['extras']:
                    ball_wides[int(str(key).split(".")[-1]) - 1] += 1

    # display current results
    print(ball_wickets)
    print(ball_wides)
    print(ball_noballs)

print('Finished')
