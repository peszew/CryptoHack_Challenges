import re

def compute_tonelli_shanks(residue, prime):
    """
    Algorytm Tonelliego-Shanksa do znajdowania pierwiastka kwadratowego modulo p.
    """
    # Sprawdzenie Kryterium Eulera
    if pow(residue, (prime - 1) // 2, prime) != 1:
        return None  # Nie jest resztą kwadratową

    # Rozkład p-1 = q_odd * 2^s_pow
    q_odd = prime - 1
    s_pow = 0
    while q_odd % 2 == 0:
        q_odd //= 2
        s_pow += 1

    # Znalezienie nieresztu kwadratowej
    non_residue = 2
    while pow(non_residue, (prime - 1) // 2, prime) != prime - 1:
        non_residue += 1

    # Inicjalizacja
    c_val = pow(non_residue, q_odd, prime)
    r_val = pow(residue, (q_odd + 1) // 2, prime)
    t_val = pow(residue, q_odd, prime)
    m_val = s_pow

    # Główna pętla
    while t_val != 1:
        # Znajdź najmniejsze i > 0 takie, że t_val^(2^i) == 1
        temp_t = t_val
        i = 0
        while temp_t != 1 and i < m_val:
            temp_t = pow(temp_t, 2, prime)
            i += 1
        
        if i == 0:
            break # Powinno się zdarzyć tylko gdy t_val == 1

        # Aktualizacja wartości
        b_pow = 2**(m_val - i - 1)
        b_val = pow(c_val, b_pow, prime)
        
        r_val = (r_val * b_val) % prime
        t_val = (t_val * b_val * b_val) % prime
        c_val = (b_val * b_val) % prime
        m_val = i

    return r_val

def find_modular_sqrt_general(a, p):
    """
    Znajduje pierwiastek kwadratowy modulo p. Zwraca mniejszy z dwóch pierwiastków.
    """
    if pow(a, (p - 1) // 2, p) != 1:
        return None # Nie ma pierwiastka

    # Przypadek p % 4 == 3
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
    # Przypadek p % 4 == 1 (lub p == 2, choć nie jest 1 mod 4)
    else:
        r = compute_tonelli_shanks(a, p)
        if r is None:
            return None

    return min(r, p - r)

def main_sqrt_task():
    
    try:
        with open('output_abe0beb359a950c8a0a9300897528a9d.txt', 'r') as f:
            content = f.read()
            
        
        a_val = None
        p_val = None
        for line in content.split('\n'):
            if line.startswith('a = '):
                a_val = int(line.split(' = ')[1])
            elif line.startswith('p = '):
                p_val = int(line.split(' = ')[1])
        
        if a_val is None or p_val is None:
            raise ValueError("Nie znaleziono a lub p w pliku.")

        print(f"a = {str(a_val)[:60]}...")
        print(f"p = {str(p_val)[:60]}...")
        print(f"p % 4 = {p_val % 4} (Użyje Tonelli-Shanks jeśli 1, prosta formuła jeśli 3)")

        result = find_modular_sqrt_general(a_val, p_val)

        if result is None:
            print("Pierwiastek kwadratowy nie istnieje.")
        else:
            print(f"Mniejszy z dwóch pierwiastków to: {result}")
            # Weryfikacja
            verification = pow(result, 2, p_val)
            print(f"\nWeryfikacja: {result}^2 % p = {verification}")
            print(f"Oryginalne a: {a_val}")
            assert verification == a_val
            
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku 'output_abe0beb359a950c8a0a9300897528a9d.txt'")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    main_sqrt_task()