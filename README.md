# Prueba Técnica AUTOScraping

Prueba tecnica solicitada por la empresa AUTOScraping para el puesto python developer.

## Descripción

El objetivo es realizar un crawler de la pagina https://www.hiperlibertad.com.ar. El mismo debe extraer todos los productos disponibles, clasificandolos por sucursal para luego almacenarlos en un archivo csv.

## Requisitos Previos

Para el desarrollo del desafio se usara Python 3.10.

## Configuración del Entorno

Como entorno de desarrollo usaremos un entorno virtual creado por python con el comando, en mi caso opte por llamar al entorno `.venv` pero esto puede cambiarse a gusto del desarrollador.

```bash
python -m venv .venv
```

Una vez creado el entorno, lo activamos y procedemos a instalar los requirements con el comando dependiendo del entorno en el que nos encontremos.

Para produccion:

```bash
pip install -r requirements/base.txt
```

Para desarrollo local (Agrega librerias de jupyther y pandas para analisis):

```bash
pip install -r requirements/local.txt
```

## Uso

Para la ejecucion del proyecto se creo un archivo main.py desde el cual se controla todo el proyecto, el mismo cuenta con 3 argumentos opcionales `--storeName`, `--storeIndex`, `--input`.

 - --storeName: Se usa para elegir la sucursal por nombre, puede ser el nombre completo o solamente una parte, en caso de usar solo la provincia se realizara el scraping para todas las sucursales de esa provincia.
 - --storeIndex: Se usa para elegir la sucursar por numero de indice segun aparecen en la pagina, empieza en 0.
 - --input: Muestra un menu con una lista de opciones, para que el usualio elija la sucursar por el numero indicado en pantalla

En caso de querer ejecutar el crawler para todas las sucursales se ejecuta con 

```bash
python main.py
```

O con los distintos argumentos

```bash
python main.py --storeName "Hipermercado Jacinto Rios"
```

```bash
python main.py --storeName "CÓRDOBA"
```

```bash
python main.py --storeIndex 0
```

```bash
python main.py --input
```

## Estructura del Proyecto

El proyecto esta pensado para scrapear todos los productos de las distintas sucursales (o todas). Todo el scraping se basa en la clase Crawler, la cual empieza por ir buscando las distintas sucursales, recorriendo cada categoria y extrayendo la informacion relevante de cada producto.

Para hacer las requests se armo una clase enfocada a hacer peticiones con reintentos, teniendo en cuenta posibles errores de conexion. Decidi juntar todas las keys que usa la api en una misma clase para poder acceder a ellas de forma mas facil, y tambien por si llegan a cambiar en un futuro que sea facil el mantenimiento. Para las urls segui la misma metodologia pudiendo agrupar tambien algunos metodos que armen los distintos metodos.

Los campos que se relevan de cada producto son:

- Id: identificacion del producto
- ProductReference: es otro id que me parecio relevante guardar
- Name: nombre del producto
- CompleteName: nombre completo del producto, suele ser igual al nombre
- Brand: marca del producto
- BrandId: id de la marca del producto
- Categories: categorias en las que se puede encontrar el producto
- Link: link al producto
- Description: descripcion del producto
- IsKit: indica si el producto es un kit de varios subproductos
- Images: link a las imagenes
- SellerId: id de la tienda, es el mismo para todos por lo que vi
- SellerName: tienda que lo vende, es el mismo para todos por lo que vi
- Price: precio actual
- ListPrice: precio de lista
- PriceWithoutDiscount: precio sin descuentos que hayan en el momento
- PriceValidUntil: fecha hasta la cual el descuento es valido
- Stock: cantidad de unidades disponibles para comprar
- PaymentOptions: metodos de pago, se agrupan por medio de pago, con todas las opciones que ofrecen de cuotas y su respectivo recargo
- CreatedAt: fecha en la que se ejecuto el scraping
- Timestamp: timestamp del momento en el que se creo el payload

## Limitaciones y Consideraciones

Para tener en cuenta, los requerimientos locales los arme debido que use un jupyther notebook para hacer un analisis de los csvs que se creaban con el crawler, para poder ver que no me faltara limpiar algun dato, o hay algun problema con algun campo. Con hacer una instalacion unicamente de los requerimientos base alcanza para ejecutar el proyecto.

Desisti de usar docker como entorno de desarrollo debido a que no use librerias muy complejas que requirieran de una configuracion adicional, como pueden ser selenium o playwright

## Información Adicional

Perfil de LinkedIn [Damian Lorenzo](https://www.linkedin.com/in/damian-lorenzo/)
