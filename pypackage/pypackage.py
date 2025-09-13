import subprocess
from typing import List, Dict


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
            raise RuntimeError(
                f"Error executing 'pip freeze': {e.stderr}") from e

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

        The package specification should be in the format
        'package_name==version'
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

    def uninstall_package(self, package_name: str) -> bool:
        """
        Uninstalls a Python package using pip uninstall.

        Args:
            package_name: Name of the package to uninstall

        Returns:
            bool: True if uninstallation succeeded, False if failed
        """
        try:
            result = subprocess.run(
                ['pip', 'uninstall', package_name, '-y'],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Successfully uninstalled: {package_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to uninstall {package_name}: {e.stderr}")
            return False

    def update_package(self, package_name: str) -> bool:
        """
        Updates a package to the latest version using pip.

        Args:
            package_name: Name of the package to update

        Returns:
            True if updated successfully, False otherwise
        """
        try:
            result = subprocess.run(
                ['pip', 'install', '--upgrade', package_name],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Updated: {package_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to update {package_name}: {e.stderr}")
            return False

    def full_update_packages(self) -> bool:
        """
        Updates all installed packages to the latest versions.

        Returns:
            True if all packages updated successfully, False otherwise
        """
        try:
            packages = self.get_installed_packages()
            all_success = True

            for package in packages:
                package_name = package['name']
                if not self.update_package(package_name):
                    all_success = False

            if all_success:
                print("All packages updated successfully")
            else:
                print("Some packages failed to update")

            return all_success

        except Exception as e:
            print(f"Error updating packages: {e}")
            return False








