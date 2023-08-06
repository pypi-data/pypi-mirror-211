import requests

class BCBAPIUFV:
    def consumir_endpoint(self, fecha_inicio, fecha_fin=None):
        if fecha_fin is None:
            fecha_fin = fecha_inicio

        url = f"https://www.bcb.gob.bo/librerias/charts/ufv.php?cFecIni={fecha_inicio}&cFecFin={fecha_fin}"
        
        try:
            # Realizar la petición GET
            response = requests.get(url)

            # Verificar si la petición fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener los datos de la respuesta en formato JSON
                data = response.json()
                # Imprimir la respuesta
                print(data)
            else:
                # Imprimir el código de estado en caso de una respuesta no exitosa
                print("La petición GET no fue exitosa. Código de estado:", response.status_code)

        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión u otros errores de la petición
            print("Error en la petición GET:", e)




