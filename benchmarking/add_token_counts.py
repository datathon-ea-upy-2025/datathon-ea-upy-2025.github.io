#!/usr/bin/env python3
import csv
import sys
import os
from google import genai
from google.genai.types import HttpOptions

# Configurar variables de entorno
os.environ['GOOGLE_CLOUD_PROJECT'] = 'covalto-ai-services-dev'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'global'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

def count_tokens(text: str, client) -> int:
    """
    Cuenta los tokens de un texto usando Google Genai API
    """
    if not text or text.strip() == '':
        return 0
    
    try:
        response = client.models.count_tokens(
            model="gemini-2.5-flash",
            contents=text,
        )
        return response.total_tokens
    except Exception as e:
        print(f"Error contando tokens: {str(e)}")
        return 0

def add_token_counts_to_csv(input_csv: str, output_csv: str):
    """
    Agrega columnas de token count al CSV existente
    """
    try:
        # Inicializar cliente de Google Genai
        client = genai.Client(http_options=HttpOptions(api_version="v1"))
        
        results = []
        
        # Leer CSV existente
        with open(input_csv, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            total_rows = 0
            for row in csv_reader:
                total_rows += 1
            
            # Reiniciar el archivo para procesar
            file.seek(0)
            csv_reader = csv.DictReader(file)
            
            for i, row in enumerate(csv_reader, 1):
                print(f"Procesando fila {i}/{total_rows}...")
                
                original_text = row.get('original_text', '')
                processed_text = row.get('processed_text', '')
                
                # Contar tokens para texto original
                original_token_count = count_tokens(original_text, client)
                
                # Contar tokens para texto procesado (solo si no hay error)
                error_value = row.get('error', '').strip()
                if not error_value and processed_text:
                    processed_token_count = count_tokens(processed_text, client)
                else:
                    processed_token_count = 0
                
                # Agregar las nuevas columnas
                row['original_token_count'] = original_token_count
                row['processed_token_count'] = processed_token_count
                
                results.append(row)
        
        # Guardar CSV con las nuevas columnas
        if results:
            fieldnames = ['row_number', 'original_text', 'processed_text', 'error', 
                         'original_token_count', 'processed_token_count']
            
            with open(output_csv, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
        
        print(f"\nProcesamiento completado. CSV con token counts guardado en: {output_csv}")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {input_csv}")
        sys.exit(1)
    except Exception as e:
        print(f"Error general: {str(e)}")
        sys.exit(1)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Agrega columnas de token count al CSV')
    parser.add_argument('input_csv', help='Archivo CSV de entrada', nargs='?', default='output.csv')
    parser.add_argument('-o', '--output', default='output_with_tokens.csv', help='Archivo CSV de salida')
    
    args = parser.parse_args()
    
    add_token_counts_to_csv(args.input_csv, args.output)

if __name__ == '__main__':
    main()