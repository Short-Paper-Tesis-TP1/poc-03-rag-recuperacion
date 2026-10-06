# -*- coding: utf-8 -*-
"""
Corpus SUSTITUTO de educacion financiera (es-PE).
Sustituto mecanico: valida el pipeline de recuperacion, NO el dominio.
En produccion se reemplaza por PDFs reales (SBS, BCRP, COFIDE) sin tocar el codigo.
Incluye DISTRACTORES a proposito: si el retrieval funciona, no deben salir.
"""

CORPUS = [
    # --- control de gastos / presupuesto ---
    dict(id="F01", fuente="Guia de presupuesto MYPE", pagina=12, tema="gastos",
         texto="El presupuesto mensual es la herramienta base para ordenar un negocio pequeno. "
               "Se recomienda registrar todos los egresos durante al menos tres meses seguidos, "
               "separandolos en gastos fijos y gastos variables. Los gastos hormiga, pequenos y "
               "frecuentes, suelen representar entre 10% y 15% del gasto total y son el primer "
               "lugar donde recortar sin afectar la operacion del negocio."),
    dict(id="F02", fuente="Guia de presupuesto MYPE", pagina=14, tema="gastos",
         texto="Cuando el gasto mensual promedio supera el 70% del ingreso, el margen para "
               "imprevistos desaparece. La recomendacion practica es fijar un techo de gasto "
               "por categoria y revisarlo semanalmente, empezando por las categorias de mayor "
               "monto acumulado y no por las de mayor frecuencia."),
    # --- separacion negocio / hogar ---
    dict(id="F03", fuente="Manual de finanzas del emprendedor", pagina=31, tema="separacion",
         texto="Mezclar el dinero del negocio con el del hogar impide saber si el emprendimiento "
               "es rentable. La practica recomendada es asignarse un sueldo fijo mensual como "
               "duena del negocio y mantener ese monto estable aunque las ventas suban, "
               "usando cuentas separadas para cada flujo."),
    # --- ahorro / fondo de emergencia ---
    dict(id="F04", fuente="Claves para ahorrar", pagina=5, tema="ahorro",
         texto="El fondo de emergencia debe cubrir entre tres y seis meses de gastos esenciales. "
               "Para quien no tiene ningun ahorro, la meta inicial no es ese monto completo sino "
               "un colchon equivalente a un mes de gastos, construido con aportes pequenos y "
               "constantes en lugar de aportes grandes y esporadicos."),
    dict(id="F05", fuente="Claves para ahorrar", pagina=8, tema="ahorro",
         texto="Ahorrar un porcentaje fijo del ingreso funciona mejor que ahorrar lo que sobra a "
               "fin de mes. Se sugiere separar el monto el mismo dia que ingresa el dinero. "
               "Un incremento gradual del 1% del ingreso cada dos meses es sostenible; saltos "
               "bruscos en la meta de ahorro suelen abandonarse antes del tercer mes."),
    # --- ingresos variables / estacionalidad ---
    dict(id="F06", fuente="Manual de finanzas del emprendedor", pagina=44, tema="volatilidad",
         texto="Los negocios con ventas estacionales deben planificar sobre el mes de menor "
               "ingreso del ano, no sobre el promedio. Presupuestar con el promedio genera "
               "deficit sistematico en los meses bajos y obliga a recurrir al credito de corto "
               "plazo justo cuando la capacidad de pago es menor."),
    dict(id="F07", fuente="Manual de finanzas del emprendedor", pagina=46, tema="volatilidad",
         texto="Ante ingresos irregulares se recomienda construir una reserva durante los meses "
               "de campana alta que cubra el deficit proyectado de los meses bajos. Esta reserva "
               "de nivelacion es distinta del fondo de emergencia y no debe usarse para cubrir "
               "imprevistos."),
    # --- sobreendeudamiento / multiples creditos ---
    dict(id="F08", fuente="Guia de uso responsable del credito", pagina=19, tema="deuda",
         texto="Mantener varias deudas simultaneas en distintas entidades eleva el costo total y "
               "dificulta el seguimiento de los vencimientos. Cuando existen tres o mas creditos "
               "activos conviene evaluar una consolidacion: un solo credito que cancele los "
               "demas, siempre que la tasa resultante sea menor al promedio ponderado actual."),
    dict(id="F09", fuente="Guia de uso responsable del credito", pagina=21, tema="deuda",
         texto="La cuota total de las deudas no deberia superar el 30% del ingreso mensual neto. "
               "Por encima de ese umbral se considera senal de alerta de sobreendeudamiento. "
               "Pagar solo el minimo de la tarjeta de credito extiende la deuda por anos y "
               "multiplica el monto final pagado."),
    dict(id="F10", fuente="Guia de uso responsable del credito", pagina=25, tema="deuda",
         texto="Antes de asumir una nueva deuda debe calcularse la capacidad de pago: ingreso neto "
               "menos gastos fijos menos cuotas vigentes. Si el resultado no cubre la nueva cuota "
               "con holgura, la decision correcta es postergar el credito y no reducir el gasto "
               "esencial del hogar."),
    dict(id="F11", fuente="Guia de uso responsable del credito", pagina=28, tema="deuda",
         texto="Si ya existe atraso en los pagos, la reprogramacion de deuda permite extender el "
               "plazo y bajar la cuota mensual. Conviene solicitarla antes de caer en mora, "
               "porque despues del incumplimiento las condiciones ofrecidas son peores y el "
               "historial crediticio queda afectado."),
    # --- historial crediticio ---
    dict(id="F12", fuente="Guia de uso responsable del credito", pagina=33, tema="historial",
         texto="El historial crediticio registra el comportamiento de pago y determina el acceso "
               "a futuros creditos y la tasa que se ofrece. Un historial limpio construido con "
               "creditos pequenos pagados puntualmente vale mas que la ausencia total de "
               "historial al momento de solicitar financiamiento para el negocio."),
    # --- DISTRACTORES: no deben aparecer en las consultas de arriba ---
    dict(id="D01", fuente="Guia de seguros", pagina=3, tema="DISTRACTOR",
         texto="El seguro vehicular cubre danos propios y a terceros. La prima depende del modelo "
               "del vehiculo, el ano de fabricacion y el historial de siniestros del conductor."),
    dict(id="D02", fuente="Guia previsional", pagina=7, tema="DISTRACTOR",
         texto="El sistema privado de pensiones acumula aportes en una cuenta individual de "
               "capitalizacion. La rentabilidad depende del tipo de fondo elegido y del horizonte "
               "de tiempo hasta la jubilacion."),
    dict(id="D03", fuente="Guia de inversiones", pagina=11, tema="DISTRACTOR",
         texto="Los fondos mutuos permiten invertir en un portafolio diversificado administrado "
               "por terceros. El valor cuota fluctua diariamente segun el mercado y no esta "
               "cubierto por el Fondo de Seguro de Depositos."),
    dict(id="D04", fuente="Boletin cambiario", pagina=1, tema="DISTRACTOR",
         texto="El tipo de cambio del dolar responde a factores externos como las tasas de la "
               "Reserva Federal y a factores internos como el riesgo pais y la balanza comercial."),
]

