from abc import ABC, abstractmethod
from datetime import date
import random
#%%
class Argentur:
    def __init__(self, sistema_activo):
        self.sistema_activo = sistema_activo
        self.servicio = []
        self.ventas_totales = []

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
        for v in self.ventas_totales:
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
        for v in self.ventas_totales:
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

    def actualizar_ventas(self):
        self.ventas_totales = []
        for s in self.servicio:
            ventas_servicio = s.get_ventas()
            for v in ventas_servicio:
                self.ventas_totales.append(v)

    def generar_informe(self,fecha_desde,fecha_hasta):
        self.actualizar_ventas()
        self.calcular_monto_total(fecha_desde,fecha_hasta)
        print("-----------------------------")
        self.ver_viajes_destino(fecha_desde,fecha_hasta)
        print("-----------------------------")
        self.ver_pagos(fecha_desde, fecha_hasta)
#%%
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

    def get_ventas(self):
        return self.ventas

    def agregar_reserva(self, nombre, email, dni, nro_asiento):
        asiento = self.unidad.asiento_disponible(nro_asiento)
        reserva = False
        if not self.unidad.ocupar_asiento(asiento):
            self.reservas.append(Reserva(date.today(),nombre, email, dni, asiento))
            reserva = True
        else:
            reserva = False
        return reserva

    def generar_venta_servicio(self,reserva,medio_pago,monto):
        self.ventas.append(Venta(date.today(),reserva.get_asiento(),medio_pago,reserva.get_pasajero(),monto))

#%%
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
#%%
class Ciudad:
    def __init__(self,codigo, nombre, provincia):
        self.codigo = codigo
        self.nombre = nombre
        self.provincia = provincia

    def get_nombre(self):
        return self.nombre
#%%
class Reserva:
    def __init__(self,fecha_hora,nombre, email, dni, asiento):
        self.fecha_hora = fecha_hora
        self.pasajero =Pasajero(nombre, email, dni, asiento)
    def get_pasajero(self):
        return self.pasajero
    def get_fecha_hora(self):
        return self.fecha_hora
    def get_asiento(self):
        return self.pasajero.get_asiento()
#%%
class Pasajero:
    def __init__(self,nombre, email, dni,asiento):
        self.nombre = nombre
        self.email = email
        self.dni = dni
        self.asiento = asiento

    def get_nombre(self):
        return self.nombre
    def get_asiento(self):
        return self.asiento
#%%
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
        if not asiento.get_ocupado():
            asiento.set_ocupado()
            estaba_ocupado = False
        return estaba_ocupado

    def asiento_disponible(self, nro_asiento):
        for i in self.asientos:
            if i.get_numero() == nro_asiento:
                return i
