<?php
$servername = "mysql26.mydevil.net";
$username = "m1022_django";
$password = "9m%%(n9@QIq5nrvUBQ$0";
$db = "m1022_autowaiter"

// Create connection
$conn = new mysqli($servername, $username, $password, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";

$sql = "SELECT product_name FROM orders_product WHERE product_name = " .$_POST['productname'];
$select = mysqli_query($con, $sql);
$row = mysqli_fetch_assoc($select);

if (mysqli_num_rows > 0) {
    echo "exist";
}else echo 'notexist';
?>