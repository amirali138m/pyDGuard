import subprocess
from typing import List, Dict, Any

class PackageManage:
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
    
    
    
    def get_installed_packages(self) -> List[Dict[str, str]]:
        """
        Returns the list of installed packages from the output of pip freeze
        """
        pip_freeze_output = self.get_pip_freeze()
    
        packages = []
        for line in pip_freeze_output:
            if line and '==' in line:
                name, version = line.split('==', 1)  # split only on first '=='
                packages.append({
                    'name': name.strip(),
                    'version': version.strip()
                })
    
        return packages
    

    def install_package(self, package_spec: str) -> bool:
        """
        Installs a Python package with a specific version using pip.
    
        The package specification should be in the format 'package_name==version'
        Example: 'requests==2.25.1'
    
        Args:
            package_spec: Package name and version in 'name==version' format
        
        Returns:
            bool: True if installation succeeded, False if failed
        """
        try:
            result = subprocess.run(
                ['pip', 'install', package_spec],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Successfully installed: {package_spec}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package_spec}: {e.stderr}")
            return False


