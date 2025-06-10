from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image  # Importar Pillow para trabajar con imágenes
from textwrap import wrap

def generar_historia_clinica(file_path="historia_clinica.pdf", paciente=None, servicios=None, empresa_cliente=None, contacto_paciente=None, historia_clinica=None,consultasmedicas_lista=None, servicios_lista = None):

    print("file_path",file_path)
    c = canvas.Canvas(file_path, pagesize=A4)

    # Tamaño de página (en puntos)
    width, height = A4  # A4: 595.27 x 841.89 puntos (1 punto = 1/72 pulgadas)
    
    # estandar
    margen_x = 56  # Margen izquierdo
    margen_y = 56  # Margen inferior

    c.setFillColorRGB(0.9, 0.9, 0.9)  # Color gris claro
    c.rect(margen_x-20, margen_y-20, width-margen_x*2+20*2, height-margen_y*2+20*2, fill=False)  # Rellena el rectángulo
    c.setFillColorRGB(0, 0, 0)  # Regresa el color del texto a negro

    # Imagen Logo de la empresa
    with Image.open(empresa_cliente.get('ruta_logo')) as img:
        img_width, img_height = img.size  # Dimensiones originales en píxeles

    desplazar = 0
    pagina = 1

    desplazar = encabezado(c,empresa_cliente,width,height,margen_x,margen_y,desplazar,'HISTORIA CLINICA VETERINARIA')

    # ENCABEZADO
    desplazar += 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margen_x, height - margen_y - desplazar, f"HC N°: {paciente.get('historia', 'N/A')}      fecha: {paciente.get('fecha', 'N/A')}")

    desplazar += 10
    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    # Dibujar la imagen (paciente) en una posición específica
    desplazar += 20

    # Ruta a la imagen
    imagen_path = paciente.get('ruta_imagen', 'N/A')

    if imagen_path:

        with Image.open(imagen_path) as img:
            img_width, img_height = img.size  # Dimensiones originales en píxeles

        # Convertir píxeles a puntos (1 punto = 1/72 pulgadas)
        img_width_points = img_width * 0.75
        img_height_points = img_height * 0.75

        x = width - 140  # Posición en X
        y = height - 40 - desplazar  # Posición en Y

        img_width = 100  # Ancho de la imagen
        img_height = (img_width * img_height_points ) / img_width_points  # Alto de la imagen

        c.drawImage(imagen_path, x, y-img_height, width=img_width, height=img_height)

    c.setFont("Helvetica-Bold", 12)
    desplazar += 2
    c.drawString(margen_x, height - margen_y - desplazar, f"Paciente: {paciente.get('nombre', 'N/A')}")

    c.setFont("Helvetica", 11)
    desplazar += 20
    c.drawString(margen_x, height - margen_y - desplazar, f"Especie - raza:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('especie_raza', 'N/A')}")

    c.drawString(margen_x, height - margen_y - desplazar, f"Especie - raza:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('especie_raza', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Sexo:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('sexo', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Edad:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('edad', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Peso:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('peso', 'N/A')} kg")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Color:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('color', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Chip:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('chip', 'N/A')}")

    desplazar += 20
    c.line(margen_x - 20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    desplazar += 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_x, height - margen_y - desplazar, f"Cliente: {contacto_paciente.get('nombres', 'N/A')}  ({contacto_paciente.get('tipo_contacto', 'N/A')})")
    c.setFont("Helvetica", 11)

    desplazar += 20
    c.drawString(margen_x, height - margen_y - desplazar, f"Documento:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{contacto_paciente.get('tipo_docid', 'N/A')} {contacto_paciente.get('docid', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Direccion:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{contacto_paciente.get('direccion', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"Telefonos:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{contacto_paciente.get('telefonos', 'N/A')}")

    desplazar += 16
    c.drawString(margen_x, height - margen_y - desplazar, f"EMAIL:")
    c.drawString(margen_x + 90, height - margen_y - desplazar, f"{contacto_paciente.get('email', 'N/A')}")

    desplazar += 10
    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    desplazar += 20
    # DETALLE ANAMNESIS
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_x, height - margen_y - desplazar, "Anamnesis")
    c.setFont("Helvetica", 11)

    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1

    desplazar += 20
    #texto_dividido = wrap(historia_clinica.get('anamnesis'), width=int((width - margen_x + 20) / 6))  # Ajusta proporcionalmente
    texto_dividido = historia_clinica.get('anamnesis','').splitlines()

    # Imprimir cada línea en el área especificada
    for linea in texto_dividido:

        # wrap trata el contenido como un texto continuo
        texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
        for linea2 in texto_dividido2:
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1
            c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
            desplazar += 16  # Reducir posición vertical para la siguiente línea

    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1

    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    desplazar += 20
    # DETALLE ANTECEDENTES MEDICOS
    c.setFont("Helvetica-Bold", 12)
    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1
    c.drawString(margen_x, height - margen_y - desplazar, "Antecedentes médicos")
    c.setFont("Helvetica", 11)

    desplazar += 20
    #texto_dividido = wrap(historia_clinica.get('antecedentes_medicos'), width=int((width - margen_x + 20) / 6))  # Ajusta proporcionalmente
    texto_dividido = historia_clinica.get('antecedentes_medicos','').splitlines()

    # Imprimir cada línea en el área especificada
    for linea in texto_dividido:

        # wrap trata el contenido como un texto continuo
        texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
        for linea2 in texto_dividido2:
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1
            c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
            desplazar += 16  # Reducir posición vertical para la siguiente línea

    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1

    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    desplazar += 20

    # DETALLE VACUNAS APLICADAS
    c.setFont("Helvetica-Bold", 12)
    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1
    c.drawString(margen_x, height - margen_y - desplazar, "Vacunas aplicadas")
    c.setFont("Helvetica", 11)

    desplazar += 20
    # wrap trata el contenido como un texto continuo
    #texto_dividido = wrap(historia_clinica.get('vacunas_aplicadas'), width=int((width - margen_x + 20) / 6)) #Ajusta proporcionalmente

    texto_dividido = historia_clinica.get('vacunas_aplicadas','').splitlines()

    # Imprimir cada línea en el área especificada
    for linea in texto_dividido:

        # wrap trata el contenido como un texto continuo
        texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
        for linea2 in texto_dividido2:
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1
            c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
            desplazar += 16  # Reducir posición vertical para la siguiente línea

    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1

    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    desplazar += 20
    # DETALLE DESPARASITACIONES
    c.setFont("Helvetica-Bold", 12)
    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1
    c.drawString(margen_x, height - margen_y - desplazar, "Desparasitaciones")
    c.setFont("Helvetica", 11)

    desplazar += 20
    #texto_dividido = wrap(historia_clinica.get('desparasitaciones'), width=int((width - margen_x + 20) / 6))  # Ajusta proporcionalmente
    texto_dividido = historia_clinica.get('desparasitaciones','').splitlines()

    # Imprimir cada línea en el área especificada
    for linea in texto_dividido:

        # wrap trata el contenido como un texto continuo
        texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
        for linea2 in texto_dividido2:
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1
            c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
            desplazar += 16  # Reducir posición vertical para la siguiente línea

    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1

    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    desplazar += 20

    # DETALLE MEDICAMENTOS APLICADOS
    if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
        desplazar = 0
        pagina += 1
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margen_x, height - margen_y - desplazar, "Medicamentos aplicados")
    c.setFont("Helvetica", 11)

    desplazar += 20
    #texto_dividido = wrap(historia_clinica.get('medicamentos_actuales'), width=int((width - margen_x + 20) / 6))  # Ajusta proporcionalmente
    texto_dividido = historia_clinica.get('medicamentos_actuales','').splitlines()

    # Imprimir cada línea en el área especificada
    for linea in texto_dividido:

        # wrap trata el contenido como un texto continuo
        texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
        for linea2 in texto_dividido2:
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1
            c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
            desplazar += 16  # Reducir posición vertical para la siguiente línea
    
    ## CONSULTAS MEDICAS

    for consulta in consultasmedicas_lista:

        corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina, True)
        pagina += 1
        desplazar = 0
        desplazar = encabezado(c,empresa_cliente,width,height,margen_x,margen_y,desplazar,'CONSULTA CLINICA :'+str(consulta['fecha']))

        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        # DATOS DEL VETERINARIO
        c.setFont("Helvetica-Bold", 12)

        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        desplazar += 20
        c.drawString(margen_x, height - margen_y - desplazar, "MEDICO VETERINARIO: "+consulta.get('veterinario',''))
        c.setFont("Helvetica", 11)

        desplazar += 16
        c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

        desplazar += 20

        c.setFont("Helvetica-Bold", 12)
        desplazar += 2
        c.drawString(margen_x, height - margen_y - desplazar, f"Paciente: {paciente.get('nombre', 'N/A')}")
        c.setFont("Helvetica", 11)
        desplazar += 20

        c.drawString(margen_x, height - margen_y - desplazar, f"Especie - raza:")
        c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('especie_raza', 'N/A')}")

        c.drawString(margen_x + 350, height - margen_y - desplazar, f"Sexo:")
        c.drawString(margen_x + 350 + 35, height - margen_y - desplazar, f"{paciente.get('sexo', 'N/A')}")

        desplazar += 16
        c.drawString(margen_x, height - margen_y - desplazar, f"Edad:")
        c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('edad', 'N/A')}")

        c.drawString(margen_x + 350, height - margen_y - desplazar, f"Peso:")
        c.drawString(margen_x + 350 + 35, height - margen_y - desplazar, f"{paciente.get('peso', 'N/A')} kg")

        desplazar += 16
        c.drawString(margen_x, height - margen_y - desplazar, f"Color:")
        c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('color', 'N/A')}")

        c.drawString(margen_x + 350, height - margen_y - desplazar, f"Chip:")
        c.drawString(margen_x + 350 + 35, height - margen_y - desplazar, f"{paciente.get('chip', 'N/A')}")

        desplazar += 20
        c.line(margen_x - 20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

        desplazar += 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, height - margen_y - desplazar, f"MOTIVO DE LA CONSULTA")
        c.setFont("Helvetica", 11)
        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        desplazar += 20
        texto_dividido = consulta['motivo'].splitlines()

        # Imprimir cada línea en el área especificada
        for linea in texto_dividido:

            # wrap trata el contenido como un texto continuo
            texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
            for linea2 in texto_dividido2:
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1
                c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
                desplazar += 16  # Reducir posición vertical para la siguiente línea

        c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)
        desplazar += 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, height - margen_y - desplazar, f"EXAMEN FISICO")
        c.setFont("Helvetica", 11)
        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        desplazar += 20
        texto_dividido = consulta['examen_fisico'].splitlines()

        # Imprimir cada línea en el área especificada
        for linea in texto_dividido:

            # wrap trata el contenido como un texto continuo
            texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
            for linea2 in texto_dividido2:
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1
                c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
                desplazar += 16  # Reducir posición vertical para la siguiente línea

        c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)
        desplazar += 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, height - margen_y - desplazar, f"DIAGNOSTICO")
        c.setFont("Helvetica", 11)
        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        desplazar += 20
        texto_dividido = consulta['diagnostico'].splitlines()

        # Imprimir cada línea en el área especificada
        for linea in texto_dividido:

            # wrap trata el contenido como un texto continuo
            texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
            for linea2 in texto_dividido2:
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1
                c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
                desplazar += 16  # Reducir posición vertical para la siguiente línea

        c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)
        desplazar += 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, height - margen_y - desplazar, f"TRATAMIENTO")
        c.setFont("Helvetica", 11)
        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        desplazar += 20
        texto_dividido = consulta['tratamiento'].splitlines()

        # Imprimir cada línea en el área especificada
        for linea in texto_dividido:

            # wrap trata el contenido como un texto continuo
            texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
            for linea2 in texto_dividido2:
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1
                c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
                desplazar += 16  # Reducir posición vertical para la siguiente línea

        c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

        desplazar += 20

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_x, height - margen_y - desplazar, f"NOTAS")
        c.setFont("Helvetica", 11)
        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
            desplazar = 0
            pagina += 1

        desplazar += 20
        texto_dividido = consulta['notas_adicionales'].splitlines()

        # Imprimir cada línea en el área especificada
        for linea in texto_dividido:

            # wrap trata el contenido como un texto continuo
            texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
            for linea2 in texto_dividido2:
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1
                c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
                desplazar += 16  # Reducir posición vertical para la siguiente línea

        ## RECETAS MEDICAS

        posologia_lista = consulta.get('posologia_lista',[])

        if posologia_lista != []:

            corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina, True)
            pagina += 1
            desplazar = 0
            desplazar = encabezado(c,empresa_cliente,width,height,margen_x,margen_y,desplazar,'RECETA MEDICA :'+str(consulta['fecha']))

            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1

            # DATOS DEL VETERINARIO
            c.setFont("Helvetica-Bold", 12)

            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1

            desplazar += 20
            c.drawString(margen_x, height - margen_y - desplazar, "MEDICO VETERINARIO: "+consulta.get('veterinario',''))
            c.setFont("Helvetica", 11)
            desplazar += 16
            c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

            desplazar += 20
            c.setFont("Helvetica-Bold", 12)
            desplazar += 2
            c.drawString(margen_x, height - margen_y - desplazar, f"Paciente: {paciente.get('nombre', 'N/A')}")
            c.setFont("Helvetica", 11)
            desplazar += 20

            c.drawString(margen_x, height - margen_y - desplazar, f"Especie - raza:")
            c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('especie_raza', 'N/A')}")

            c.drawString(margen_x + 350, height - margen_y - desplazar, f"Sexo:")
            c.drawString(margen_x + 350 + 35, height - margen_y - desplazar, f"{paciente.get('sexo', 'N/A')}")

            desplazar += 16
            c.drawString(margen_x, height - margen_y - desplazar, f"Edad:")
            c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('edad', 'N/A')}")

            c.drawString(margen_x + 350, height - margen_y - desplazar, f"Peso:")
            c.drawString(margen_x + 350 + 35, height - margen_y - desplazar, f"{paciente.get('peso', 'N/A')} kg")

            desplazar += 16
            c.drawString(margen_x, height - margen_y - desplazar, f"Color:")
            c.drawString(margen_x + 90, height - margen_y - desplazar, f"{paciente.get('color', 'N/A')}")

            c.drawString(margen_x + 350, height - margen_y - desplazar, f"Chip:")
            c.drawString(margen_x + 350 + 35, height - margen_y - desplazar, f"{paciente.get('chip', 'N/A')}")

            desplazar += 20
            c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

            desplazar += 20
            c.setFont("Helvetica-Bold", 9)
            c.drawString(margen_x, height - margen_y - desplazar, f"Farmaco")
            c.drawString(margen_x+150, height - margen_y - desplazar, f"Cantidad")
            c.drawString(margen_x+300, height - margen_y - desplazar, f"Dosis")

            for posologia in posologia_lista:

                c.setFont("Helvetica", 9)
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1

                desplazar += 20

                c.drawString(margen_x, height - margen_y - desplazar, f"{posologia['farmaco']}")
                c.drawString(margen_x+150, height - margen_y - desplazar, f"{posologia['cantidad']}")
                c.drawString(margen_x+300, height - margen_y - desplazar, f"{posologia['dosis']}")
                c.setFont("Helvetica", 11)
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1

        desplazar += 20

