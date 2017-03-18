<?php
ob_start();
session_start();

//database credentials
define('DBHOST','localhost');
define('DBUSER','DB_4400');
define('DBPASS','17Mar"YX>');
define('DBNAME','db_course4400');

$db = new PDO("mysql:host=".DBHOST.";dbname=".DBNAME, DBUSER, DBPASS);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


//set timezone
date_default_timezone_set('US/Eastern');

//load classes as needed
function __autoload($class) {

   $class = strtolower($class);

	//if call from within the path
   $classpath = 'classes/class.'.$class . '.php';
   if ( file_exists($classpath)) {
      require_once $classpath;
	}

	//if call from above the path
   $classpath = '../classes/class.'.$class . '.php';
   if ( file_exists($classpath)) {
      require_once $classpath;
	}

}

$user = new User($db);

//include('functions.php');
?>
