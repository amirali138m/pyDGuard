import subprocess
from typing import List, Dict, Any


class DependencyScanner:
    """
    Python dependency scanner that analyzes pip freeze output.
    """

    def get_pip_freeze(self) -> List[str]:
        """
        Execute pip freeze command and get output.
        """
        try:
            result = subprocess.run(
                ['pip', 'freeze'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error executing 'pip freeze': {e.stderr}") from e

    def parse_pip_freeze(self, freeze_output: List[str]) -> List[Dict[str, str]]:
        """
        Parse pip freeze output into a list of dictionaries.
        """
        dependencies = []
        for line in freeze_output:
            line = line.strip()
            if line and '==' in line:
                parts = line.split('==', 1)
                if len(parts) == 2:
                    name, version = parts
                    dependencies.append({
                        'name': name.strip(),
                        'version': version.strip()
                    })
        return dependencies

    def check_deprecation_status(self, dependencies: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Check deprecation status of dependencies.
        """
        # List of known deprecated packages with minimum supported versions
        deprecated_packages = {
            'requests': '2.0.0',
            'django': '3.0.0',
            'flask': '2.0.0',
            'numpy': '1.20.0',
            'tensorflow': '2.0.0',
            'pandas': '1.0.0',
            'matplotlib': '3.0.0',
            'scikit-learn': '0.22.0',
            'fastapi': '0.68.0',
            'pytorch': '1.8.0',
            'scipy': '1.6.0',
            'pillow': '8.0.0',
            'sqlalchemy': '1.4.0',
            'beautifulsoup4': '4.9.0',
            'selenium': '4.0.0',
            'pytest': '6.0.0',
            'jupyter': '1.0.0',
            'notebook': '6.0.0',
            'ipython': '7.0.0',
            'aiohttp': '3.7.0',
            'tornado': '6.1.0',
            'celery': '5.0.0',
            'redis': '3.5.0',
            'psycopg2': '2.8.0',
            'pymongo': '3.11.0',
            'sqlite3': '3.35.0',
            'pygame': '2.0.0',
            'opencv-python': '4.5.0',
            'tqdm': '4.60.0',
            'loguru': '0.5.0',
            'rich': '9.0.0',
            'click': '8.0.0',
            'typer': '0.3.0',
            'pydantic': '1.8.0',
            'marshmallow': '3.12.0',
            'gunicorn': '20.1.0',
            'uvicorn': '0.13.0',
            'django-rest-framework': '3.12.0',
            'flask-restful': '0.3.9',
            'graphene': '3.0.0',
            'plotly': '5.0.0',
            'seaborn': '0.11.0',
            'bokeh': '2.4.0',
            'streamlit': '1.0.0',
            'dash': '2.0.0',
            'airflow': '2.2.0',
            'prefect': '0.15.0',
            'luigi': '3.0.0',
            'mlflow': '1.23.0',
            'transformers': '4.15.0',
            'spacy': '3.2.0',
            'nltk': '3.6.0',
            'gensim': '4.1.0',
            'elasticsearch': '7.15.0',
            'kafka-python': '2.0.0',
            'boto3': '1.20.0',
            'azure-storage-blob': '12.9.0',
            'google-cloud-storage': '2.0.0',
            'twisted': '22.0.0',
            'asyncio': '3.4.0',
            'virtualenv': '20.10.0',
            'pipenv': '2022.0.0',
            'poetry': '1.2.0'
        }
        
        results = []
        for dep in dependencies:
            dep_name = dep['name'].lower()
            current_version = dep['version']
            
            dep_info = {
                'name': dep_name,
                'current_version': current_version,
                'is_deprecated': False,
                'deprecation_reason': None,
                'has_warnings': False,
                'warnings': []
            }

            if dep_name in deprecated_packages:
                min_supported_version = deprecated_packages[dep_name]
                
                try:
                    current_parts = list(map(int, current_version.split('.')))
                    min_parts = list(map(int, min_supported_version.split('.')))
                    
                    if current_parts < min_parts:
                        dep_info['is_deprecated'] = True
                        dep_info['deprecation_reason'] = f'Version {current_version} is deprecated. Minimum supported version: {min_supported_version}'
                        
                except ValueError:
                    dep_info['has_warnings'] = True
                    dep_info['warnings'].append(f'Version {current_version} cannot be parsed')

            if any(keyword in current_version.lower() for keyword in ['alpha', 'beta', 'rc', 'dev', 'pre']):
                dep_info['has_warnings'] = True
                dep_info['warnings'].append('This is a development/pre-release version')

            if 'deprecated' in dep_name or 'legacy' in dep_name:
                dep_info['is_deprecated'] = True
                dep_info['deprecation_reason'] = 'Package name indicates deprecated status'

            results.append(dep_info)
        
        return results 


if __name__ == "__main__":
    scanner = DependencyScanner()
    
    print("Starting dependency scan...")
    print("=" * 50)
    
    try:
        print("Getting pip freeze output...")
        freeze_output = scanner.get_pip_freeze() 
        print("Parsing dependencies...")
        dependencies = scanner.parse_pip_freeze(freeze_output)
        print(f"Found {len(dependencies)} dependencies")
        print()
        
        print("Checking deprecation status...")
        results = scanner.check_deprecation_status(dependencies)
        
        print("=" * 50)
        print("SCAN RESULTS:")
        print("=" * 50)
        
        deprecated_count = 0
        warning_count = 0
        
        for result in results:
            if result['is_deprecated']:
                print(f"DEPRECATED: {result['name']}=={result['current_version']}")
                print(f"   Reason: {result['deprecation_reason']}")
                deprecated_count += 1
            elif result['has_warnings']:
                print(f"WARNING: {result['name']}=={result['current_version']}")
                for warning in result['warnings']:
                    print(f"   {warning}")
                warning_count += 1
            else:
                print(f"OK: {result['name']}=={result['current_version']}")
        
        print("=" * 50)
        print("SUMMARY:")
        print(f"Total packages: {len(results)}")
        print(f"Deprecated: {deprecated_count}")
        print(f"Warnings: {warning_count}")
        print(f"Healthy: {len(results) - deprecated_count - warning_count}")
        
    except RuntimeError as e:
        print(f"Error: {e}")
        print("Make sure you have pip installed and in your PATH")
    except Exception as e:
        print(f"Unexpected error: {e}")

   