## SERVICIOS COMPLEMENTARIOS

    if servicios_lista:

        corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina, True)
        pagina += 1
        desplazar = 0
        desplazar = encabezado(c,empresa_cliente,width,height,margen_x,margen_y,desplazar,'SERVICIOS')

        desplazar += 20

        for servicio in servicios_lista:

            c.setFont("Helvetica-Bold", 12)
            c.drawString(margen_x, height - margen_y - desplazar, f"Del {(servicio[0])}")
            c.setFont("Helvetica", 11)
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1

            desplazar += 20

            if servicio[1] != "":
                c.setFont("Helvetica-Bold", 12)
                c.drawString(margen_x, height - margen_y - desplazar, f"Notas")
                c.setFont("Helvetica", 11)
                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1

                desplazar += 20
                texto_dividido = servicio[1].splitlines()

                # Imprimir cada línea en el área especificada
                for linea in texto_dividido:

                    # wrap trata el contenido como un texto continuo
                    texto_dividido2 = wrap(linea, width=int((width - margen_x + 80) / 6)) #Ajusta proporcionalmente
                    for linea2 in texto_dividido2:
                        if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                            desplazar = 0
                            pagina += 1
                        c.drawString(margen_x, height - margen_y - desplazar, f"{linea2}")
                        desplazar += 16  # Reducir posición vertical para la siguiente línea

                desplazar += 5  # Reducir posición vertical para la siguiente línea

            c.setFont("Helvetica-Bold", 12)
            c.drawString(margen_x, height - margen_y - desplazar, f"Detalle")
            c.setFont("Helvetica", 11)
            if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                desplazar = 0
                pagina += 1

            desplazar += 20

            servicios_cabecera = servicio[2]

            for servicio_detalle in servicios_cabecera:
                
                texto = ' - '+servicio_detalle['nombre']

                if corte_pagina(c, height - margen_y - desplazar, width, height, margen_x, margen_y,pagina):
                    desplazar = 0
                    pagina += 1
                c.drawString(margen_x, height - margen_y - desplazar, f"{texto}")
                desplazar += 16  # Reducir posición vertical para la siguiente líne

            c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)
            desplazar += 20

    c.save()