#%%
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
#%%
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
#%%
class MedioPago(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_tipo(self):
        pass
#%%
class TajetaCredito(MedioPago):
    def __init__(self, numero, dni, nombre,fecha_vencimiento):
        self.numero = numero
        self.dni = dni
        self.nombre = nombre
        self.fecha_vencimiento = fecha_vencimiento

    def get_tipo(self):
        return "Pago con Tajeta de Credito"
#%%
class MercadoPago(MedioPago):
    def __init__(self,celular, email):
        self.celular = celular
        self.email = email

    def get_tipo(self):
        return "Pago con Mercado Pago"
#%%
class Uala(MedioPago):
    def __init__(self,email, nombre_titular):
        self.email = email
        self.nombre_titular = nombre_titular

    def get_tipo(self):
        return "Pago con Uala"
#%%
if __name__ == '__main__':
    random.seed(42)  # Para que los datos aleatorios sean reproducibles

    # Crear ciudades
    ciudades = [
        Ciudad(1, "Buenos Aires", "Buenos Aires"),
        Ciudad(2, "Rosario", "Santa Fe"),
        Ciudad(3, "Córdoba", "Córdoba"),
        Ciudad(4, "Mendoza", "Mendoza"),
        Ciudad(5, "Salta", "Salta"),
        Ciudad(6, "Bariloche", "Río Negro")
    ]

    # Crear itinerarios aleatorios
    itinerarios = []
    for _ in range(5):
        seleccionadas = random.sample(ciudades, random.randint(2, 4))
        itinerarios.append(Itinerario(seleccionadas))

    # Crear unidades
    unidades = []
    for i in range(5):
        asientos = [Asiento(str(j), random.choice([False, False, True])) for j in range(20)]  # más libres que ocupados
        unidades.append(Unidad(f"PAT{i:03}", asientos))

    # Crear servicios
    servicios = []
    calidades = ["Premium", "Económico", "Ejecutivo"]
    for i in range(5):
        fecha_partida = date(2025, random.randint(1, 12), random.randint(1, 28))
        fecha_llegada = date(2025, random.randint(1, 12), random.randint(1, 28))
        while fecha_llegada <= fecha_partida:
            fecha_llegada = date(2025, random.randint(1, 12), random.randint(1, 28))
        servicios.append(
            Servicio(f"serv{i+1}", unidades[i], fecha_partida, fecha_llegada,
                     random.choice(calidades), random.randint(5000, 20000), itinerarios[i])
        )

    # Crear sistema Argentur
    sistema = Argentur(True)
    sistema.add_servicio(servicios)

    # Crear medios de pago
    medios_pago = [
        TajetaCredito("1111222233334444", "12345678", "Juan Perez", "12/26"),
        MercadoPago("1122334455", "maria@gmail.com"),
        Uala("carlos@uala.com", "Carlos Gomez")
    ]

    # Crear reservas y ventas automáticamente
    nombres = ["Lucas", "María", "Juan", "Ana", "Pedro", "Lucía", "Santiago", "Carla", "Mateo", "Sofía"]
    for servicio in servicios:
        for _ in range(random.randint(8, 15)):  # cada servicio tendrá entre 3 y 7 ventas
            nombre = random.choice(nombres)
            email = nombre.lower() + str(random.randint(1, 100)) + "@gmail.com"
            dni = random.randint(20000000, 45000000)
            nro_asiento = str(random.randint(0, 19))

            servicio.agregar_reserva(nombre, email, dni, nro_asiento)

            # Tomar última reserva agregada para la venta
            if servicio.reservas:
                reserva = servicio.reservas[-1]
                medio_pago = random.choice(medios_pago)
                monto = random.randint(5000, 20000)
                servicio.generar_venta_servicio(reserva, medio_pago, monto)

    # =============================Programa Principal========================================

    eleccion = 0
    while eleccion != 3:
        eleccion = int(input("Seleccione la opcion:\n1.Hacer una reserva\n2.Generar informe\n3.Salir\n"))
        if eleccion == 1:
            print("============SERVICIOS DISPONIBLES===================")
            sistema.get_servicio()
            print("----------------------------------------------------")
            serv_selec = False
            while not serv_selec:
                codigo_servicio = input("seleccione el servicio: ")
                codigo_servicio = codigo_servicio.lower()
                servicio_select = sistema.get_servicio_unico(codigo_servicio)
                if servicio_select == None:
                    serv_selec = False
                    print("------------------------------------------------------")
                else:
                    serv_selec = True

            print(f"Usted selecciono el servicio: {servicio_select.get_cod_servicio()}")
            servicio_select.get_asientos_unidad()
            print("----------------------------------------------------")
            print("Complete los siguientes datos para realizar una reserva:")
            nombre = input("Nombre:\n")
            email = input("Email:\n")
            dni = input("Dni:\n")
            asiento_selec = False
            while not asiento_selec:
                nro_asiento = input("Numero de asiento:\n")
                print("----------------------------------------------------")
                if not servicio_select.agregar_reserva(nombre, email, dni, nro_asiento):
                    print("asiento ocupado")
                    asiento_selec = False
                else:
                    asiento_selec = True

            print(f"Reserva realizada: pasajero: {nombre}, asiento: {nro_asiento}, servicio del {servicio_select.get_fecha_partida()}")
            print("----------------------------------------------------")
            print("Estado acutalizado de los asientos:")
            servicio_select.get_asientos_unidad()
        elif eleccion == 2:
            print("==================GENERAR INFORME=====================")

            print("Seleccione fecha desde:")
            fecha_desde_año = int(input("Seleccione año:"))
            fecha_desde_mes = int(input("Seleccione mes:"))
            fecha_desde_dia = int(input("Seleccione dia:"))
            fecha_desde = date(fecha_desde_año, fecha_desde_mes, fecha_desde_dia)

            print("Seleccione fecha hasta:")
            fecha_hasta_año = int(input("Seleccione año:"))
            fecha_hasta_mes = int(input("Seleccione mes:"))
            fecha_hasta_dia = int(input("Seleccione dia:"))
            fecha_hasta = date(fecha_hasta_año, fecha_hasta_mes, fecha_hasta_dia)

            print("Informe:")
            sistema.generar_informe(fecha_desde, fecha_hasta)
    print("Gracias por visitarnos!")