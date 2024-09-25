def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

def linear_search(numbers, search_value):
    for i in range(len(numbers)):
        if numbers[i] == search_value:
            return True
    return False

def main():
    numbers = []
    while True:
        print("\nMENU PILIHAN")
        print("1. Input angka")
        print("2. Sorting")
        print("3. Searching")
        print("4. Selesai")
        
        choice = int(input("Masukkan pilihan [1/2/3/4]: "))
        
        if choice == 1:
            n = int(input("Masukkan jumlah nilai tugas: "))
            for i in range(n):
                num = int(input(f"Angka {i + 1}: "))
                numbers.append(num)
        
        elif choice == 2:
            bubble_sort(numbers)
            print("Hasil sorting:", numbers)
        
        elif choice == 3:
            search_value = int(input("Masukkan angka yang dicari: "))
            if linear_search(numbers, search_value):
                print("Angka ditemukan")
            else:
                print("Angka tidak ditemukan")
        
        elif choice == 4:
            break
        
        else:
            print("Pilihan tidak valid")
    
if __name__ == "__main__":
    main()
