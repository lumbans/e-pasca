<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class ProfileController extends Controller
{
    public function show()
    {
        $user = Auth::user();
        return view('profile.show', compact('user'));
    }

    public function update(Request $request)
    {
        $request->validate([
            'username' => 'required|unique:users,username,' . Auth::id(),
        ]);

        $user = Auth::user();
        $user->update([
            'username' => $request->username,
        ]);

        return redirect()->route('profile.show')->with('success', 'Profile updated successfully.');
    }
}
