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
            'scikit-learn': '0.22.0'
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

   