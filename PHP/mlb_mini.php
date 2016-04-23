<?php
$dbhost = xxxx
$dbuser = xxxx
$dbpass = xxxx
$dbname = xxxx
$conn = mysqli_connect($dbhost, $dbuser, $dbpass, $dbname);

// TEAM
$team = $_GET['team'];
$team = strtolower(substr($team, 0, 3));

$stmt = $conn->prepare("SELECT teamId FROM team WHERE lower(abbrev)=? AND leagueId in (103, 104)");
$stmt->bind_param('s', $team);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc();
$tid = $row['teamId'];

$stmt = $conn->prepare("SELECT url FROM game WHERE gamedate=? AND (hometeamid=? or awayteamid=?)");
$stmt->bind_param('sdd', date('Ymd'), $tid, $tid);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc();
$gameday_url = $row['url'];

mysqli_close($conn);

$idx = strpos($gameday_url, "gid_");
$gid = substr($gameday_url, $idx + 4);
$mlb_mini_url = sprintf("http://mlb.mlb.com/mlb/gameday/mini.jsp?gid=%1s", $gid);

echo "<div id=\"data\" hidden>$mlb_mini_url</div>";
?>

<script type="text/javascript">
    var dataDiv = document.getElementById('data');
    var url = dataDiv.innerHTML;
    window.open(url, 'mini_win', 'scrollbars=0,resizable=0,width=310,height=400,left=0,top=0');
</script>
