<?php
function OpenCon()
{
$dbhost = "localhost";
$dbuser = "php";
$dbpass = "phppasswd";
$db = "simple_app";
$conn = new mysqli($dbhost, $dbuser, $dbpass,$dbname) or die("Connect failed: %s\n". $conn -> error);
return $conn;
}
function CloseCon($conn)
{
$conn -> close();
}
