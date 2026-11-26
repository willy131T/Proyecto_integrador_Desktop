from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from config.settings import REPORTS_DIR, APP_NAME

class PDFService:
    @staticmethod
    def generar_receta_medica(paciente_nombre: str, doctor_nombre: str, procedimiento: str, medicamentos: str, fecha: str = None) -> str:
        """Genera un archivo PDF con la receta médica y retorna la ruta absoluta."""
        if not fecha:
            fecha = datetime.now().strftime("%d/%m/%Y")

        filename = f"Receta_{paciente_nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = REPORTS_DIR / filename

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(
            'TituloReceta',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#0284C7'),
            alignment=1, # Centro
            spaceAfter=6
        )
        subtitulo_style = ParagraphStyle(
            'SubTituloReceta',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#64748B'),
            alignment=1,
            spaceAfter=15
        )
        seccion_style = ParagraphStyle(
            'Seccion',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=10,
            spaceAfter=6
        )
        texto_style = ParagraphStyle(
            'TextoNormal',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155')
        )

        elementos = []

        # Encabezado Clínico
        elementos.append(Paragraph(f"🦷 {APP_NAME.upper()}", titulo_style))
        elementos.append(Paragraph("Especialidades Odontológicas Integrales • Cuidado y Salud Bucal", subtitulo_style))
        elementos.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284C7'), spaceAfter=15))

        # Ficha Informativa
        datos_cabecera = [
            [Paragraph(f"<b>Paciente:</b> {paciente_nombre}", texto_style), Paragraph(f"<b>Fecha:</b> {fecha}", texto_style)],
            [Paragraph(f"<b>Odontólogo Tratante:</b> {doctor_nombre}", texto_style), Paragraph("<b>Folio:</b> " + datetime.now().strftime('%y%m%d%H%M'), texto_style)]
        ]
        tabla_cabecera = Table(datos_cabecera, colWidths=[300, 230])
        tabla_cabecera.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elementos.append(tabla_cabecera)
        elementos.append(Spacer(1, 15))

        # Procedimiento Clínico Realizado
        elementos.append(Paragraph("🩺 Procedimiento Dental Realizado", seccion_style))
        elementos.append(Paragraph(procedimiento, texto_style))
        elementos.append(Spacer(1, 15))

        # Prescripción Farmacológica / Receta
        elementos.append(Paragraph("💊 Prescripción Médica e Indicaciones", seccion_style))
        elementos.append(Paragraph(medicamentos if medicamentos else "No se requieren medicamentos adicionales.", texto_style))
        elementos.append(Spacer(1, 40))

        # Firma
        elementos.append(HRFlowable(width="40%", thickness=1, color=colors.HexColor('#94A3B8'), spaceAfter=5, hAlign='CENTER'))
        elementos.append(Paragraph(f"<b>{doctor_nombre}</b><br/>Cirujano Dentista • Cédula Profesional Registrada", ParagraphStyle('Firma', parent=texto_style, alignment=1)))

        doc.build(elementos)
        return str(filepath)

    @staticmethod
    def generar_recibo_pago(
        paciente_nombre: str,
        concepto: str,
        monto: float,
        metodo_pago: str,
        estado: str,
        fecha: str = None,
        folio: str = None,
    ) -> str:
        """Genera un recibo oficial de pago odontológico en PDF y retorna la ruta absoluta."""
        if not fecha:
            fecha = datetime.now().strftime("%d/%m/%Y")
        if not folio:
            folio = datetime.now().strftime("%y%m%d%H%M")

        filename = f"Recibo_Pago_{paciente_nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = REPORTS_DIR / filename

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(
            "TituloRecibo",
            parent=styles["Heading1"],
            fontSize=20,
            textColor=colors.HexColor("#0D9488"),
            alignment=1,
            spaceAfter=6,
        )
        subtitulo_style = ParagraphStyle(
            "SubTituloRecibo",
            parent=styles["Normal"],
            fontSize=11,
            textColor=colors.HexColor("#64748B"),
            alignment=1,
            spaceAfter=15,
        )
        texto_style = ParagraphStyle(
            "TextoRecibo",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155"),
        )

        elementos = [
            Paragraph(f"💳 {APP_NAME.upper()} — RECIBO DE PAGO", titulo_style),
            Paragraph("Comprobante Oficial de Servicios Odontológicos", subtitulo_style),
            HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0D9488"), spaceAfter=15),
        ]

        datos = [
            [Paragraph("<b>Concepto / Campo</b>", texto_style), Paragraph("<b>Detalle</b>", texto_style)],
            [Paragraph("Folio de Operación:", texto_style), Paragraph(str(folio), texto_style)],
            [Paragraph("Fecha de Emisión:", texto_style), Paragraph(fecha, texto_style)],
            [Paragraph("Paciente:", texto_style), Paragraph(paciente_nombre, texto_style)],
            [Paragraph("Concepto / Tratamiento:", texto_style), Paragraph(concepto, texto_style)],
            [Paragraph("Método de Pago:", texto_style), Paragraph(metodo_pago, texto_style)],
            [Paragraph("Estado:", texto_style), Paragraph(estado, texto_style)],
            [Paragraph("<b>TOTAL:</b>", texto_style), Paragraph(f"<b>${float(monto):,.2f} MXN</b>", texto_style)],
        ]

        tabla = Table(datos, colWidths=[200, 330])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("PADDING", (0, 0), (-1, -1), 8),
        ]))
        elementos.append(tabla)
        elementos.append(Spacer(1, 30))
        elementos.append(Paragraph("Gracias por su confianza • OdontoCloud Gestión Odontológica", ParagraphStyle("PieRecibo", parent=texto_style, alignment=1)))

        doc.build(elementos)
        return str(filepath)
