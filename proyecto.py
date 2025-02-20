from datetime import datetime


class NodoMantenimiento:
    def __init__(self, mantenimiento):
        self.mantenimiento = mantenimiento
        self.siguiente = None


class NodoVehiculo:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.siguiente = None
        self.anterior = None


class Mantenimiento:
    def __init__(self, fecha, descripcion, costo):
        self.fecha = self.validar_fecha(fecha)
        self.descripcion = descripcion
        self.costo = self.validar_costo(costo)
    
    def validar_fecha(self, fecha):
        formatos_validos = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
        for formato in formatos_validos:
            try:
                fecha_valida = datetime.strptime(fecha, formato)
                return fecha_valida.strftime("%Y-%m-%d")  
            except ValueError:
                continue
        raise ValueError("Fecha inválida. Use formato YYYY-MM-DD, DD-MM-YYYY o DD/MM/YYYY.")
    
    def validar_costo(self, costo):
        if costo >= 0:
            return costo
        else:
            raise ValueError("El costo debe ser un número positivo.")


class Vehiculo:
    def __init__(self, placa, marca, modelo, anio, kilometraje):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.kilometraje = kilometraje
        self.historial = None  
    
    def agregar_mantenimiento(self, mantenimiento):
        nuevo_nodo = NodoMantenimiento(mantenimiento)
        if self.historial is None:
            self.historial = nuevo_nodo
        else:
            actual = self.historial
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def consultar_historial(self):
        actual = self.historial
        if not actual:
            print("No hay mantenimientos registrados.")
        while actual:
            print(f"Fecha: {actual.mantenimiento.fecha}, Descripción: {actual.mantenimiento.descripcion}, Costo: {actual.mantenimiento.costo}")
            actual = actual.siguiente

    def costo_total_mantenimientos(self):
        total = 0
        actual = self.historial
        while actual:
            total += actual.mantenimiento.costo
            actual = actual.siguiente
        return total

    def eliminar_historial(self):
        self.historial = None


class FlotaVehiculos:
    def __init__(self):
        self.inicio = None  
    
    def registrar_vehiculo(self, placa, marca, modelo, anio, kilometraje):
        vehiculo = Vehiculo(placa, marca, modelo, anio, kilometraje)
        nuevo_nodo = NodoVehiculo(vehiculo)
        if self.inicio is None:
            self.inicio = nuevo_nodo
        else:
            actual = self.inicio
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = actual
    
    def eliminar_vehiculo(self, placa):
        actual = self.inicio
        while actual:
            if actual.vehiculo.placa == placa:
                actual.vehiculo.eliminar_historial()  
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                if actual == self.inicio:
                    self.inicio = actual.siguiente
                print(f"Vehículo {placa} y su historial de mantenimientos eliminados.")
                return
            actual = actual.siguiente
        print("Vehículo no encontrado.")
    
    def buscar_vehiculo(self, placa):
        actual = self.inicio
        while actual:
            if actual.vehiculo.placa == placa:
                return actual.vehiculo
            actual = actual.siguiente
        return None
    
    def listar_vehiculos(self):
        actual = self.inicio
        if not actual:
            print("No hay vehículos registrados.")
        while actual:
            print(f"Placa: {actual.vehiculo.placa}, Marca: {actual.vehiculo.marca}, Modelo: {actual.vehiculo.modelo}, Año: {actual.vehiculo.anio}, Kilometraje: {actual.vehiculo.kilometraje}")
            actual = actual.siguiente

def menu():
    flota = FlotaVehiculos()
    while True:
        print("""    
            Menú de opciones  """)
        print("1. Registrar vehículo")
        print("2. Mostrar vehículos")
        print("3. Buscar vehículo")
        print("4. Eliminar vehículo")
        print("5. Gestionar mantenimientos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            placa = input("Ingrese la placa: ")
            marca = input("Ingrese la marca: ")
            modelo = input("Ingrese el modelo: ")
            anio = int(input("Ingrese el año: "))
            kilometraje = int(input("Ingrese el kilometraje: "))
            flota.registrar_vehiculo(placa, marca, modelo, anio, kilometraje)
            print("Vehículo registrado con éxito.")
        elif opcion == "2":
            flota.listar_vehiculos()
        elif opcion == "3":
            placa = input("Ingrese la placa a buscar: ")
            vehiculo = flota.buscar_vehiculo(placa)
            if vehiculo:
                print(f"Placa: {vehiculo.placa}, Marca: {vehiculo.marca}, Modelo: {vehiculo.modelo}, Año: {vehiculo.anio}, Kilometraje: {vehiculo.kilometraje}")
            else:
                print("Vehículo no encontrado.")
        elif opcion == "4":
            placa = input("Ingrese la placa a eliminar: ")
            flota.eliminar_vehiculo(placa)
        elif opcion == "5":
            placa = input("Ingrese la placa del vehículo para gestionar mantenimientos: ")
            vehiculo = flota.buscar_vehiculo(placa)
            if vehiculo:
                while True:
                    print("    Gestión de Mantenimientos   ")
                    print("1. Agregar mantenimiento")
                    print("2. Consultar historial de mantenimientos")
                    print("3. Calcular costo total de mantenimientos")
                    print("4. Volver al menú principal")
                    sub_opcion = input("Seleccione una opción: ")

                    if sub_opcion == "1":
                        fecha = input("Ingrese la fecha del mantenimiento (dia-mes-año): ")
                        descripcion = input("Ingrese la descripción del servicio realizado: ")
                        costo = float(input("Ingrese el costo del mantenimiento: "))
                        try:
                            mantenimiento = Mantenimiento(fecha, descripcion, costo)
                            vehiculo.agregar_mantenimiento(mantenimiento)
                            print("Mantenimiento agregado con éxito.")
                        except ValueError as e:
                            print(e)
                    elif sub_opcion == "2":
                        vehiculo.consultar_historial()
                    elif sub_opcion == "3":
                        total = vehiculo.costo_total_mantenimientos()
                        print(f"Costo total de los mantenimientos: {total}")
                    elif sub_opcion == "4":
                        break
                    else:
                        print("Opción no válida. Intente de nuevo.")
            else:
                print("Vehículo no encontrado.")
        elif opcion == "6":
            print("Saliendo del programa, ¡¡¡ Gracias por utilizar este programa!!! ;)")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

menu()

