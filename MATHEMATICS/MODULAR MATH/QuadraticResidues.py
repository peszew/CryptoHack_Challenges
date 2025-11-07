def find_quadratic_residue(modulus, numbers_to_check):
    
    print(f"p = {modulus}")
    print(f"Lista liczb do sprawdzenia = {numbers_to_check}")
    print("--------------------------------")

    for potential_root in range(1, modulus):
        square = pow(potential_root, 2, modulus)

        if square in numbers_to_check:
            root1 = potential_root
            
            root2 = (-root1) % modulus 
            
            found_residue = square
            
            print(f"Znaleziona reszta kwadratowa: {found_residue}")
            print(f"Pierwiastki kwadratowe to: {root1} i {root2}")

            # Znalezienie flagi
            flag = min(root1, root2)
            print(f"Mniejszy pierwiastek (flaga) to: {flag}")
            return flag

    print("Nie znaleziono reszty kwadratowej na liście.")
    return None

# Dane z zadania
p_val = 29
candidates = [14, 6, 11]

# Uruchomienie
find_quadratic_residue(p_val, candidates)