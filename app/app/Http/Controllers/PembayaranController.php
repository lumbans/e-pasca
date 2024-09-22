namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Pembayaran;
use Illuminate\Support\Facades\Auth;

class PembayaranController extends Controller
{
    public function riwayatPembayaran()
    {
        $riwayat = Pembayaran::where('id_user', Auth::id())->get();
        return view('pembayaran.riwayat', compact('riwayat'));
    }
}
