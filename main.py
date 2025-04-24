from abc import ABC, abstractmethod


class Argentur:
    def __init__(self, sistema_activo):
        self.sistema_activo = sistema_activo
    def get_sistema_activo(self):
        return self.sistema_activo

class Servicio:
    def __init__(self, sistema_activo, unidad, fecha_partida, fecha_llegada,calidad,precio):
        self.unidad = unidad
        self.fecha_partida = fecha_partida
        self.fecha_llegada = fecha_llegada
        self.calidad = calidad
        self.precio = precio

class Itinerario:
    def __init__(self):
        pass

class Reserva:
    def __init__(self,fecha_hora):
        self.fecha_hora = fecha_hora

class Venta:
    def __init__(self,fecha_hora):
        self.fecha_hora = fecha_hora

class Ciudad:
    def __init__(self,codigo, nombre, provincia):
        self.codigo = codigo
        self.nombre = nombre
        self.provincia = provincia

class Unidad:
    def __init__(self,patente):
        self.patente = patente

class Pasajero:
    def __init__(self,nombre, email, dni):
        self.nombre = nombre
        self.email = email
        self.dni = dni

class MedioPago:
    @abstractmethod
    def __init__(self):
        pass

class TajetaCredito:
    def __init__(self, numero, dni, nombre,fecha_vencimiento):
        self.numero = numero
        self.dni = dni
        self.nombre = nombre
        self.fecha_vencimiento = fecha_vencimiento

class MercadoPago:
    def __init__(self,celular, email):
        self.celular = celular
        self.email = email

class Uala:
    def __init__(self,email, nombre_titular):
        self.email = email
        self.nombre_titular = nombre_titular










if __name__ == '__main__':
    pass