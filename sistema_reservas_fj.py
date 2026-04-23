from abc import ABC, abstractmethod
from datetime import datetime

# ---------------- LOG ----------------
def registrar_log(mensaje):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {mensaje}\n")

# ---------------- EXCEPCIONES ----------------
class ErrorSistema(Exception):
    pass

class ErrorValidacion(ErrorSistema):
    pass

class ErrorReserva(ErrorSistema):
    pass

# ---------------- CLASE ABSTRACTA ----------------
class Entidad(ABC):
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre

# ---------------- CLIENTE ----------------
class Cliente(Entidad):
    def __init__(self, id, nombre, correo):
        super().__init__(id, nombre)
        self.set_correo(correo)

    def set_correo(self, correo):
        if "@" not in correo:
            raise ErrorValidacion("Correo inválido")
        self._correo = correo

    def get_info(self):
        return f"{self._nombre} - {self._correo}"

# ---------------- SERVICIO ABSTRACTO ----------------
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, *args):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ---------------- SERVICIOS ----------------
class ReservaSala(Servicio):
    def calcular_costo(self, horas, descuento=0):
        return (self.precio_base * horas) - descuento

    def descripcion(self):
        return "Reserva de sala"

class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias, impuesto=0.1):
        return (self.precio_base * dias) * (1 + impuesto)

    def descripcion(self):
        return "Alquiler de equipo"

class Asesoria(Servicio):
    def calcular_costo(self, horas):
        return self.precio_base * horas

    def descripcion(self):
        return "Asesoría especializada"

# ---------------- RESERVA ----------------
class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente inválido")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio inválido")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):
        try:
            costo = self.servicio.calcular_costo(self.duracion)
        except Exception as e:
            raise ErrorReserva("Error al calcular costo") from e
        else:
            self.confirmar()
            return costo
        finally:
            registrar_log(f"Reserva procesada para {self.cliente.get_info()}")

# ---------------- SIMULACIÓN ----------------
def simulacion():
    clientes = []
    servicios = []
    reservas = []

    # CLIENTES
    try:
        c1 = Cliente(1, "Juan", "juan@mail.com")
        clientes.append(c1)
    except Exception as e:
        registrar_log(e)

    try:
        c2 = Cliente(2, "Ana", "correo_invalido")
        clientes.append(c2)
    except Exception as e:
        registrar_log(e)

    # SERVICIOS
    s1 = ReservaSala("Sala VIP", 100)
    s2 = AlquilerEquipo("Proyector", 50)
    s3 = Asesoria("Consultoría", 200)

    servicios.extend([s1, s2, s3])

    # RESERVAS
    for i in range(10):
        try:
            cliente = clientes[0]
            servicio = servicios[i % 3]
            reserva = Reserva(cliente, servicio, i + 1)
            costo = reserva.procesar()
            print(f"Reserva {i+1} OK - Costo: {costo}")
            reservas.append(reserva)

        except Exception as e:
            registrar_log(e)
            print(f"Error en reserva {i+1}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    simulacion()