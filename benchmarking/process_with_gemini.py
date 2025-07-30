#!/usr/bin/env python3
import csv
import sys
import argparse
from typing import List, Dict
import json
import os
from google import genai
from google.genai.types import HttpOptions

# Configurar variables de entorno
os.environ['GOOGLE_CLOUD_PROJECT'] = 'covalto-ai-services-dev'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'global'
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = 'True'

def process_csv_with_gemini(csv_file: str, output_file: str, prompt_template: str = None):
    """
    Procesa un archivo CSV con una columna 'prompt_text' usando Google Gemini
    
    Args:
        csv_file: Ruta al archivo CSV de entrada
        output_file: Ruta al archivo de salida
        prompt_template: Template opcional para el prompt
    """
    
    # Prompt por defecto si no se proporciona uno
    if not prompt_template:
        prompt_template = "{prompt_text}"
    
    results = []
    
    try:
        # Inicializar cliente de Google Genai
        client = genai.Client(http_options=HttpOptions(api_version="v1"))
        
        # Leer archivo CSV
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Verificar que existe la columna prompt_text
            if 'prompt_text' not in csv_reader.fieldnames:
                raise ValueError("El archivo CSV no contiene una columna 'prompt_text'")
            
            for row_num, row in enumerate(csv_reader, 1):
                prompt_text = row.get('prompt_text', '').strip()
                
                if not prompt_text:
                    print(f"Fila {row_num}: Sin contenido en prompt_text, saltando...")
                    results.append({
                        'row_number': row_num,
                        'original_text': '',
                        'processed_text': 'Sin contenido',
                        'error': None,
                        'original_token_count': 0,
                        'processed_token_count': 0
                    })
                    continue
                
                try:
                    # Preparar el prompt
                    prompt = prompt_template.format(prompt_text=prompt_text)
                    
                    # Llamar a Gemini
                    print(f"Procesando fila {row_num}...")
                    
                    # Generar respuesta con Gemini
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    
                    processed_text = response.text
                    
                    # Contar tokens para texto original
                    original_token_response = client.models.count_tokens(
                        model="gemini-2.5-flash",
                        contents=prompt_text
                    )
                    original_token_count = original_token_response.total_tokens
                    
                    # Contar tokens para texto procesado
                    processed_token_response = client.models.count_tokens(
                        model="gemini-2.5-flash",
                        contents=processed_text
                    )
                    processed_token_count = processed_token_response.total_tokens
                    
                    results.append({
                        'row_number': row_num,
                        'original_text': prompt_text[:100] + '...' if len(prompt_text) > 100 else prompt_text,
                        'processed_text': processed_text,
                        'error': None,
                        'original_token_count': original_token_count,
                        'processed_token_count': processed_token_count
                    })
                    
                except Exception as e:
                    print(f"Error procesando fila {row_num}: {str(e)}")
                    results.append({
                        'row_number': row_num,
                        'original_text': prompt_text[:100] + '...' if len(prompt_text) > 100 else prompt_text,
                        'processed_text': None,
                        'error': str(e),
                        'original_token_count': 0,
                        'processed_token_count': 0
                    })
        
        # Guardar resultados
        save_results(results, output_file)
        print(f"\nProcesamiento completado. Resultados guardados en: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error general: {str(e)}")
        sys.exit(1)

def save_results(results: List[Dict], output_file: str):
    """Guarda los resultados en diferentes formatos según la extensión del archivo"""
    
    if output_file.endswith('.json'):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    elif output_file.endswith('.csv'):
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            if results:
                fieldnames = ['row_number', 'original_text', 'processed_text', 'error', 
                             'original_token_count', 'processed_token_count']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
    
    else:  # Formato de texto por defecto
        with open(output_file, 'w', encoding='utf-8') as f:
            for result in results:
                f.write(f"=== Fila {result['row_number']} ===\n")
                f.write(f"Texto original: {result['original_text']}\n")
                f.write(f"Tokens originales: {result['original_token_count']}\n")
                if result['error']:
                    f.write(f"Error: {result['error']}\n")
                else:
                    f.write(f"Texto procesado:\n{result['processed_text']}\n")
                    f.write(f"Tokens procesados: {result['processed_token_count']}\n")
                f.write("\n" + "-"*50 + "\n\n")

def main():
    parser = argparse.ArgumentParser(description='Procesa un archivo CSV con columna prompt_text usando Google Gemini')
    parser.add_argument('csv_file', help='Archivo CSV de entrada', nargs='?', default='conciencia ambiental.csv')
    parser.add_argument('-o', '--output', default='output_gemini.csv', help='Archivo de salida (default: output_gemini.csv)')
    parser.add_argument('-p', '--prompt', help='Template personalizado para el prompt (usar {prompt_text} como placeholder)')
    
    args = parser.parse_args()
    
    # Ejecutar el procesamiento
    process_csv_with_gemini(
        csv_file=args.csv_file,
        output_file=args.output,
        prompt_template=args.prompt
    )

if __name__ == '__main__':
    main()