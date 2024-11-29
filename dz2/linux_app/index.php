<?php
session_start();

if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true) {
    header("Location: login.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Home Page</title>
</head>
<body>
    <p style="text-align:center;"><img src="tux.png" alt="tux"></p>
    <p style="text-align:center;">This is the home page. You logged as <strong> <?php echo $_SESSION["username"]; ?> </strong> </p>
</body>
</html>
