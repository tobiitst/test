
<!DOCTYPE HTML>


<HEADER>
<div align = "center">
<H1>Log In<H1>
</div>

<BODY>
<div class="container" style="width: 250px;">

        <label for="inputUsername" class="sr-only">Username</label>
        <input type="username" id="inputUsername" class="form-control" placeholder="Username" required autofocus>
        <label for="inputPassword" class="sr-only">Password</label>
        <input type="password" id="inputPassword" class="form-control" placeholder="Password" required>
        <button onClick = "checkDetails()" class="btn btn-lg btn-primary btn-block">Log in</button>
<?PHP
$username = "admin";
$password = "password";
?>


<script>
function checkDetails(){
expectedUsername = "<?PHP echo $username; ?>";
expectedPassword = "<?PHP echo $password; ?>";
var username = document.getElementById('inputUsername').value;
var password = document.getElementById('inputPassword').value;

if(username == expectedUsername && password == expectedPassword)
var newWindow = window.open("mainPannel.php","_self");
else
document.write("Wrong details!");
}
</script>

    </div>
</BODY>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
</HTML>
