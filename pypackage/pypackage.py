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


