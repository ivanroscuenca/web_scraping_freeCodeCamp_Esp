from bs4 import BeautifulSoup
import requests

# Empezamos el scraping

# 1. Obtener el HTML
URL_BASE = 'https://scrapepark.org/courses/spanish/'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

# 2. "Parsear" ese HTML
soup = BeautifulSoup(html_obtenido, "html.parser")


# El método find()
# Nos permite quedarnos con la información asociada a una etiqueta de HTML

primer_h2 = soup.find('h2')
print(primer_h2)

## **El método `find_all()`**

# Busca **TODOS** los elementos de la página con esa etiqueta y devuelve una "lista"
# que los contiene (en realidad devuelve un objeto de la clase *bs4.element.ResultSet*).
h2_todos = soup.find_all('h2')
print(h2_todos)
# ARGUMENTOS
# Si usamos el parametro limit = 1, emulamos al metodo find
h2_uno_solo = soup.find_all('h2',limit=1)
print(h2_uno_solo)

# Podemos iterar sobre el objeto
for seccion in h2_todos:
  print(seccion.text)

# get_text() para más funcionalidades
for seccion in h2_todos:
  print(seccion.get_text(strip=True))

# Utilizando atributos de las etiquetas

# Clase
divs = soup.find_all('div', class_ = "heading-container heading-center")

for div in divs:
  print(div)
  print(" ")

# Todas las etiquetas que tengan el atributo "src"
src_todos = soup.find_all(src=True)

for elemento in src_todos:
  if elemento['src'].endswith(".jpg"):
    print(elemento)

#@title Ejercicio: Bajar todas las imagenes!

# Inicializamos una lista vacía para almacenar las URLs de las imágenes que cumplan con ciertos criterios.
url_imagenes = []

# Recorremos todos los elementos en 'src_todos', obteniendo tanto el índice 'i' como el diccionario 'imagen'.
for i, imagen in enumerate(src_todos):

  # Verificamos si el valor asociado con la clave 'src' del diccionario 'imagen' termina en 'png'.
  if imagen['src'].endswith('png'):
    # Imprimimos la URL de la imagen que termina en 'png' para depuración o verificación.
    print(imagen['src'])

    # Realizamos una solicitud HTTP GET para descargar la imagen desde la URL construida.
    # La URL base es "https://scrapepark.org/courses/spanish/" y añadimos el valor de 'imagen['src']' al final.
    r = requests.get(f"https://scrapepark.org/courses/spanish/{imagen['src']}")

    # Abrimos un nuevo archivo en modo binario de escritura ('wb') con un nombre secuencial, por ejemplo, 'imagen_0.png'.
    with open(f'img_{i}.png', 'wb') as f:
      # Escribimos el contenido de la respuesta HTTP (los datos de la imagen) en el archivo abierto.
      f.write(r.content)

# Información de tablas

# URL base del sitio web donde se encuentran los cursos de español.
URL_BASE = 'https://scrapepark.org/courses/spanish'

# Se utiliza BeautifulSoup para encontrar el primer elemento <iframe> en la página HTML.
# El atributo 'src' del <iframe> contiene la URL de la tabla que queremos scrape.
URL_TABLA = soup.find_all('iframe')[0]['src']

# Realizamos una solicitud GET para obtener el contenido de la página donde se encuentra la tabla.
request_tabla = requests.get(f'{URL_BASE}/{URL_TABLA}')

# Obtenemos el contenido HTML de la página solicitada.
html_tabla = request_tabla.text

# Utilizamos BeautifulSoup nuevamente para analizar el contenido HTML de la tabla.
soup_tabla = BeautifulSoup(html_tabla, "html.parser")

# Encontramos el elemento <table> en el HTML, que contiene los datos que buscamos.
soup_tabla.find('table')

# Buscamos todas las celdas de la tabla (<th> o <td>) que tienen un estilo específico.
# En este caso, buscamos las celdas cuyo texto está en color rojo ('color: red;'),
# que presumiblemente indica productos faltantes.
productos_faltantes = soup_tabla.find_all(['th', 'td'], attrs={'style':'color: red;'})

