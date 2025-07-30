#!/usr/bin/env python3
import csv
import sys
import re

def txt_to_csv(txt_file: str, csv_file: str):
    """
    Convierte el archivo output.txt del script a formato CSV
    """
    results = []
    
    try:
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Dividir por las secciones que empiezan con "=== Fila X ==="
        sections = re.split(r'=== Fila (\d+) ===\n', content)
        
        # El primer elemento está vacío, luego vienen pares (número, contenido)
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                row_number = sections[i]
                section_content = sections[i + 1]
                
                # Extraer texto original
                original_match = re.search(r'Texto original: (.*?)\n', section_content)
                original_text = original_match.group(1) if original_match else ""
                
                # Verificar si hay error
                error_match = re.search(r'Error: (.*?)\n', section_content)
                if error_match:
                    error = error_match.group(1)
                    processed_text = None
                else:
                    error = None
                    # Extraer texto procesado
                    processed_match = re.search(r'Texto procesado:\n(.*?)(?=\n-{50}|\Z)', section_content, re.DOTALL)
                    processed_text = processed_match.group(1).strip() if processed_match else ""
                
                results.append({
                    'row_number': int(row_number),
                    'original_text': original_text,
                    'processed_text': processed_text,
                    'error': error
                })
        
        # Guardar como CSV
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=['row_number', 'original_text', 'processed_text', 'error'])
                writer.writeheader()
                writer.writerows(results)
        
        print(f"Conversión completada: {len(results)} filas convertidas a {csv_file}")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {txt_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Convierte output.txt a CSV')
    parser.add_argument('txt_file', help='Archivo TXT de entrada', nargs='?', default='output.txt')
    parser.add_argument('-o', '--output', default='output.csv', help='Archivo CSV de salida')
    
    args = parser.parse_args()
    
    txt_to_csv(args.txt_file, args.output)