from anthropic import Anthropic
from typing import Dict, List
from ..config import config
import json
from ..exploits.exploit_db import ExploitDBSearcher, GithubExploitSearcher, GTFOBinsLookup
import re

class PrivescAnalyzer:
    # Uses selected LLM to analyze output and suggest vectors

    def __init__(self):
        if not config.anthropic_api_key:
            raise ValueError("Anrthopic API key not set")

        self.client = Anthropic(api_key=config.anthropic_api_key)
        self.system_prompt = self._build_system_prompt()

        self.exploitdb = ExploitDBSearcher()
        self.github = GithubExploitSearcher(github_token)
        self.gtfobins = GTFOBinsLookup()

    def analyze_with_exploits(self, system_info: Dict[str, str], enum_output: str) -> str:

        base_analysis = self.analyze(system_info, enum_output)

        cves = self._extract_cves(base_analysis)

        enriched_findings = base_analysis + "\n\n## Exploit Resources\n\n"

        for cve in cves[:5]:
            enriched_findings += f"\n### {cve}\n\n"

            edb_results = self.exploitdb.search_by_cve(cve)
            if edb_results:
                enriched_findings += "**ExploitDB:**\n"
                for exploit in edb_results[:3]:
                    enriched_findings += f"- [{exploit.title}]({exploit.url})\n"
            
            # Search GitHub
            gh_results = self.github.search_by_cve(cve)
            if gh_results:
                enriched_findings += "\n**GitHub PoCs:**\n"
                for repo in gh_results[:3]:
                    enriched_findings += f"- [{repo['name']}]({repo['url']}) - ⭐ {repo['stars']}\n"
        
        return enriched_findings

    def check_suid_exploits(self, suid_output: str) -> str:
        """Check SUID binaries against GTFOBins"""
        
        # Parse SUID binaries from output
        suid_binaries = suid_output.strip().split('\n')
        
        # Check against GTFOBins
        gtfo_results = self.gtfobins.check_suid_list(suid_binaries)
        
        if not gtfo_results:
            return "No GTFOBins entries found for discovered SUID binaries."
        
        report = "## GTFOBins SUID Exploitation Opportunities\n\n"
        
        for binary, info in gtfo_results.items():
            report += f"### {binary}\n"
            report += f"- **GTFOBins URL:** {info['url']}\n"
            report += f"- **Techniques:** {', '.join(info['techniques'])}\n\n"
        
        return report
    
    def _extract_cves(self, text: str) -> List[str]:
        """Extract CVE identifiers from text"""
        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        return list(set(re.findall(cve_pattern, text, re.IGNORECASE)))

    def _build_system_prompt(self) -> str:
        return """You are an expert privilege escalation analyst for penetration testing.

Your role is to analyze Linux enumeration output and identify exploitable privilege escalation vectors.

For each finding, provide:
1. **Severity**: Critical/High/Medium/Low
2. **Technique**: Specific privesc method (SUID abuse, sudo misconfig, etc.)
3. **Explanation**: Why this is exploitable
4. **Exploitation steps**: Exact commands to attempt
5. **Resources**: Links to GTFOBins, exploit-db, or github PoCs

Prioritize findings by likelihood of success and ease of exploitation
Be concise but specific. Focus on actionable intelligence."""

    def analyze(self, system_info: Dict[str, str], enum_output: str) -> str:

        user_prompt = f"""
System Information:
- OS: {system_info.get('os', 'Unknown')}
- Kernel: {system_info.get('kernel', 'Unknown')}
- User: {system_info.get('user', 'Unknown')}
- Groups: {system_info.get('groups', 'Unknown')}

Enumeration Output:
{enum_output[:15000]}

Analyze this output and identify the top 5 most promising privilege escalation vectors. Format your response as structured findings with clear exploitation steps.
"""

        try:
            message = self.client.messages.create(
                    model=config.model,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    system=self.system_prompt,
                    messages =[
                        {"role": "user", "content": user_prompt}
                        ]
                    )

            return message.content[0].text

        except Exception as e:
            return f"Error during LLM analysis: {str(e)}"

    def quick_wins_check(self, custom_enum: Dict[str, str]) -> str:
        # Check for quick win pricesc opportunities

        prompt = f"""
Quick analysis for immediate prives opportunities:

Sudo rights:
{custom_enum.get('sudo_rights', 'None found')}

SUID Binaries:
{custom_enum.get('suid,files' 'None found')[:1000]}

Writable /etc files:
{custom_enum.get('writable_etc', 'None found')}

Capabilites:
{custom_enum.get('capabilities', 'None found')}

Identify any immediate privilege escalation opportunities from these findings.
Be brief - only report if there's a clear exploitation path.
"""

        try:
            message = self.client.messages.create(
                    model=config.model,
                    max_tokens=1500,
                    temperature=0.1,
                    system="You are a privilege escalation expert. Identify quick wins only.",
                    messages=[{"role": "user", "content": prompt}]
                    )

            return message.content[0].text

        except Exception as e:
            return f"Error: {str(e)}"
