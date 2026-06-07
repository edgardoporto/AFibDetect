from fpdf import FPDF
import datetime

class ReporteClinicoECG(FPDF):
    def header(self):
        # Encabezado formal membretado
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 41, 59) # Gris oscuro elegante
        self.cell(0, 10, '🩺 SISTEMA COMPUTACIONAL AFIBDETECT v1.0', ln=True, align='L')
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 5, 'Plataforma Digital de Detección Automática de Arritmias de Alta Precisión', ln=True, align='L')
        self.line(10, 27, 200, 27) # Línea divisoria superior
        self.ln(8)

    def footer(self):
        # Pie de página con numeración estándar
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}} — Documento Informativo de Investigación Científica', align='C')

def generar_pdf_clinico(paciente, proc, resultados_inferencia):
    """
    Construye la estructura del reporte en PDF leyendo los datos en memoria RAM.
    """
    pdf = ReporteClinicoECG()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. BLOQUE DE METADATOS DEL PACIENTE
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, '1. INFORMACIÓN GENERAL DEL REGISTRO CLÍNICO', ln=True)
    pdf.line(10, pdf.get_y(), 80, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('Helvetica', '', 10)
    duracion_seg = paciente["total_muestras"] / paciente["frecuencia_muestreo"]
    
    pdf.cell(95, 6, f'• ID del Registro / Paciente: {paciente["id_registro"]}', ln=False)
    pdf.cell(95, 6, f'• Diagnóstico de Referencia: {paciente["etiqueta_referencia"]}', ln=True)
    pdf.cell(95, 6, f'• Frecuencia Muestreo Nativa: {paciente["frecuencia_muestreo"]} Hz', ln=False)
    pdf.cell(95, 6, f'• Duración Total: {duracion_seg:.2f} segundos', ln=True)
    pdf.cell(95, 6, f'• Canales Totales en Matriz: {paciente["num_derivaciones"]} derivaciones', ln=False)
    pdf.cell(95, 6, f'• Fecha/Hora de Auditoría: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}', ln=True)
    pdf.ln(5)
    
    # 2. CONFIGURACIÓN DEL PREPROCESAMIENTO
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '2. ESPECIFICACIONES DEL PIPELINE DE PREPROCESAMIENTO', ln=True)
    pdf.line(10, pdf.get_y(), 105, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(95, 6, f'• Derivación de Diseño Analizada: {proc.get("derivacion_procesada", "II")}', ln=False)
    pdf.cell(95, 6, f'• Frecuencia Destino (Resampling): {proc["fs_nueva"]} Hz', ln=True)
    pdf.cell(95, 6, f'• Filtro de Frecuencia: Butterworth Pasabanda (0.5 - 40.0 Hz)', ln=False)
    pdf.cell(95, 6, f'• Normalización de Amplitud: Z-score (Media 0, Varianza 1)', ln=True)
    pdf.cell(95, 6, f'• Ventana de Segmentación Rígida: {proc["cantidad_segmentos"]} bloques de 10 segundos', ln=True)
    pdf.ln(5)
    
    # 3. TABLA DE INFERENCIA POR SEGMENTOS
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 8, '3. ANALÍTICA DE PREDICCIONES PROBABILÍSTICAS DE LA IA (SOFTMAX)', ln=True)
    pdf.line(10, pdf.get_y(), 125, pdf.get_y())
    pdf.ln(4)
    
    # Encabezados de la Tabla
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(226, 232, 240) # Fondo gris tenue para los encabezados
    pdf.cell(20, 7, 'Segmento', border=1, align='C', fill=True)
    pdf.cell(45, 7, 'Predicción Ganadora', border=1, align='C', fill=True)
    pdf.cell(31, 7, 'Prob NSR', border=1, align='C', fill=True)
    pdf.cell(31, 7, 'Prob AF', border=1, align='C', fill=True)
    pdf.cell(31, 7, 'Prob Other', border=1, align='C', fill=True)
    pdf.cell(31, 7, 'Prob Noise', border=1, align='C', fill=True, ln=True)
    
    # Cuerpo de la Tabla
    pdf.set_font('Helvetica', '', 9)
    for seg in resultados_inferencia:
        pdf.cell(20, 6, str(seg["num_segmento"]), border=1, align='C')
        
        # Resaltamos visualmente si predice AF en el reporte
        if seg["diagnostico_ganador"] == "AF":
            pdf.set_text_color(220, 38, 38) # Letra roja para alertas críticas
            pdf.set_font('Helvetica', 'B', 9)
        else:
            pdf.set_text_color(15, 23, 42)
            pdf.set_font('Helvetica', '', 9)
            
        pdf.cell(45, 6, f'  {seg["diagnostico_ganador"]}', border=1, align='L')
        pdf.set_text_color(15, 23, 42) # Reseteo de color estándar
        pdf.set_font('Helvetica', '', 9)
        
        pdf.cell(31, 6, f'{seg["prob_NSR"]:.4f}', border=1, align='C')
        pdf.cell(31, 6, f'{seg["prob_AF"]:.4f}', border=1, align='C')
        pdf.cell(31, 6, f'{seg["prob_Other"]:.4f}', border=1, align='C')
        pdf.cell(31, 6, f'{seg["prob_Noise"]:.4f}', border=1, align='C', ln=True)
        
    pdf.ln(15)
    
    # 4. ÁREA DE FIRMA DE AUDITORÍA
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 10, '________________________________________', ln=True, align='C')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 4, 'Firma / Sello del Especialista Auditor', ln=True, align='C')
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, 'Validación y Control de Calidad del Diagnóstico por Computadora', ln=True, align='C')
    
    return pdf.output() # Retorna los bytes puros del archivo PDF