# Extraemos el texto de cada celda de producto faltante.
# Se itera sobre la lista productos_faltantes y se extrae el texto de cada elemento,
# formando una lista final de nombres de productos faltantes.
productos_faltantes = [producto.text for producto in productos_faltantes]

# Imprimimos la lista de productos faltantes.
print(productos_faltantes)

# Buscar precios

divs = soup.find_all('div', class_='detail-box')
productos = []
precios = []

for div in divs:
  if (div.h6 is not None) and ('Patineta' in div.h5.text):
    producto = div.h5.get_text(strip=True)
    precio = div.h6.get_text(strip=True).replace('$', '')
    # Se puede agregar filtros
    print(f'producto: {producto:<16} | precio: {precio}')
    productos.append(producto)
    precios.append(precio)

# Itera sobre cada div en la lista de divs
for div in divs:

  # Verifica si el div tiene un elemento <h6> y si existe algún texto en el elemento <h5>
  if (div.h6 is not None) and (div.h5 and div.h5.text.strip()):
    # Extrae el texto del elemento <h5>, eliminando cualquier espacio en blanco alrededor del texto
    producto = div.h5.get_text(strip=True)

    # Extrae el texto del elemento <h6>, eliminando cualquier espacio en blanco alrededor del texto y
    # reemplazando el símbolo '$' con una cadena vacía para limpiar el precio
    precio = div.h6.get_text(strip=True).replace('$', '')

    # Se puede agregar filtros

    # Imprime el producto y el precio formateados, donde el nombre del producto se ajusta a la izquierda con un ancho de 16 caracteres
    print(f'producto: {producto:<16} | precio: {precio}')

    # Agrega el nombre del producto a la lista de productos
    productos.append(producto)

    # Agrega el precio a la lista de precios
    precios.append(precio)

# **Cambios que dependen de la URL**

URL_BASE = "https://scrapepark.org/courses/spanish/contact"

# Itera sobre el rango de 1 a 2 (el 3 no está incluido)
for i in range(1, 3):
  # Construye la URL final concatenando la URL base con el número actual del rango
  URL_FINAL = f"{URL_BASE}{i}"
  # Imprime la URL final generada para cada iteración
  print(URL_FINAL)
  # Realiza una solicitud HTTP GET a la URL final
  r = requests.get(URL_FINAL)
  # Crea un objeto BeautifulSoup con el contenido de la página descargada
  soup = BeautifulSoup(r.text, "html.parser")

  # Imprime el texto dentro del primer elemento <h5> encontrado en la página
  # Puede causar error si no existe un elemento <h5> en la página
  print(soup.h5.text)

  # Crea un objeto BeautifulSoup
  soup2 = BeautifulSoup(r.text, 'html.parser')
  # Encontrar el elemento <a> con la clase 'footer-logo'
  footer_logo = soup2.find('a', class_='footer-logo')
  # Obtener el texto dentro del elemento <a>
  texto = footer_logo.get_text(strip=True)
  # Imprimir el texto
  print(texto)


#Datos que no sabemos en que parte de la página se encuentran

# Expresiones regulares
import re

# 1. Obtener el HTML
URL_BASE = 'https://scrapepark.org/courses/spanish'
pedido_obtenido = requests.get(URL_BASE)
html_obtenido = pedido_obtenido.text

# 2. "Parsear" ese HTML
soup = BeautifulSoup(html_obtenido, "html.parser")

telefono = soup.find_all(string=re.compile("\d+-\d+-\d+"))
print(telefono)

# Moverse por el arbol con padres e hijos

copyrights = soup.find_all(string=re.compile("©"))
print(copyrights[0])

primer_copyright = copyrights[0]
print(primer_copyright.parent)

# # Otro ejemplo con elementos al mismo nivel
menu = soup.find(string=re.compile("MENÚ"))
# menu.parent
print(menu.parent.find_next_siblings())

