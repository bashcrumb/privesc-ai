# privesc_ai/enumeration/downloader.py
import requests
from pathlib import Path

class ScriptDownloader:
    """Download enumeration scripts if not present"""
    
    LINPEAS_URL = "https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh"
    
    def __init__(self, scripts_dir: str = "./scripts"):
        self.scripts_dir = Path(scripts_dir)
        self.scripts_dir.mkdir(exist_ok=True)
    
    def download_linpeas(self) -> Path:
        """Download LinPEAS if not present"""
        linpeas_path = self.scripts_dir / "linpeas.sh"
        
        if linpeas_path.exists():
            return linpeas_path
        
        print(f"Downloading LinPEAS from {self.LINPEAS_URL}...")
        
        try:
            response = requests.get(self.LINPEAS_URL, timeout=30)
            response.raise_for_status()
            
            linpeas_path.write_bytes(response.content)
            linpeas_path.chmod(0o755)  # Make executable
            
            print(f"✓ LinPEAS downloaded to {linpeas_path}")
            return linpeas_path
            
        except Exception as e:
            raise Exception(f"Failed to download LinPEAS: {str(e)}")
