"""
Este módulo calcula el costo total de las ventas basándose en un catálogo de precios
y un conjunto de registros de ventas. Carga los datos de archivos JSON y genera un informe
con el costo total de las ventas y posibles errores.
"""

import json
import sys
import time


def load_json_file(filename):
    """Carga un archivo JSON y maneja errores en caso de formato inválido."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError, IOError) as error:
        print(f"Error al cargar el archivo {filename}: {error}")
        return None


def build_price_catalogue(product_list):
    """Convierte la lista de productos en un diccionario {nombre: precio}."""
    price_catalogue = {}
    for product in product_list:
        title = product.get("title")
        price = product.get("price")

        if title and isinstance(price, (int, float)):
            price_catalogue[title] = price
        else:
            print(f"Advertencia: Producto con datos inválidos {product}")
    return price_catalogue


def compute_total_sales(price_catalogue, sales_records):
    """Calcula el costo total de las ventas para cada archivo."""
    results = {}
    for filename, sales_record in sales_records.items():
        total_cost = 0.0
        errors = []

        for sale in sales_record:
            product = sale.get("Product")
            quantity = sale.get("Quantity")

            if product not in price_catalogue:
                errors.append(f"Producto no encontrado en catálogo: {product}")
                continue

            if not isinstance(quantity, (int, float)):
                errors.append(
                    f"Cantidad inválida para {product}: {quantity}"
                )
                continue

            total_cost += price_catalogue[product] * quantity

        results[filename] = (total_cost, errors)
    return results


def main():
    """Función principal que ejecuta el programa."""
    if len(sys.argv) < 3:
        print("Uso: python compute_sales.py priceCatalogue.json "
              "salesRecord1.json [salesRecord2.json ...]")
        sys.exit(1)

    price_file = sys.argv[1]
    sales_files = sys.argv[2:]
    start_time = time.time()

    raw_catalogue = load_json_file(price_file)
    if raw_catalogue is None:
        print("No se pudo cargar el archivo de catálogo de precios.")
        sys.exit(1)

    price_catalogue = build_price_catalogue(raw_catalogue)
    sales_records = {}
    for sales_file in sales_files:
        sales_data = load_json_file(sales_file)
        if sales_data is not None:
            sales_records[sales_file] = sales_data

    if not sales_records:
        print("No se pudo cargar ningún archivo de ventas.")
        sys.exit(1)

    results = compute_total_sales(price_catalogue, sales_records)
    execution_time = time.time() - start_time

    result_text = f"Tiempo de ejecución: {execution_time:.4f} segundos\n"
    for filename, (total_sales, errors) in results.items():
        result_text += (
            f"\nArchivo: {filename}\n"
            f"Costo total de las ventas: {total_sales:.2f} unidades monetarias\n"
        )
        if errors:
            result_text += "Errores detectados:\n" + "\n".join(errors) + "\n"

    print(result_text)

    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(result_text)


if __name__ == "__main__":
    main()
    