strings_a_buscar = ["MENÚ", "©", "carpincho", "Patineta"]

for string in strings_a_buscar:
  try:
    resultado = soup.find(string=re.compile(string))
    print(resultado.text)
  except AttributeError:
    print(f"El string '{string}' no fue encontrado")

# **Almacenamiento de los datos**
productos.insert(0, "productos")
precios.insert(0, "precios")
datos = dict(zip(productos, precios))

import csv

with open('datos.csv','w') as f:
    w = csv.writer(f)
    w.writerows(datos.items())

# 1. Las patinetas que cuesten menos de $68
# Para este ejercicio, asumimos que ya hemos almacenado los nombres y precios de las patinetas en las listas productos y precios. Necesitamos filtrar las patinetas cuyo precio sea menor a $68.

# Eliminar encabezados si están presentes
if 'productos' in productos:
    productos.remove('productos')
if 'precios' in precios:
    precios.remove('precios')

# Convertir los precios a float y filtrar los productos con precios menores a $68
patinetas_menores_68 = {producto: float(precio) for producto, precio in zip(productos, precios) if float(precio) < 68}

# Imprimir las patinetas que cumplen con la condición
print("Patinetas que cuestan menos de $68:")
for producto, precio in patinetas_menores_68.items():
    print(f"Producto: {producto}, Precio: ${precio}")

# 2. Las patinetas que en su nombre tengan un número mayor a 3
# Este ejercicio implica verificar si el nombre de cada patineta contiene un número mayor a 3. Utilizaremos expresiones regulares para esto.


import re

# Filtrar patinetas cuyo nombre contiene un número mayor a 3
patinetas_con_numero_mayor_3 = {producto: precio for producto, precio in zip(productos, precios) if re.search(r'\b[4-9]\b', producto)}

# Imprimir las patinetas que cumplen con la condición
print("\nPatinetas cuyo nombre tiene un número mayor a 3:")
for producto, precio in patinetas_con_numero_mayor_3.items():
    print(f"Producto: {producto}, Precio: ${precio}")

# 3. Traer cualquier texto de la página que tenga la palabra "descuento" u "oferta"
# Aquí utilizaremos BeautifulSoup para buscar todas las instancias de texto que contengan las palabras "descuento" o "oferta".


# Obtener el contenido HTML de la página
URL_BASE = 'https://scrapepark.org/courses/spanish'
response = requests.get(URL_BASE)
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")

# Buscar todos los textos que contienen "descuento" u "oferta"
descuentos_ofertas = soup.find_all(string=re.compile(r"descuento|oferta", re.IGNORECASE))

# Imprimir los textos encontrados
print("\nTextos que contienen 'descuento' u 'oferta':")
for texto in descuentos_ofertas:
    print(texto.strip())

# 4. Generar un archivo .csv con dos columnas: Nombre del cliente y su testimonio
# Asumiendo que los testimonios de los clientes y sus nombres están en etiquetas específicas dentro del HTML (por ejemplo, nombres en <h4> y testimonios en <p> con una clase específica), el código podría ser algo como esto:
#

# Obtener el contenido HTML de la página (ya obtenido previamente)
# soup ya está definido

# Encontrar todos los elementos de nombre de cliente y testimonios
nombres = soup.find_all('h5', class_='customer-name')
testimonios = soup.find_all('p', class_='customer-comment')

# Crear listas para almacenar nombres y testimonios
lista_nombres = [nombre.get_text(strip=True) for nombre in nombres]
lista_testimonios = [testimonio.get_text(strip=True) for testimonio in testimonios]

# Escribir los datos en un archivo CSV
with open('testimonios_clientes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['customer-name', 'customer-client'])  # Escribir encabezados
    writer.writerows(zip(lista_nombres, lista_testimonios))  # Escribir datos

print("\nArchivo 'testimonios_clientes.csv' generado con éxito.")