# Tabla de mapeo: nombre de columna del modelo -> frase del dominio.
MAPEO = {
    "gasto_mensual_promedio":  "control de gastos y presupuesto mensual del negocio",
    "ahorro_mensual":          "habito de ahorro y fondo de emergencia",
    "num_creditos_activos":    "multiples deudas simultaneas y sobreendeudamiento",
    "ratio_cuota_ingreso":     "capacidad de pago y porcentaje del ingreso destinado a cuotas",
    "ingreso_peor_mes":        "ingresos estacionales e irregulares del emprendimiento",
    "dias_atraso_max":         "atraso en pagos, mora y reprogramacion de deuda",
    "mezcla_negocio_hogar":    "separacion entre finanzas del negocio y del hogar",
    "antiguedad_crediticia":   "historial crediticio y acceso a financiamiento",
}

# Verdad de referencia: que fragmentos SON relevantes para cada variable.
# Definida a mano ANTES de correr el experimento.
RELEVANTES = {
    "gasto_mensual_promedio": {"F01", "F02"},
    "ahorro_mensual":         {"F04", "F05"},
    "num_creditos_activos":   {"F08", "F09", "F10"},
    "ratio_cuota_ingreso":    {"F09", "F10"},
    "ingreso_peor_mes":       {"F06", "F07"},
    "dias_atraso_max":        {"F11", "F09"},
    "mezcla_negocio_hogar":   {"F03"},
    "antiguedad_crediticia":  {"F12"},
}
