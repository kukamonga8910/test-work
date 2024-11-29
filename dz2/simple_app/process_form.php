<?php
// Проверка, была ли отправлена форма
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Данные для подключения к базе данных
    $host = 'localhost'; // Хост базы данных
    $username = 'php'; // Имя пользователя базы данных
    $password = 'phppasswd'; // Пароль базы данных
    $database = 'simple_app'; // Имя базы данных

    // Подключение к базе данных
    $connection = mysqli_connect($host, $username, $password, $database);

    // Проверка на ошибку подключения
    if (!$connection) {
        die("Ошибка подключения: " . mysqli_connect_error());
    }

    // Получение данных из формы
    $id = $_POST["id"];
    $model = $_POST["model"];
    $license = $_POST["license"];
    $color = $_POST["color"];

    // Подготовка SQL-запроса для добавления записи
    $insertQuery = "INSERT INTO cars (id, model, license, color) VALUES ('$id', '$model', '$license', '$color')";

    // Выполнение запроса
    if (mysqli_query($connection, $insertQuery)) {
	    echo "<p>Новая запись успешно добавлена в таблицу.</p>";
	    echo '<a href="view_records.php">View all records</a>';

    } else {
        echo "Ошибка при добавлении записи: " . mysqli_error($connection);
    }

    // Закрытие соединения с базой данных
    mysqli_close($connection);
} else {
    // Если форма не была отправлена, перенаправьте пользователя на страницу с формой
    header("Location: index.html");
    exit;
}
?>
