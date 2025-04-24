from abc import ABC, abstractmethod


class Argentur:
    def __init__(self, sistema_activo):
        self.sistema_activo = sistema_activo
        self.servicio = []
        self.ventas = []

    def get_servicio(self):
        for s in self.servicio:
            print(f"Servicio:{s.get_cod_servicio()}")
            print(f"Fecha Partida: {s.get_fecha_partida()} \nFecha llegada: {s.get_fecha_llegada()} \nCalidad: {s.get_calidad()} \nItinerario:")
            s.get_itinerario()
            print()

    def get_servicio_unico(self, servicio_selecionado):
        for s in self.servicio:
            if s.get_cod_servicio() == servicio_selecionado:
                return s
        print("Error no servicio selecionado")


class Servicio:
    def __init__(self,codigo,unidad, fecha_partida, fecha_llegada,calidad,precio,itinerario):
        self.codigo = codigo
        self.unidad = unidad
        self.fecha_partida = fecha_partida
        self.fecha_llegada = fecha_llegada
        self.calidad = calidad
        self.precio = precio
        self.itinerario=itinerario
        self.reservas = []
        self.ventas = []
    def get_asientos_unidad(self):
        self.unidad.get_asientos()
    def get_cod_servicio(self):
        return self.codigo
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

class Pasajero:
    def __init__(self,nombre, email, dni,asiento):
        self.nombre = nombre
        self.email = email
        self.dni = dni
        self.asiento = asiento

class Unidad:
    def __init__(self,patente , asientos):
        self.patente = patente
        self.asientos = asientos
    def get_asientos(self):
        for a in self.asientos:
            if not a.get_ocupado():
                print(a.get_numero())

class Asiento:
    def __init__(self, numero, ocupado):
        self.numero = numero
        self.ocupado = ocupado
    def get_numero(self):
        return self.numero
    def get_ocupado(self):
        return self.ocupado

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
    ciudad5 = Ciudad(5, "Salta", "Salta")
    ciudad6 = Ciudad(6, "Bariloche", "Río Negro")

    # Crear itinerarios
    itinerario1 = Itinerario([ciudad1, ciudad2, ciudad3])
    itinerario2 = Itinerario([ciudad3, ciudad4])
    itinerario3 = Itinerario([ciudad1, ciudad5, ciudad6])
    itinerario4 = Itinerario([ciudad2, ciudad3, ciudad4])
    itinerario5 = Itinerario([ciudad6, ciudad4, ciudad1])
    #Generar mas asientos con un for y una ocupacion aleatoria
    asiento1 = Asiento("1",True)
    asiento2 = Asiento("2",False)
    asiento3 = Asiento("3",True)
    asiento4 = Asiento("4",False)
    asiento5 = Asiento("5",True)

    vector_asientos = [asiento1, asiento2, asiento3, asiento4, asiento5]

    # Crear unidades utilizar diferentes arreglos de asientos
    unidad1 = Unidad("ABC123",vector_asientos)
    unidad2 = Unidad("DEF456",vector_asientos)
    unidad3 = Unidad("GHI789",vector_asientos)
    unidad4 = Unidad("JKL012",vector_asientos)
    unidad5 = Unidad("MNO345",vector_asientos)

    # Crear servicios
    servicio1 = Servicio("serv1", unidad1, "2025-05-01 08:00", "2025-05-02 18:00", "Premium", 15000, itinerario1)
    servicio2 = Servicio("serv2", unidad2, "2025-06-10 07:30", "2025-06-11 15:45", "Económico", 8000, itinerario2)
    servicio3 = Servicio("serv3", unidad3, "2025-07-05 20:00", "2025-07-07 06:00", "Ejecutivo", 12000, itinerario3)
    servicio4 = Servicio("serv4",unidad4, "2025-08-15 10:00", "2025-08-16 22:00", "Premium", 16000, itinerario4)
    servicio5 = Servicio("serv5",unidad5, "2025-09-20 06:00", "2025-09-21 18:30", "Económico", 9000, itinerario5)

    # Crear instancia del sistema Argentur
    sistema = Argentur(sistema_activo=True)

    # Cargar los servicios
    sistema.servicio.extend([servicio1, servicio2, servicio3, servicio4, servicio5])

    # Consultar los servicios disponibles
    print("=== Servicios Disponibles ===")
    sistema.get_servicio()

    codigo_servicio = input("seleccione su servicio:\n")
    servicio_selec = sistema.get_servicio_unico(codigo_servicio)
    print(f"Usted selecciono: {servicio_selec.get_cod_servicio()}")
    print("asientos disponibles:")
    servicio_selec.get_asientos_unidad()


