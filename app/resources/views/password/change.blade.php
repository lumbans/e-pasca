<!DOCTYPE html>
<html>
<head>
    <title>Ganti Password</title>
</head>
<body>
    <h1>Ganti Password</h1>
    <form action="{{ route('password.update') }}" method="POST">
        @csrf
        <label for="current_password">Password Saat Ini:</label>
        <input type="password" name="current_password" required><br>

        <label for="new_password">Password Baru:</label>
        <input type="password" name="new_password" required><br>

        <label for="confirm_password">Konfirmasi Password Baru:</label>
        <input type="password" name="confirm_password" required><br>

        <button type="submit">Ganti Password</button>
    </form>
</body>
</html>
