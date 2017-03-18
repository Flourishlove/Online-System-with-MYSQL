<?php
//include config
require_once('includes/config.php');
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="bootstrap-3.3.7/docs/favicon.ico">

    <title>New User</title>

    <!-- Bootstrap core CSS -->
    <link href="bootstrap-3.3.7/docs/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="style/custom.css" rel="stylesheet">

  </head>

  <body>
    <div class="container">
      <h2>New User</h2>

      <?php
        if(isset($_POST['submit'])){
            extract($_POST);

            if($password != $passwordConfirm){
                $error[] = 'Passwords do not match.';
            }
            if(!isset($error)){
                $hashedpassword = $user->password_hash($password, PASSWORD_BCRYPT);

                try {
                    $stmt = $db->prepare('INSERT INTO USER (Email, Username, Password, UserType, Title, UCity, UState) VALUES (:email, :username, :password, :userType, :title, :ucity, :ustate)') ;
                    $stmt->execute(array(
                    ':email' => $email,
                    ':username' => $username,
                    ':password' => $hashedpassword,
                    ':userType' => $userType,
                    ':title' => $title,
                    ':ucity' => $ucity,
                    ':ustate' => $ustate
                    ));
                    header('Location: index.php');
                    exit;
                } catch(PDOException $e) {
                    echo $e->getMessage();
                }
            }
        }
      ?>

      <form action='' method='post'>
        <p><label>Email</label><br />
        <input type='text' name='email' value='<?php if(isset($error)){ echo $_POST['email'];}?>' required></p>

        <p><label>Username</label><br />
        <input type='text' name='username' value='<?php if(isset($error)){ echo $_POST['username'];}?>' required></p>

        <p><label>Password</label><br />
        <input type='password' name='password' value='<?php if(isset($error)){ echo $_POST['password'];}?>' required></p>

        <p><label>Confirm Password</label><br />
        <input type='password' name='passwordConfirm' value='<?php if(isset($error)){ echo $_POST['passwordConfirm'];}?>' required></p>

        <div class="form-group">
        <label for="exampleSelect1">User Type</label>
        <select class="form-control" name="userType">
          <option>City Official</option>
          <option>City Scientist</option>
        </select>
        </div>

        <p><label>Title</label><br />
        <input type='text' name='title' value='<?php if(isset($error)){ echo $_POST['username'];}?>'></p>

        <div class="form-group">
        <label for="Select1">City</label>
        <select class="form-control" name="ucity">
          <option>City1</option>
          <option>City2</option>
        </select>
        </div>

        <div class="form-group">
        <label for="Select1">State</label>
        <select class="form-control" name="ustate">
          <option>State1</option>
          <option>State2</option>
        </select>
        </div>

        <p><input class="btn btn-primary" type='submit' name='submit' value='Register'></p>
      </form>

    </div><!-- /.container -->

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="bootstrap-3.3.7/assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="bootstrap-3.3.7/docs/dist/js/bootstrap.min.js"></script>
  </body>
</html>