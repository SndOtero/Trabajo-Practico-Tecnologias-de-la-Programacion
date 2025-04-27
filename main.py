from abc import ABC, abstractmethod
from datetime import date
import random

class Argentur:
    def __init__(self, sistema_activo):
        self.sistema_activo = sistema_activo
        self.servicio = []
        self.ventas = []

    def add_servicio(self, servicios):
        self.servicio.extend(servicios)

    def get_servicio(self):
        for s in self.servicio:
            print(f"Servicio:{s.get_cod_servicio()}")
            print(f"Fecha Partida: {s.get_fecha_partida()} \nFecha llegada: {s.get_fecha_llegada()} \nCalidad: {s.get_calidad()} \nItinerario:")
            s.get_itinerario()
            print()

    def get_servicio_unico(self, servicio_selecionado):
        servicio = None
        for s in self.servicio:
            if s.get_cod_servicio() == servicio_selecionado:
                servicio= s
        if servicio is None:
            print("Error no servicio selecionado")
        return servicio

    def calcular_monto_total(self,fecha_desde,fecha_hasta):
        monto_total = 0
        for v in self.ventas:
            if v.get_fecha_hora() > fecha_desde and v.get_fecha_hora() < fecha_hasta:
                monto_total += v.get_monto()
        print(f"Monto total: {monto_total}")

    def ver_viajes_destino(self,fecha_desde,fecha_hasta):
        destino_aux = []
        for s in self.servicio:
            if s.get_fecha_partida() > fecha_desde and s.get_fecha_partida() < fecha_hasta:
                destino_aux.append(s.ver_viajes_destino_servicio())
        destino_final = {}
        for d in destino_aux:

            if d not in destino_final:
                destino_final[d] = 1
            else:
                destino_final[d] += 1
        print("Cantidad de viajes realizados a una ciudad:")
        for d in destino_final:
            print(f"{d}: {destino_final[d]}")

    def ver_pagos(self,fecha_desde,fecha_hasta):
        medio_pago_aux = []
        for v in self.ventas:
            if v.get_fecha_hora() > fecha_desde and v.get_fecha_hora() < fecha_hasta:
                medio_pago_aux.append(v.get_medio_pago())

        medio_pago_dic = {}
        for d in medio_pago_aux:
            if d not in medio_pago_dic:
                medio_pago_dic[d] = 1
            else:
                medio_pago_dic[d] += 1
        print("Cantidad de pagos realizados con cada medio de pago:")
        for d in medio_pago_dic:
            print(f"{d}: {medio_pago_dic[d]}")
        print("\n")

    def generar_venta(self,fecha_hora,asiento,medio_pago,pasajero,monto):
        self.ventas.append(Venta(fecha_hora,asiento,medio_pago,pasajero,monto))

    def generar_informe(self,fecha_desde,fecha_hasta):
        self.calcular_monto_total(fecha_desde,fecha_hasta)
        print("-----------------------------")
        self.ver_viajes_destino(fecha_desde,fecha_hasta)
        print("-----------------------------")
        self.ver_pagos(fecha_desde, fecha_hasta)


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

    def ver_viajes_destino_servicio(self):
        return self.itinerario.get_destino()

    def agregar_reserva(self, nombre, email, dni, nro_asiento):
        asiento = self.unidad.asiento_disponible(nro_asiento)

        if not self.unidad.ocupar_asiento(asiento):
            self.reservas.append(Reserva(date.today(),nombre, email, dni, asiento))
            print(f"Reserva realizada: pasajero: {nombre}, asiento: {asiento.get_numero()}, servicio del {self.fecha_partida}")


class Itinerario:
    def __init__(self,ciudad):
        self.ciudad = ciudad

    def get_destino(self):
        return self.ciudad[len(self.ciudad)-1].get_nombre()

    def get_ciudad(self):
        for i in self.ciudad:
            if i == self.ciudad[0] :
                print(f"Ciudad de Partida: {i.get_nombre()}")
            elif i != self.ciudad[len(self.ciudad)-1]:
                print(f"Parada Intermedia: {i.get_nombre()}")
            else:
                print(f"Ciudad de destino: {i.get_nombre()}")


