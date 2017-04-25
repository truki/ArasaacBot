# API Documentation

En cuanto a los datos para acceder a la API son:

* callback = json // obligatorio
* language = ES // Idioma de búsqueda. Otros idiomas ES, EN, FR, CA, IT, DE
* word = cadena de caracteres a buscar // escribimos la palabra exacta o la cadena de caracteres
* catalog = colorpictos // bwpictos para pictogramas en blanco y negro
* nresults = 10 // Numero de resultados
* ThumbnailSize = 150 // | Tamaño de la miniatura
* TXTlocate = 1 //Tipo de búsqueda del texto 1-Empieza por 2-Contiene 3-Termina por 4-Exacta
* KEY = xxxxxxxx  // clave de API para vuestro uso exclusivo e instransferible (no se la podéis proporcionar a nadie)

VARIABLES OPCIONALES:

tipo_palabra = 2 //
tipos:
* 1- Nombres propios,
* 2-Nombres Comunes,
* 3- Verbos,
* 4- Descriptivos,
* 5- Contenido Social
* 6-Miscelánea

Ejemplo:

http://arasaac.org/api/index.php?callback=json&language=ES&word=botella&catalog=colorpictos&nresults=0&thumbnailsize=100&TXTlocate=1&KEY=xxxxxxxx
