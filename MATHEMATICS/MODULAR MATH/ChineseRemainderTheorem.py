def solve_crt_explicit(remainders, moduli):
    
    # Obliczenie N (total_product) - iloczynu wszystkich modułów
    total_product = 1
    for n in moduli:
        total_product *= n
        
    solution = 0
    
    # Użycie zip do iteracji po obu listach jednocześnie
    for a_i, n_i in zip(remainders, moduli):
        # Obliczenie N_i
        N_i = total_product // n_i
        # Obliczenie M_i jako odwrotności modularnej N_i modulo n_i
        M_i = pow(N_i, -1, n_i)
        
        # Dodanie składnika do sumy
        solution += a_i * N_i * M_i
        
    # Wynik to suma modulo N
    final_solution = solution % total_product
    return final_solution

# Dane z zadania
a_list = [2, 3, 5]
n_list = [5, 11, 17]

print(f"Rozwiązywanie układu:")
print(f"z = {a_list[0]} (mod {n_list[0]})")
print(f"z = {a_list[1]} (mod {n_list[1]})")
print(f"z = {a_list[2]} (mod {n_list[2]})")

result = solve_crt_explicit(a_list, n_list)

print(f"\nRozwiązanie: z = {result}")

# Weryfikacja
print("\nWeryfikacja:")
print(f"{result} % {n_list[0]} = {result % n_list[0]} (oczekiwano {a_list[0]})")
print(f"{result} % {n_list[1]} = {result % n_list[1]} (oczekiwano {a_list[1]})")
print(f"{result} % {n_list[2]} = {result % n_list[2]} (oczekiwano {a_list[2]})")

# Flaga
print(f"\nFlaga: {result}")