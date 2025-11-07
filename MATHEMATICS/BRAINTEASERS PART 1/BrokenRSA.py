from Crypto.Util.number import long_to_bytes
import sys

# Dane wejściowe z pliku broken_rsa
n = 27772857409875257529415990911214211975844307184430241451899407838750503024323367895540981606586709985980003435082116995888017731426634845808624796292507989171497629109450825818587383112280639037484593490692935998202437639626747133650990603333094513531505209954273004473567193235535061942991750932725808679249964667090723480397916715320876867803719301313440005075056481203859010490836599717523664197112053206745235908610484907715210436413015546671034478367679465233737115549451849810421017181842615880836253875862101545582922437858358265964489786463923280312860843031914516061327752183283528015684588796400861331354873
e = 16
ct = 11303174761894431146735697569489134747234975144162172162401674567273034831391936916397234068346115459134602443963604063679379285919302225719050193590179240191429612072131629779948379821039610415099784351073443218911356328815458050694493726951231241096695626477586428880220528001269746547018741237131741255022371957489462380305100634600499204435763201371188769446054925748151987175656677342779043435047048130599123081581036362712208692748034620245590448762406543804069935873123161582756799517226666835316588896306926659321054276507714414876684738121421124177324568084533020088172040422767194971217814466953837590498718


def legendre_symbol(a, n):
    
    l = pow(a, (n - 1) // 2, n)
    if l == n - 1:
        return -1
    return l

def modular_sqrt(a, n):
    """Oblicza pierwiastek kwadratowy modulo n (Tonelli-Shanks)"""
    if legendre_symbol(a, n) != 1:
        return 0  # Nie ma pierwiastka (lub jest 0)
    
    if n % 4 == 3:
        return pow(a, (n + 1) // 4, n)

    # Logika dla n % 4 == 1 (Tonelli-Shanks)
    q = n - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2

    z = 2
    while legendre_symbol(z, n) != -1:
        z += 1
    
    c = pow(z, q, n)
    x = pow(a, (q + 1) // 2, n)
    t = pow(a, q, n)
    r = s

    while True:
        if t == 1:
            return x
        if t == 0:
            return 0
            
        i, temp_t = 0, t
        while temp_t != 1 and i < r:
            temp_t = pow(temp_t, 2, n)
            i += 1

        if i == 0:
            return 0 # err

        b = pow(c, 2**(r - i - 1), n)
        x = (x * b) % n
        c = (b * b) % n
        t = (t * c) % n
        r = i


print(f"Testowanie {e} kandydatów (ścieżek pierwiastkowania)...")

found_flag = None

for i in range(e):
    f = ct  
    chk = i # 'chk' koduje ścieżkę (0 = +r, 1 = -r)
    valid_path = True
    
    # 4 razy pierwiastkowanie
    for j in range(4): 
        f_next = modular_sqrt(f, n)
        
        if f_next == 0:
            valid_path = False
            break
        
        f = f_next
        
        # Sprawdź bit ze ścieżki 'i', aby zdecydować czy wziąć +r czy -r
        if (chk >> j) & 1:  # (chk % 2 == 1)
            f = n - f
    
    # Jeśli ścieżka była poprawna, spróbuj zdekodować
    if valid_path:
        try:
            message_bytes = long_to_bytes(f)
            if all(32 <= b < 127 for b in message_bytes):
                decoded_str = message_bytes.decode('ascii')
                print(f"[+] Znaleziono kandydata dla i = {i}: {decoded_str}")
                if "crypto" in decoded_str or "{" in decoded_str:
                    found_flag = decoded_str
        except Exception as e:
            continue

if found_flag:
    print(f"\nFlaga: {found_flag}")
else:
    print("\nNie znaleziono flagi. Wszyscy kandydaci zostali przetestowani.")