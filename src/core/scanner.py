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

            # Check for known deprecated packages
            if dep_name in deprecated_packages:
                min_supported_version = deprecated_packages[dep_name]
                
                # Simple version comparison
                try:
                    current_parts = list(map(int, current_version.split('.')))
                    min_parts = list(map(int, min_supported_version.split('.')))
                    
                    if current_parts < min_parts:
                        dep_info['is_deprecated'] = True
                        dep_info['deprecation_reason'] = f'Version {current_version} is deprecated. Minimum supported version: {min_supported_version}'
                        
                except ValueError:
                    # If version cannot be parsed
                    dep_info['has_warnings'] = True
                    dep_info['warnings'].append(f'Version {current_version} cannot be parsed')

            # Check for alpha/beta/pre-release versions
            if any(keyword in current_version.lower() for keyword in ['alpha', 'beta', 'rc', 'dev', 'pre']):
                dep_info['has_warnings'] = True
                dep_info['warnings'].append('This is a development/pre-release version')

            # Check for packages with "deprecated" in name
            if 'deprecated' in dep_name or 'legacy' in dep_name:
                dep_info['is_deprecated'] = True
                dep_info['deprecation_reason'] = 'Package name indicates deprecated status'

            results.append(dep_info)
        
        return results
