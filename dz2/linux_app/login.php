<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Подключение к базе данных MySQL
    $servername = "localhost";
    $username = "username";
    $password = "password";
    $dbname = "application";

    // Создание подключения
    $conn = new mysqli($servername, $username, $password, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Получаем введенные пользователем данные из формы
    $input_username = $_POST["username"];
    $input_password = $_POST["password"];

    // Запрос к базе данных для получения данных пользователя
    $stmt = $conn->prepare("SELECT username, password FROM users WHERE username = ?");
    $stmt->bind_param("s", $input_username);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 1) {
        // Пользователь найден, проверяем пароль
        $row = $result->fetch_assoc();
	$hashed_password = $row["password"];

        if (password_verify($input_password, $hashed_password)) {
            // Успешная аутентификация
            $_SESSION["loggedin"] = true;
            $_SESSION["username"] = $input_username;
            header("Location: index.php"); // Перенаправление на домашнюю страницу
            exit();
        } else {
            // Неверный пароль
            $error = "Invalid username or password!";
        }
    } else {
        // Пользователь не найден
        $error = "User not found!";
    }

    $stmt->close();
    $conn->close();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h2>Login</h2>
    <?php if(isset($error)) { echo "<p>$error</p>"; } ?>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
    <p>Don't have an account? <a href="register.php">Register here</a></p>
</body>
</html>

