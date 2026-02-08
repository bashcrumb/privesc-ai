import subprocess
from typing import Dict, Optional
from pathlib import Path
from .downloader import ScriptDownloader

class EnumerationRunner:
    # Runs prives enum tools

    def __init__(self):
        self.results = {}
        self.downloader = ScriptDownloader()
        self.linpeas_path = None

    def run_linpeas(self, output_file: Optional[str] = None) -> str:
        # Run linpeas and return output
        try:
            
            if not self.linpeas_path:
                self.linpeas_path = self.downloader.download_linpeas()

            result = subprocess.run(
                    ['bash', 'linpeas.sh'],
                    capture_output = True,
                    text=True,
                    timeout=300
                    )

            output = result.stdout

            if output_file:
                Path(output_file).write_text(output)

            self.results['linpeas'] = output
            return output

        except subprocess.TimeoutExpired:
            return "LinPEAS timed out after 5 mins"
        except FileNotFoundError:
            return "LinPEAS not found."
        except Exception as e:
            return f"Error running LinPEAS: {str(e)}"

    def run_custom_enum(self) -> Dict[str, str]:
        # Run basic enum commands
        commands = {
                'sudo_rights': 'sudo -l',
                'suid_files': 'find / -perm -4000 -type f 2>/dev/null',
                'writable_etc': 'find /etc -writeable -type f 2>/dev/null',
                'cron_jobs': 'cat /etc/crontab',
                'capabilities': 'getcap -r / 2>/dev/null',
                }

        results = {}
        for name, cmd in commands.items():
            try:
                result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                        )
                results[name] = result.stdout
            except Exception as e:
                results[name] = f"Error: {str(e)}"

        return results

    def get_system_info(self) -> Dict[str, str]:
        # Get basic sys info
        info_commands = {
                'os': 'cat /etc/os-release',
                'kernel': 'uname -r',
                'user': 'whoami',
                'groups': 'groups',
                'hostname': 'hostname',
                }

        info = {}
        for key, cmd in info_commands.items():
            try:
                result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=5
                        )
                info[key] = result.stdout.strip()
            except:
                info[key] = "Unknown"

        return info
