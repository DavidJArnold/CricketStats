-- How much data do we have?
SELECT COUNT(DISTINCT bbl.match_info.match_id) matches, 
	COUNT(DISTINCT bbl.ball_info.ball_id) balls, 
	COUNT(DISTINCT bbl.wicket_info.wicket_id) wickets
FROM bbl.ball_info LEFT JOIN bbl.wicket_info USING (ball_id) JOIN bbl.match_info ON bbl.ball_info.match_id=bbl.match_info.match_id;

-- showing each ball_id, and corresponding match_id and wicket_id (if a wicket fell on that ball)
SELECT  ball_info.match_id, ball_info.ball_id, wicket_id
FROM bbl.ball_info LEFT JOIN bbl.wicket_info USING (ball_id) 
	JOIN bbl.match_info ON bbl.ball_info.match_id=bbl.match_info.match_id;

-- Average number of runs per over in each season
SELECT season, over_number+1 over_number, SUM(RUNS)*6/COUNT(*) avg_RR
FROM bbl.ball_info b JOIN bbl.match_info m ON m.match_id=b.match_id
GROUP BY over_number, season
ORDER BY season, over_number;

-- different averaging methods
SELECT SUM(runs)/COUNT(over_number)*6, 6*AVG(runs) FROM bbl.ball_info GROUP BY over_number;

-- Get deviation from all-seasons average run rate per over (2 methods)
WITH
    m1 AS ( -- average run-rate per over in each season
        SELECT season, over_number, 6*SUM(runs)/COUNT(*) RR
        FROM bbl.ball_info b JOIN bbl.match_info m ON b.match_id=m.match_id
        GROUP BY season, over_number
        ),
    m2 AS ( -- overall average run-rate per over
        SELECT over_number, 6*SUM(runs)/COUNT(*) mean
        FROM bbl.ball_info
        GROUP BY over_number)
SELECT m1.over_number, season, RR, mean, RR-mean deviation
FROM m1 JOIN m2 WHERE m1.over_number=m2.over_number
ORDER BY season, m1.over_number;

WITH
    average_per_over AS ( -- overall average run-rate per over
        SELECT over_number, 6*AVG(runs) AS mean
        FROM bbl.ball_info
        GROUP BY over_number)
SELECT ball_info.over_number, season, mean, 6*AVG(runs) RR, 6*AVG(runs)-mean deviation
FROM bbl.match_info JOIN average_per_over JOIN bbl.ball_info
WHERE average_per_over.over_number=ball_info.over_number AND ball_info.match_id=match_info.match_id
GROUP BY season, over_number
ORDER BY season, over_number;

-- wickets per over per season
SELECT m.season, b.over_number+1 over_number, COUNT(*) num_wickets
FROM bbl.wicket_info w JOIN bbl.ball_info b JOIN bbl.match_info m WHERE w.match_id=m.match_id AND w.ball_id=b.ball_id
GROUP BY season, over_number
ORDER BY season, over_number;

-- Porportion of wickets falling per over in each season
WITH totals AS (SELECT m.season, COUNT(*) total -- total wickets per season
				FROM bbl.wicket_info w JOIN bbl.ball_info b JOIN bbl.match_info m WHERE w.ball_id=b.ball_id AND m.match_id=w.match_id
				GROUP BY season)
SELECT m.season, b.over_number+1 over_number, COUNT(*) num_wickets, total, COUNT(*)/total proportion
FROM bbl.wicket_info w JOIN bbl.ball_info b JOIN bbl.match_info m JOIN totals WHERE w.match_id=m.match_id AND w.ball_id=b.ball_id AND m.season=totals.season
GROUP BY season, over_number
ORDER BY season, over_number;

-- List the grounds that have hosted BBL games, and how many games they've hosted
SELECT row_number() over (ORDER BY ground) id, ground, COUNT(*) games_played FROM bbl.match_info GROUP BY ground;

-- At what score do wickets happen?
SELECT AVG(score), VARIANCE(score), wicket_num FROM bbl.wicket_info JOIN bbl.ball_info ON wicket_info.ball_id=ball_info.ball_id WHERE wicket_num>0 GROUP BY wicket_num ORDER BY wicket_num;