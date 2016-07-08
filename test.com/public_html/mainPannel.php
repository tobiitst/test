<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
</head>
<body>

<div class="jumbotron text-center">
  <h1>Home controller</h1> 
</div>

<div class="container" align="center">
  <h2>Commands</h2>
  <form method="post">
    <input type="submit" name="submit">
  </form>
<?php
if(isset($_POST['submit'])){
$process = shell_exec("hostname -I");
echo $process;}
?>
<form method="post">
  <button id="button1" "type="submit" name="button1"  class="btn btn-success">Start Alert</button>
</form>
<?php
if(isset($_POST['button1'])){
$process = shell_exec("python alert.py");
echo $process;
}
?>
<form method="post">
  <button type="submit" name="button2" class="btn btn-danger">Stop Alert</button>
</form>
<?php 
if(isset($_POST['button2'])){
$process = shell_exec("python stopAlert.py");
}
?>
</div>

</body>
</html>

