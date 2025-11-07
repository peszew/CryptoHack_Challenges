def parse_input_file(filename="output_479698cde19aaa05d9e9dfca460f5443.txt"):
    """
    Wczytuje i parsuje p oraz listę liczb z pliku.
    """
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if len(lines) < 2:
            print(f"Błąd: Plik musi zawierać co najmniej 2 linie")
            return None, None
        
        p_val = None
        ints_list = None
        
        
        for line in lines:
            if line.startswith('p = '):
                p_val = int(line.split(' = ')[1])
            elif line.startswith('ints = '):
                ints_list = eval(line.split(' = ')[1])
                
        if p_val is None or ints_list is None:
            print("Błąd: Nie znaleziono 'p =' lub 'ints =' w pliku")
            return None, None
            
        print(f"Pomyślnie sparsowano {filename}")
        return p_val, ints_list
        
    except FileNotFoundError:
        print(f"Błąd: Plik '{filename}' nie został znaleziony")
        return None, None
    except Exception as e:
        print(f"Błąd parsowania pliku: {e}")
        return None, None

def solve_qr_special_case(prime, number_list):
   
   
    if prime % 4 != 3:
        print(f"Błąd: p ({prime}) nie spełnia warunku p % 4 == 3")
        return None

    print(f"Szukanie dla p = {prime} (p % 4 == 3)")
    
    # Kryterium Eulera
    euler_exponent = (prime - 1) // 2
    found_qr = None
    
    for num in number_list:
        legendre_symbol = pow(num, euler_exponent, prime)
        
        if legendre_symbol == 1:
            print(f"[+] Znaleziono QR: {num}")
            found_qr = num
            break
        else:
            print(f"[-] {num} nie jest QR")
            
    if found_qr is None:
        print("Nie znaleziono żadnej reszty kwadratowej na liście.")
        return None
        
    # Obliczanie pierwiastków dla p % 4 == 3
    root_exponent = (prime + 1) // 4
    root_1 = pow(found_qr, root_exponent, prime)
    root_2 = prime - root_1
    
    print(f"Pierwiastki to: {root_1} i {root_2}")
    
    # Flaga to większy pierwiastek
    flag = max(root_1, root_2)
    print(f"Flaga (większy pierwiastek): {flag}")
    return flag

# Główna część skryptu
if __name__ == "__main__":
    p, candidates = parse_input_file("output_479698cde19aaa05d9e9dfca460f5443.txt")
    if p and candidates:
        solve_qr_special_case(p, candidates)