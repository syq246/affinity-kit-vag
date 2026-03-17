import logging
import os
from pathlib import Path
from typing import Optional
import win32com.client

class AffinityPhotoClient:
    """Client interface for interacting with Affinity Photo for Windows."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the AffinityPhotoClient.
        
        Args:
            config_path (Optional[Path]): Path to the configuration file.
        """
        self.config_path = config_path
        self.app = None
        self.is_connected = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect(self) -> bool:
        """Connects to the Affinity Photo application via COM interface.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.logger.info("Attempting to connect to Affinity Photo...")
            self.app = win32com.client.Dispatch("AffinityPhoto.Application")
            self.is_connected = True
            self.logger.info("Successfully connected to Affinity Photo.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to Affinity Photo: {e}")
            return False
    
    def disconnect(self):
        """Disconnects from the Affinity Photo application."""
        if self.is_connected:
            self.logger.info("Disconnecting from Affinity Photo...")
            self.app = None
            self.is_connected = False
            self.logger.info("Successfully disconnected from Affinity Photo.")
        else:
            self.logger.warning("Already disconnected from Affinity Photo.")
    
    def get_version(self) -> str:
        """Retrieves the version of the Affinity Photo application.

        Returns:
            str: Version string of the Affinity Photo application.

        Raises:
            RuntimeError: If not connected to the application.
        """
        if not self.is_connected:
            raise RuntimeError("Not connected to Affinity Photo.")
        
        try:
            version = self.app.Version
            self.logger.info(f"Retrieved Affinity Photo version: {version}")
            return version
        except Exception as e:
            self.logger.error(f"Failed to retrieve version: {e}")
            raise RuntimeError("Could not retrieve version information.")
    
    def is_installed(self) -> bool:
        """Checks if Affinity Photo is installed on the system.

        Returns:
            bool: True if Affinity Photo is installed, False otherwise.
        """
        try:
            installed = win32com.client.Dispatch("AffinityPhoto.Application")
            self.logger.info("Affinity Photo is installed.")
            return True
        except Exception:
            self.logger.warning("Affinity Photo is not installed.")
            return False
