from abc import ABC, abstractmethod


class Argentur:
    def __init__(self, sistema_activo):
        self.sistema_activo = sistema_activo
        self.servicio = []
        self.ventas = []

    def get_servicio(self):
        for s in self.servicio:
            print(f"Fecha Partida: {s.get_fecha_partida()} \n Fecha llegada: {s.get_fecha_llegada()} \n Calidad: {s.get_calidad()} \n Itinerario:")
            s.get_itinerario()


class Servicio:
    def __init__(self,unidad, fecha_partida, fecha_llegada,calidad,precio,itinerario):
        self.unidad = unidad
        self.fecha_partida = fecha_partida
        self.fecha_llegada = fecha_llegada
        self.calidad = calidad
        self.precio = precio
        self.itinerario=itinerario
        self.reservas = []
        self.ventas = []
    def get_fecha_partida(self):
        return self.fecha_partida
    def get_fecha_llegada(self):
        return self.fecha_llegada
    def get_calidad(self):
        return self.calidad
    def get_itinerario(self):
        self.itinerario.get_ciudad()

class Ciudad:
    def __init__(self,codigo, nombre, provincia):
        self.codigo = codigo
        self.nombre = nombre
        self.provincia = provincia

    def get_nombre(self):
        return self.nombre


class Itinerario:
    def __init__(self,ciudad):

       self.ciudad = ciudad
    def get_ciudad(self):
        for i in self.ciudad:
            if i == self.ciudad[0] :
                print(f"Ciudad de Partida: {i.get_nombre()}")
            elif i != self.ciudad[len(self.ciudad)-1]:
                print(f"Parada Intermedia: {i.get_nombre()}")
            else:
                print(f"Ciudad de destino: {i.get_nombre()}")


class Reserva:
    def __init__(self,fecha_hora,pasajero):
        self.fecha_hora = fecha_hora
        self.pasajero =pasajero

class Venta:
    def __init__(self,fecha_hora,asiento,medio_pago,pasajero):
        self.fecha_hora = fecha_hora
        self.asiento = asiento
        self.medio_pago=medio_pago
        self.pasajero = pasajero



class Unidad:
    def __init__(self,patente):
        self.patente = patente
        self.asientos=[]

class Pasajero:
    def __init__(self,nombre, email, dni,asiento):
        self.nombre = nombre
        self.email = email
        self.dni = dni
        self.asiento = asiento

class MedioPago(ABC):
    @abstractmethod
    def __init__(self):
        pass

class TajetaCredito(MedioPago):
    def __init__(self, numero, dni, nombre,fecha_vencimiento):
        self.numero = numero
        self.dni = dni
        self.nombre = nombre
        self.fecha_vencimiento = fecha_vencimiento

class MercadoPago(MedioPago):
    def __init__(self,celular, email):
        self.celular = celular
        self.email = email

class Uala(MedioPago):
    def __init__(self,email, nombre_titular):
        self.email = email
        self.nombre_titular = nombre_titular










if __name__ == '__main__':
    # Crear ciudades
    ciudad1 = Ciudad(1, "Buenos Aires", "Buenos Aires")
    ciudad2 = Ciudad(2, "Rosario", "Santa Fe")
    ciudad3 = Ciudad(3, "Córdoba", "Córdoba")
    ciudad4 = Ciudad(4, "Mendoza", "Mendoza")
    ciudades = [ciudad1, ciudad2, ciudad3, ciudad4]

    # Crear itinerario con ciudades
    itinerario = Itinerario(ciudades)

    # Crear unidad (colectivo, micro, etc.)
    unidad1 = Unidad("ABC123")

    # Crear servicio con itinerario
    servicio1 = Servicio(unidad1, "2025-05-01 08:00", "2025-05-02 18:00", "Premium", 15000, itinerario)

    # Crear instancia del sistema Argentur
    sistema = Argentur(sistema_activo=True)
    sistema.servicio.append(servicio1)  # Cargar el servicio

    # Consultar los servicios disponibles
    print("=== Servicios Disponibles ===")
    sistema.get_servicio()
