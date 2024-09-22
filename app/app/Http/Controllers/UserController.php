<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use SebastianBergmann\CodeCoverage\Report\Html\Dashboard;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    //
    public function index()
    {
        return view("user.profile", ['judul_menu' => 'profile']);
    }

    public function status()
    {
        return view("user.status", ['judul_menu' => 'status']);
    }

    public function riwayat()
    {
        return view("user.riwayat", ['judul_menu' => 'riwayat']);
    }

    public function ubahPassword()
    {
        return view("user.ubah-password", ['judul_menu' => 'password']);
    }
   
    public function updatePassword(Request $request)
    {
        $request->validate([
            'current_password' => 'required',
            'new_password' => 'required|min:8|confirmed',
        ]);

        // Memeriksa apakah password saat ini sesuai
        if (!Hash::check($request->current_password, Auth::user()->password)) {
            return back()->withErrors(['current_password' => 'Password saat ini tidak sesuai']);
        }

        // Mengupdate password pengguna
        $user = Auth::user();
        $user->password = Hash::make($request->new_password);
        $user->save();

        return redirect()->route('password.change')->with('success', 'Password berhasil diubah');
    }
}
