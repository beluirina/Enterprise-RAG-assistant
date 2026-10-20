"""
Genera los PDFs de ejemplo de la empresa ficticia (NovaTech).

Los dejo como script para que se pueda ver de dónde salen los PDFs
y para poder regenerarlos si cambio el texto.

Uso:  python scripts/generar_pdfs.py
"""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"

# Cada documento es una lista de "páginas"; cada página es una lista de (tipo, texto)
DOCUMENTOS = {
    "politica_gastos_viaticos.pdf": [
        [
            ("h1", "Política de Gastos y Viáticos"),
            ("p", "NovaTech Soluciones S.A. - Gerencia de Administración y Finanzas. Versión 4.0, vigente desde enero de 2026."),
            ("h2", "1. Alcance"),
            ("p", "Esta política aplica a los gastos que hacen los empleados en viajes de trabajo, visitas a clientes y eventos. Las compras de bienes y servicios para la empresa se rigen por el Procedimiento de Compras."),
            ("h2", "2. Aprobación previa del viaje"),
            ("p", "Todo viaje de trabajo debe ser aprobado por el gerente del área antes de reservar pasajes o alojamiento. Los viajes al exterior también necesitan la aprobación del Director del área. Las reservas se hacen a través de la agencia de viajes corporativa, no de forma particular."),
            ("h2", "3. Pasajes"),
            ("p", "Los vuelos se compran siempre en clase económica. Se permite clase ejecutiva únicamente en vuelos de más de 8 horas de duración y con aprobación del Director del área. Para viajes de menos de 400 km se recomienda usar micro o auto."),
        ],
        [
            ("h2", "4. Límites de gastos diarios"),
            ("p", "Comidas en viajes nacionales: hasta ARS 30.000 por día por persona. Comidas en viajes al exterior: hasta USD 60 por día por persona."),
            ("p", "Alojamiento en viajes nacionales: hasta ARS 90.000 por noche. Alojamiento en el exterior: hasta USD 180 por noche. Los hoteles se reservan con la agencia corporativa."),
            ("p", "Taxis y aplicaciones de transporte: se reintegran los traslados hacia y desde aeropuertos y terminales, y los traslados por trabajo después de las 22:00 horas."),
            ("p", "No se reintegran bebidas alcohólicas, multas de tránsito, gastos de familiares ni compras personales."),
            ("h2", "5. Anticipos"),
            ("p", "Se puede pedir un anticipo de viáticos de hasta el 70% del gasto estimado. El anticipo se pide en MiGente con al menos 5 días hábiles de anticipación al viaje."),
        ],
        [
            ("h2", "6. Rendición de gastos"),
            ("p", "Los gastos se rinden en el módulo Gastos de MiGente dentro de los 10 días hábiles posteriores al regreso del viaje. Cada gasto debe tener su comprobante (factura o ticket) escaneado o fotografiado. Los gastos sin comprobante no se reintegran."),
            ("p", "Las rendiciones de más de ARS 200.000 necesitan la aprobación del gerente del área además de la del líder directo."),
            ("p", "El reintegro se deposita en la cuenta sueldo dentro de los 15 días posteriores a la aprobación."),
            ("h2", "7. Tarjeta corporativa"),
            ("p", "Los empleados que viajan más de 4 veces por año pueden pedir una tarjeta de crédito corporativa. El límite mensual es de ARS 1.000.000. La tarjeta es solo para gastos de trabajo y el uso personal es una falta grave."),
        ],
    ],
    "politica_seguridad_informatica.pdf": [
        [
            ("h1", "Política de Seguridad de la Información"),
            ("p", "NovaTech Soluciones S.A. - Área de Seguridad Informática. Versión 5.2. Aplica a todos los empleados, contratistas y proveedores con acceso a sistemas de NovaTech."),
            ("h2", "1. Contraseñas"),
            ("p", "Las contraseñas deben tener como mínimo 12 caracteres e incluir mayúsculas, minúsculas, números y símbolos. Se deben cambiar cada 90 días y no se pueden repetir las últimas 5 contraseñas. Está prohibido compartir contraseñas o anotarlas en papel. Se recomienda usar el gestor de contraseñas corporativo 1Password."),
            ("h2", "2. Autenticación multifactor"),
            ("p", "La autenticación multifactor (MFA) es obligatoria para el correo, la VPN, GitHub y todos los sistemas que la soporten. Se usa la aplicación Okta Verify. No se aceptan códigos por SMS."),
            ("h2", "3. Bloqueo de pantalla"),
            ("p", "Las computadoras deben bloquearse automáticamente después de 5 minutos de inactividad. Al alejarse del puesto, hay que bloquear la pantalla manualmente."),
        ],
        [
            ("h2", "4. Clasificación de la información"),
            ("p", "Toda la información de NovaTech se clasifica en cuatro niveles: Pública, Interna, Confidencial y Restringida."),
            ("p", "Pública: puede compartirse fuera de la empresa, por ejemplo el sitio web. Interna: solo para empleados, por ejemplo esta política. Confidencial: datos de clientes, contratos y datos financieros; solo para quienes los necesitan para su trabajo. Restringida: claves de producción, datos de tarjetas e información de fusiones; acceso nominal aprobado por el CISO."),
            ("p", "La información Confidencial y Restringida no puede enviarse a correos personales ni subirse a herramientas externas, incluyendo asistentes de inteligencia artificial no aprobados por Seguridad Informática."),
            ("h2", "5. Dispositivos USB"),
            ("p", "Está prohibido el uso de pendrives y discos externos en las notebooks corporativas. Los puertos USB de almacenamiento están bloqueados. Para compartir archivos se usa Google Drive corporativo."),
        ],
        [
            ("h2", "6. Phishing y reporte de incidentes de seguridad"),
            ("p", "Si recibís un correo sospechoso, no hagas clic en los enlaces ni descargues adjuntos. Reportalo con el botón 'Reportar phishing' de Gmail o reenvialo a seguridad@novatech.com.ar. Si ya hiciste clic o ingresaste tu contraseña, avisá a Seguridad Informática dentro de la primera hora y cambiá tu contraseña de inmediato."),
            ("p", "Seguridad Informática hace simulaciones de phishing cada trimestre. Quien cae en dos simulaciones seguidas debe repetir el curso de Seguridad de la Información."),
            ("h2", "7. Software permitido"),
            ("p", "Solo se puede instalar software del catálogo de Autoservicio de la empresa. Para pedir un programa que no está en el catálogo hay que abrir un ticket en Mesa de Ayuda, que lo envía a Seguridad Informática para su revisión."),
            ("h2", "8. Incumplimientos"),
            ("p", "El incumplimiento de esta política puede derivar en sanciones disciplinarias, incluyendo el despido con causa en casos graves."),
        ],
    ],
    "codigo_de_conducta.pdf": [
        [
            ("h1", "Código de Conducta y Ética"),
            ("p", "NovaTech Soluciones S.A. - Aprobado por el Directorio. Versión 2025."),
            ("h2", "1. Nuestros valores"),
            ("p", "En NovaTech trabajamos con integridad, respeto, transparencia y foco en el cliente. Este código aplica a empleados, directores, contratistas y proveedores."),
            ("h2", "2. Respeto y no discriminación"),
            ("p", "No se tolera ninguna forma de discriminación, acoso o violencia, ya sea por género, orientación sexual, edad, religión, origen, discapacidad o cualquier otra condición. Esto aplica tanto en la oficina como en reuniones virtuales, eventos y redes sociales."),
            ("h2", "3. Regalos e invitaciones"),
            ("p", "Los empleados pueden aceptar regalos de clientes o proveedores solo si su valor no supera los USD 50 y no se reciben con frecuencia. Los regalos de mayor valor deben rechazarse amablemente o informarse al área de Compliance. Nunca se aceptan regalos en efectivo, sin importar el monto. Está prohibido aceptar regalos de proveedores que estén participando de una licitación."),
        ],
        [
            ("h2", "4. Conflicto de intereses"),
            ("p", "Hay conflicto de intereses cuando un interés personal puede afectar una decisión de trabajo, por ejemplo contratar a un proveedor donde trabaja un familiar. Todo posible conflicto de intereses debe declararse por escrito al área de Compliance apenas se detecta, completando el formulario en MiGente. Además, todos los empleados renuevan su declaración jurada de conflicto de intereses una vez por año, en el mes de abril."),
            ("h2", "5. Uso de redes sociales"),
            ("p", "Los empleados pueden mencionar que trabajan en NovaTech, pero no pueden publicar información interna o confidencial, ni hablar en nombre de la empresa sin autorización del área de Comunicación."),
            ("h2", "6. Línea Ética"),
            ("p", "Cualquier persona puede reportar incumplimientos de este código a través de la Línea Ética, de forma anónima si lo prefiere. La Línea Ética la administra un proveedor externo independiente y está disponible las 24 horas, por teléfono al 0800-555-6682 o en el sitio etica.novatech.com.ar. Está prohibida cualquier represalia contra quien haga un reporte de buena fe."),
            ("h2", "7. Sanciones"),
            ("p", "Las faltas a este código se analizan en el Comité de Ética, que se reúne una vez por mes. Las sanciones van desde un apercibimiento hasta el despido con causa."),
        ],
    ],
}


def construir_pdf(nombre, paginas):
    estilos = getSampleStyleSheet()
    mapa = {"h1": estilos["Title"], "h2": estilos["Heading2"], "p": estilos["BodyText"]}

    elementos = []
    for i, pagina in enumerate(paginas):
        for tipo, texto in pagina:
            elementos.append(Paragraph(texto, mapa[tipo]))
            elementos.append(Spacer(1, 6))
        if i < len(paginas) - 1:
            elementos.append(PageBreak())

    ruta = DOCS_DIR / nombre
    SimpleDocTemplate(str(ruta), pagesize=A4, title=nombre).build(elementos)
    print(f"Generado: {ruta}")


if __name__ == "__main__":
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for nombre, paginas in DOCUMENTOS.items():
        construir_pdf(nombre, paginas)