class Ciudad:
    def __init__(self,codigo, nombre, provincia):
        self.codigo = codigo
        self.nombre = nombre
        self.provincia = provincia

    def get_nombre(self):
        return self.nombre


class Reserva:
    def __init__(self,fecha_hora,nombre, email, dni, asiento):
        self.fecha_hora = fecha_hora
        self.pasajero =Pasajero(nombre, email, dni, asiento)


class Pasajero:
    def __init__(self,nombre, email, dni,asiento):
        self.nombre = nombre
        self.email = email
        self.dni = dni
        self.asiento = asiento

    def get_nombre(self):
        return self.nombre


class Unidad:
    def __init__(self,patente , asientos):
        self.patente = patente
        self.asientos = asientos

    def get_asientos(self):
        asientos_libres = ""
        for a in self.asientos:
            if not a.get_ocupado():
                asientos_libres += " " + a.get_numero()
        print(f"Asientos disponibles:{asientos_libres}")

    def ocupar_asiento(self, asiento):
        estaba_ocupado = True
        if asiento.get_ocupado():
           print("Asiento Ocupado")
        else:
            asiento.set_ocupado()
            estaba_ocupado=False

        return estaba_ocupado

    def asiento_disponible(self, nro_asiento):
        for i in self.asientos:
            if i.get_numero() == nro_asiento:
                return i


class Asiento:
    def __init__(self, numero, ocupado):
        self.numero = numero
        self.ocupado = ocupado

    def get_numero(self):
        return self.numero

    def get_ocupado(self):
        return self.ocupado

    def set_ocupado(self):
        self.ocupado = True


class Venta:
    def __init__(self,fecha_hora,asiento,medio_pago,pasajero,monto):
        self.fecha_hora = fecha_hora
        self.asiento = asiento
        self.medio_pago = medio_pago
        self.pasajero = pasajero
        self.monto = monto

    def get_monto(self):
        return self.monto

    def get_fecha_hora(self):
        return self.fecha_hora

    def get_medio_pago(self):
        return self.medio_pago.get_tipo()


