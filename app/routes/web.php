<?php
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\AdminController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\PasswordController;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProfileController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

// route utama
Route::get('/', [AdminController::class, 'index'])->middleware('auth', 'onlyAdmin');

// route untuk User (pelanggan dan juga admin adalah user) 
Route::prefix('/User')->middleware('auth')->group(function () {
    Route::get('/', [UserController::class, 'index']);
    Route::get('/status', [UserController::class, 'status']);
    Route::get('/password', [UserController::class, 'ubahPassword']);
    Route::get('/riwayat', [UserController::class, 'riwayat']);
});

// route untuk Admin (hanya admin yang boleh mengakses)
Route::prefix('/Admin')->middleware('onlyAdmin', 'auth')->group(function () {
    Route::get('/', [AdminController::class, 'index']);
    Route::get('/dataPelanggan', [AdminController::class, 'dataPelanggan']);
    Route::post('/add', [AdminController::class, 'addPelanggan']);
    Route::post('/edit', [AdminController::class, 'editPelanggan']);
    Route::get('/delete/{id}', [AdminController::class, 'deletePelanggan']);
    Route::get('/dataTagihan', [AdminController::class, 'dataTagihan']);
});

// route untuk Auth (pengelolaan authentikasi dan otorisasi)
Route::prefix('/auth')->group(function () {
    Route::get('/', [AuthController::class, 'index'])->name('login')->middleware('guest');
    Route::post('/login', [AuthController::class, 'login'])->middleware('guest');
    Route::get('/logout', [AuthController::class, 'logout'])->middleware('auth');
});

Route::get('/', [DashboardController::class, 'index'])->middleware('auth');
Route::get('/password/change', [PasswordController::class, 'showChangeForm'])->name('password.change');
Route::post('/password/update', [PasswordController::class, 'update'])->name('password.update');
Route::get('/signup', [AuthController::class, 'showSignupForm'])->name('signup');
Route::post('/signup', [AuthController::class, 'signup']);
Route::get('/riwayat-pembayaran', [PembayaranController::class, 'riwayatPembayaran'])->middleware('auth')->name('riwayat.pembayaran');
Route::get('/profile', [ProfileController::class, 'show'])->middleware('auth')->name('profile.show');
Route::post('/profile', [ProfileController::class, 'update'])->middleware('auth');