def corte_pagina(c, pos_y_actual, width, height, margen_x, margen_y, pagina, corte_pagina = False):
    
    corte = False
    if pos_y_actual < 54 or corte_pagina:

        corte = True
        if pagina == 1:
            c.setFont("Helvetica-Bold", 8)
            c.drawString(width/2-20, 24, "Pág-"+str(pagina).zfill(2))
            c.setFont("Helvetica", 11)

        c.showPage()
        c.setFillColorRGB(0.9, 0.9, 0.9)  # Color gris claro
        c.rect(margen_x-20, margen_y-20, width-margen_x*2+20*2, height-margen_y*2+20*2, fill=False)  # Rellena el rectángulo
        c.setFillColorRGB(0, 0, 0)  # Regresa el color del texto a negro

        c.setFont("Helvetica-Bold", 8)
        c.drawString(width/2-20, 24, "Pág-"+str(pagina+1).zfill(2))
        c.setFont("Helvetica", 11)

    return corte

def encabezado(c,empresa_cliente,width,height, margen_x, margen_y,desplazar,titulo):

    # Imagen Logo de la empresa
    with Image.open(empresa_cliente.get('ruta_logo')) as img:
        img_width, img_height = img.size  # Dimensiones originales en píxeles

    # Convertir píxeles a puntos (1 punto = 1/72 pulgadas)
    img_width_points = img_width * 0.75
    img_height_points = img_height * 0.75

    # Dibujar la imagen (logo empresa) en una posición específica

    x = width - 120  # Posición en X
    y = height - 38  # Posición en Y
    img_width = 82  # Ancho de la imagen
    img_height = (img_width * img_height_points ) / img_width_points  # Alto de la imagen

    print('x',x,'y',y,img_height,img_width)

    c.drawImage(empresa_cliente.get('ruta_logo'), x, y-img_height, width=img_width, height=img_height)

    # TITULO
    desplazar += 10
    c.setFont("Helvetica-Bold", 15)
    c.drawString(margen_x, height - margen_y - desplazar, f"{titulo}")

    c.setFillColorRGB(0.262, 0.557, 0.314)
    c.setFont("Helvetica-Bold", 14)

    desplazar += 20
    c.drawString(margen_x, height - margen_y - desplazar, f"{empresa_cliente.get('nombre')}")

    c.setFont("Helvetica-Bold", 9)
    desplazar += 15
    c.drawString(margen_x, height - margen_y - desplazar, f"RUC {empresa_cliente.get('ruc')} domicilio {empresa_cliente.get('direccion')}")

    desplazar += 10
    c.drawString(margen_x, height - margen_y - desplazar, f"Telef {empresa_cliente.get('telefono')} email {empresa_cliente.get('email')}")

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0, 0, 0)  # negro

    desplazar += 15
    c.line(margen_x-20, height - margen_y - desplazar, width - margen_x + 20, height - margen_y - desplazar)

    return desplazar