<!DOCTYPE html>
<html>
<head>
    <title>Profile</title>
</head>
<body>
    <h1>Profile</h1>
    <form action="{{ route('profile.show') }}" method="POST">
        @csrf
        <label for="username">Username:</label>
        <input type="text" name="username" value="{{ $user->username }}" required><br>

        <button type="submit">Update Profile</button>
    </form>
</body>
</html>