class MedioPago(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_tipo(self):
        pass


class TajetaCredito(MedioPago):
    def __init__(self, numero, dni, nombre,fecha_vencimiento):
        self.numero = numero
        self.dni = dni
        self.nombre = nombre
        self.fecha_vencimiento = fecha_vencimiento

    def get_tipo(self):
        return "Pago con Tajeta de Credito"


class MercadoPago(MedioPago):
    def __init__(self,celular, email):
        self.celular = celular
        self.email = email

    def get_tipo(self):
        return "Pago con Mercado Pago"


class Uala(MedioPago):
    def __init__(self,email, nombre_titular):
        self.email = email
        self.nombre_titular = nombre_titular

    def get_tipo(self):
        return "Pago con Uala"











if __name__ == '__main__':
    # Declaracion de instancias #



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



    #Generacion de asientos con estado de ocupacion aleatorio
    vector_asientos=[]

    # Seleccionar la cantidad de asientos del movil
    cantidad_asientos = 5
    for nro_asiento in range(cantidad_asientos):
        variable = random.choice([True, False])
        asiento = Asiento(str(nro_asiento), variable)
        vector_asientos.append(asiento)

    # Crear unidades utilizar diferentes arreglos de asientos
    unidad1 = Unidad("ABC123",vector_asientos)
    unidad2 = Unidad("DEF456",vector_asientos)
    unidad3 = Unidad("GHI789",vector_asientos)
    unidad4 = Unidad("JKL012",vector_asientos)
    unidad5 = Unidad("MNO345",vector_asientos)


    # Creacion de servicios que la empresa ofrece
    servicio1 = Servicio("serv1", unidad1, date(2025, 8, 4), date(2025, 8, 6), "Premium", 15000, itinerario1)
    servicio2 = Servicio("serv2", unidad2, date(2025, 9, 4), date(2025, 9, 6), "Económico", 8000, itinerario2)
    servicio3 = Servicio("serv3", unidad3, date(2025, 10, 4), date(2025, 10, 6), "Ejecutivo", 12000, itinerario3)
    servicio4 = Servicio("serv4", unidad4, date(2025, 11, 4), date(2025, 11, 6), "Premium", 16000, itinerario4)
    servicio5 = Servicio("serv5", unidad5, date(2025, 12, 4), date(2025, 12, 6), "Económico", 9000, itinerario5)

    # Crear instancia del sistema Argentur
    sistema = Argentur(True)

    # Cargar los servicios
    sistema.add_servicio([servicio1, servicio2, servicio3, servicio4, servicio5])

    ########################################
    #       EJEMPLO VENTA
    # Carga de ventas de ejemplo
    tarjeta = TajetaCredito("1234567890123456", "12345678", "Juan Perez", "12/27")
    mpago = MercadoPago("1122334455", "juan@example.com")
    uala = Uala("maria@example.com", "Maria Gomez")

    # Crear asientos
    asiento1 = Asiento("1", False)
    asiento2 = Asiento("2", False)
    asiento3 = Asiento("3", False)

    # Crear pasajeros
    pasajero1 = Pasajero("Juan Perez", "juan@example.com", "12345678", asiento1)
    pasajero2 = Pasajero("Maria Gomez", "maria@example.com", "87654321", asiento2)
    pasajero3 = Pasajero("Carlos Ruiz", "carlos@example.com", "56781234", asiento3)

    # Generar ventas
    sistema.generar_venta(date.today(), asiento1, tarjeta, pasajero1, 15000)
    sistema.generar_venta(date.today(), asiento2, mpago, pasajero2, 12000)
    sistema.generar_venta(date.today(), asiento3, uala, pasajero3, 8000)
    sistema.generar_venta(date.today(), asiento1, tarjeta, pasajero1, 15000)
    ########################################
    #----------------------------------------------------------------

    # Ejecucion del programa
    eleccion = int(input("Seleccione la opcion:\n1: Hacer una reserva \n2: Generar informe \n3: Salir\n"))
    while eleccion != 3:

        if eleccion == 1:
            # Consultar los servicios disponibles
            print("=== Servicios Disponibles ===")
            sistema.get_servicio()

            print("-----------------------------")

            #El cliente selecciona un servicio
            codigo_servicio = input("Seleccione su servicio:\n")

            #Transformacion a minusculas
            codigo_servicio = codigo_servicio.lower()

            servicio_selec = sistema.get_servicio_unico(codigo_servicio)
            print(f"Usted selecciono: {servicio_selec.get_cod_servicio()}")

            print("-----------------------------")

            #Muestra cuales son los asientos disponibles en la unidad de ese servicio
            servicio_selec.get_asientos_unidad()
            print("-----------------------------")
            print("Complete los siguientes datos para realizar una reserva:")
            # Datos del cliente
            nombre = input("Nombre:\n")
            email = input("Email:\n")
            dni = input("Dni:\n")

            # Nro Asiento seleccionado
            nro_asiento = input("Numero de asiento:\n")

            print("-----------------------------")
            # Crear reserva
            servicio_selec.agregar_reserva(nombre, email, dni, nro_asiento)

            #Mostrar estado actualizado de los asientos
            print("-----------------------------")
            print("Estado actualizado de los asientos: ")
            servicio_selec.get_asientos_unidad()
        elif eleccion == 2:
            #Fechas de ejemplo
            fecha = date(2023, 12, 31)
            fecha_hasta = date(2026, 12, 31)

            sistema.generar_informe(fecha, fecha_hasta)

        else: print("Elegir una de las opcines")
        eleccion = int(input("Seleccione la opcion:\n1: Hacer una reserva \n2: Generar informe \n3: Salir\n"))

    print("Gracias por visitarnos!")






