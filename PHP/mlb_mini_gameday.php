<?php
$dbhost = 'totals.statcorner.com';
$dbuser = 'msea85';
$dbpass = 'seb10June7410';
$dbname = 'scsax';

// TEAM
$team = $_GET['team'];
$team = substr($team, 0, 3);

$conn = mysqli_connect($dbhost, $dbuser, $dbpass, $dbname);

$stmt = $mysqli->prepare("SELECT teamId FROM team WHERE abbrev=? AND leagueId in (103, 104)");
$stmt->bind_param('s', $team);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc();

$tid = $row['teamId'];

$stmt = $mysqli->prepare("SELECT url FROM game WHERE gamedate=? AND (hometeamid=? or awayteamid=?)");
$stmt->bind_param('sdd', date('Ymd'), $tid, $tid);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc();

// sample URL http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_20/gid_2016_04_20_seamlb_clemlb_1
 $gameday_url = row['url'];

 mysqli_close($conn);

$gid = substr($gameday_url, strpos($gameday_url, "gid_"+4));
$mlb_mini_url = sprintf("http://mlb.mlb.com/mlb/gameday/mini.jsp?gid=%1s", $gid);
echo $mlb_mini_url
# header("Location: $mlb_mini_url");
?>
