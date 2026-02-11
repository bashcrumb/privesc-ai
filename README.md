# AI-Assisted PrivEsc Tool

AI-Assisted privilege escalation helper for unix-like systems, designed for pentesting labs, CTF environments, and post-exploitation research.

This project explorts using LLM-based reasoning to analyze system enumeration output and suggest likely privesc paths. It is intended as a research and workflow-assistance tool, not a fully automated exploitation framework.

---

## Features

* Enumeration-aware analysis
    * Ingests common privesc findings (users, groups, sudo rules, SUID bins, services)
    * Correlates results with known escalation techniques
* AI-driven reasoning
    * Suggests possible escalation vectors based on system context
    * Provides human-readable explanations for why a vector may apply
* Workflow focused
    * Designed to complement manual enumeration
    * Useful for CTFs and lab environments (HTB, THM, etc.)
* Extensible architecture
    * New checks and reasoning paths can be added incrementally
    * Separation between data collection and analysis logic
> **Ethical use only:** This tool is intended for environments where you have authorization. Do not use it on systems you do not own or have permission to test.

---

## Building / Installation
```bash
git clone https://github.com/bashcrumb/privesc-ai.git
cd privesc-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage
```bash
python3 cli.py
```

---

## Design Notes
* Focuses on reasoning and prioritization, not exploit delivery
* Keeps exploitation logic separate from analysis
* Assumes the user understands basic privesc concepts
* Designed to be transparent rather than fully autonomous

---

## Limitations
* Work in progress
* Suggestions may be incomplete or incorrect
* Requires human judgment before acting on any recommendation
* Not intended for automated exploitation
* Requires API key

---

## Future Enhancements
* Better structured input from enumeration tools
* Improved prompt tuning and reasoning consistency
* Confidence scoring for suggested vectors
* Modular plugin system for checks
* Expanded test coverage

---

## License
MIT License
