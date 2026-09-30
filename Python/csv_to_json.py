#!/usr/bin/env python3
"""
CSV to JSON Schema Processor
Converts CSV files and JSON schema into a structured JSON spec matching Pydantic models.
"""

import pandas as pd
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def convert_boolean(value: Any) -> Optional[bool]:
    """Convert string boolean values to actual booleans."""
    if pd.isna(value):
        return None
    
    if isinstance(value, str):
        lower = value.lower().strip()
        if lower in ['y', 'yes', 'true']:
            return True
        elif lower in ['n', 'no', 'false']:
            return False
        elif lower in ['n/a', '']:
            return None
        elif lower.startswith('y ('):  # Handle "y (see comment)" cases
            return True
        elif lower.startswith('n ('):
            return False
    
    return value


def process_csv_files(schema_file: str, required_fields_file: str) -> Dict[str, Any]:
    """
    Process CSV files and optional JSON schema file to create structured JSON spec.
    
    Args:
        schema_file: Path to the schema CSV file
        required_fields_file: Path to the required fields CSV file  
        json_file: Optional path to JSON schema file for descriptions
        
    Returns:
        Dictionary containing the processed schema structure
    """
    
    # Load CSV files
    print(f"Loading required fields from: {required_fields_file}")
    required_df = pd.read_csv(required_fields_file)
    
    print(f"Loading schema from: {schema_file}")
    schema_df = pd.read_csv(schema_file)
    
    print(f"Required fields CSV shape: {required_df.shape}")
    print(f"Schema CSV shape: {schema_df.shape}")
    
    
    # Process required fields CSV as PRIMARY source
    data_map = {}
    
    for _, row in required_df.iterrows():
        data_key = row.get('key')
        level = row.get('level', 'root')
        if level not in data_map:
            data_map[level] = {}

        if pd.notna(data_key):
            data_map[level][data_key] = {
                'data_key': data_key,
                'data_type': row.get('data_type') if pd.notna(row.get('data_type')) else None,
                'db_nullable': None,  # Will be populated from schema file if available
                're_request_if_missing': convert_boolean(row.get('re-request_if_missing')),
                'required_for_abstraction': convert_boolean(row.get('required_for_abstraction')),
                'required_for_ingestion': convert_boolean(row.get('required_for_ingestion')),
                'required_comment': row.get('comment') if pd.notna(row.get('comment')) else None,
                'examples': [row.get('examples')] if pd.notna(row.get('examples')) else None,
                # Initialize other fields that may come from schema
                'json_comment': None,
                'schema_comment': None,
                'ccdm_destination': None,
                'ccdm_import_details': None
            }
    
    # LEFT OUTER JOIN with schema CSV - only add data where keys match
    for _, row in schema_df.iterrows():
        data_key = row.get('key')
        data_level = row.get('level')
        
        # Only update if the key exists in our required fields data
        if pd.notna(data_key) and data_key in data_map[data_level]:
            existing = data_map[data_level][data_key]
            
            # Update with schema data
            data_map[data_level][data_key].update({
                'data_type': row.get('data_type') if pd.notna(row.get('data_type')) else existing['data_type'],
                'schema_comment': row.get('comment') if pd.notna(row.get('comment')) else None,
                'ccdm_destination': row.get('ccdm_destination') if pd.notna(row.get('ccdm_destination')) else None,
                'ccdm_import_details': row.get('ccdm_import_details') if pd.notna(row.get('ccdm_import_details')) else None,
                # Keep examples from required file if schema doesn't have any
                'examples': [row.get('examples')] if pd.notna(row.get('examples')) else existing['examples']
            })
        
    # Create final schema structure
    schema = {
        'groups': [
            {
                'group_name': group_name,
                'data_definitions': [v for k,v in definitions.items()]
            }
            for group_name, definitions in data_map.items()
        ]
    }
    
    return schema


def main():
    """Main function to process files and generate JSON output."""
    
    # File paths - modify these as needed
    schema_file = "/Users/matthew/Downloads/new_abstraction_schema.csv"
    required_fields_file = "/Users/matthew/Downloads/abstraction_schema_required_fields.csv"
    output_file = "/Users/matthew/Downloads/schema_definition.json"
    
    # Check if files exist
    if not Path(required_fields_file).exists():
        print(f"Error: Required fields file not found: {required_fields_file}")
        sys.exit(1)
    
    if not Path(schema_file).exists():
        print(f"Error: Schema file not found: {schema_file}")
        sys.exit(1)
    
    try:
        # Process the files
        result = process_csv_files(schema_file, required_fields_file)
        
        # Calculate summary
        total_fields = sum(len(group['data_definitions']) for group in result['groups'])
        num_groups = len(result['groups'])
        
        print("\nProcessing complete!")
        print(f"Groups: {num_groups}")
        print(f"Total Fields: {total_fields}")
        
        # Write output file
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=4)
        
        print(f"Output written to: {output_file}")
        
        # Display group summary
        print("\nGroup Summary:")
        for group in result['groups']:
            print(f"  {group['group_name']}: {len(group['data_definitions'])} fields")
    
    except Exception as e:
        print(f"Error processing files: {e}")
        raise e


if __name__ == "__main__":
    main()