import sys

def main(numero_extraer=None):
    print("Buscar numero que falta del 1-100")
    conjunto = PrimerosCienNumeros()
    
    if numero_extraer is None:
        while True:
            try:
                numero_extraer = int(input("\nSe tiene que extraer un numero entre 1 y 100: "))
                if 1 <= numero_extraer <= 100:
                    break
                else:
                    print("El numero debe estar entre 1 y 100")
            except ValueError:
                print("Debe ingresar un número entero valido")
    
    if not conjunto.extract(numero_extraer):
        print(f"El numero {numero_extraer} puede que ya se haya extraído.")
        return
    
    print(f"\nSe extrajo el numero {numero_extraer}")

    faltante = conjunto.calcular_faltante()
    
    if faltante is not None:
        print(f"\n    El faltante es: {faltante}")
    else:
        print("\n Ocurrio un error")

class PrimerosCienNumeros:
    def __str__(self):
        return f"conjunto de numeros: {sorted(self.numeros)}"
    
    def __init__(self):
        self.numeros = set(range(1, 101))
    
    def _validar_numero(self, numero):
        if not isinstance(numero, int):
            return False
        return 1 <= numero <= 100
    
    def calcular_faltante(self):
        if len(self.numeros) == 99:
            for num in range(1, 101):
                if num not in self.numeros:
                    return num
        return None
    
    def extract(self, numero):
        if not self._validar_numero(numero):
            return False
        if numero in self.numeros:
            self.numeros.remove(numero)
            return True
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            num = int(sys.argv[1])
            if 1 <= num <= 100:
                main(num)
            else:
                print("el numero debe estar entre 1 y 100")
        except ValueError:
            print(" Debe ser un numero entero del 1 al 100.")
    else:
        main()