import click
from rich.console import Console
from rich.markdown import Markdown
from .enumeration.runner import EnumerationRunner
from .analysis.analyzer import PrivescAnalyzer

console = Console()

@click.group()
def cli():
    """PrivEsc-AI: AI-powered privilege escalation assistant"""
    pass

@cli.command()
@click.option('--full', is_flag=True, help='Run full LinPEAS enumeration')
@click.option('--quick', is_flag=True, help='Run quick custom enumeration only')
@click.option('--exploits', is_flag=True, help='Search for exploits')
@click.option('--output', '-o', help='Save results to file')
def scan(full, quick, exploits, output):
    """Run enumeration and AI analysis"""

    console.print("[bold blue]Starting PrivEsc-AI...[/bold blue]\n")

    enumerator = EnumerationRunner()
    analyzer = PrivescAnalyzer()

    console.print("[yellow]Gathering system information...[/yellow]")
    system_info = enumerator.get_system_info()

    console.print(f"  OS: {system_info['os']}")
    console.print(f"  Kernel: {system_info['kernel']}")
    console.print(f"  User: {system_info['user']}\n")

    # Run enumeration
    if quick or not full:
        console.print("[yellow]Running quick enumeration...[/yellow]")
        custom_results = enumerator.run_custom_enum()

        console.print("[yellow]Analyzing for quick wins...[/yellow]\n")
        findings = analyzer.quick_wins_check(custom_results)

    else:
        console.print("[yellow]Running LinPEAS (this may take a while)...[/yellow]")
        linpeas_output = enumerator.run_linpeas()

        console.print("[yellow]Analyzing with AI...[/yellow]\n")
        findings = analyzer.analyze(system_info, linpeas_output)

    # display results
    console.print("[bold green]Analysis Results:[/bold green]\n")
    md = Markdown(findings)
    console.print(md)

    if exploits:
        console.print("[yellow]Searching for exploits...[/yellow]\n")

        if full:
            findings = analyzer.analyze_with_exploits(system_info, linpeas_output)
        else:
            suid_check = analyzer.check_suid_exploits(custom_results.get('suid_files', ''))
            findings += f"\n\n{suid_check}"

    # save if requested
    if output:
        with open(output, 'w') as f:
            f.write(findings)
        console.print(f"\n[green]Results saved to {output}[/green]")

@cli.command()
def test():
    """Test API connection"""
    try:
        analyzer = PrivescAnalyzer()
        console.print("[green] API connection successfull[/green]")
        console.print(f"Using model: {analyzer.client}")
    except Exception as e:
        console.print(f"[red] API connection failed: {str(e)}[/red]")

if __name__ == '__main__':
    cli()
