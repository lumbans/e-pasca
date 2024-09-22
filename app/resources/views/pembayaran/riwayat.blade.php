<!DOCTYPE html>
<html>
<head>
    <title>Riwayat Pembayaran</title>
</head>
<body>
    <h1>Riwayat Pembayaran</h1>
    <table border="1">
        <thead>
            <tr>
                <th>ID Pembayaran</th>
                <th>Tanggal Pembayaran</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            @foreach($riwayat as $pembayaran)
                <tr>
                    <td>{{ $pembayaran->id_pembayaran }}</td>
                    <td>{{ $pembayaran->tanggal_pembayaran }}</td>
                    <td>{{ $pembayaran->total }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
