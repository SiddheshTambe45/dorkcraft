#!/usr/bin/env python3
"""
DorkCraft CLI - Interactive Mode
A command-line tool for building Google dorks interactively
"""

import webbrowser
from urllib.parse import quote_plus
from typing import Optional


class DorkBuilder:
    """Build search engine dorks from parameters"""
    
    ENGINES = {
        '1': ('google', 'https://www.google.com/search?q='),
        '2': ('duckduckgo', 'https://duckduckgo.com/?q='),
        '3': ('bing', 'https://www.bing.com/search?q=')
    }
    
    def __init__(self, engine_choice: str = '1'):
        """Initialize DorkBuilder with search engine"""
        if engine_choice not in self.ENGINES:
            engine_choice = '1'
        self.engine_name, self.base_url = self.ENGINES[engine_choice]
    
    def build_dork(
        self,
        domain: Optional[str] = None,
        intitle: Optional[str] = None,
        inurl: Optional[str] = None,
        filetype: Optional[str] = None,
        intext: Optional[str] = None,
        exact: Optional[str] = None
    ) -> str:
        """Build a dork query from parameters"""
        parts = []
        
        if domain:
            parts.append(self._format_field('site', domain))
        
        if intitle:
            parts.append(self._format_field('intitle', intitle, quoted=True))
        
        if inurl:
            parts.append(self._format_field('inurl', inurl))
        
        if filetype:
            parts.append(self._format_field('filetype', filetype))
        
        if intext:
            parts.append(self._format_field('intext', intext, quoted=True))
        
        if exact:
            values = [v.strip() for v in exact.split(',') if v.strip()]
            if len(values) == 1:
                parts.append(f'"{values[0]}"')
            elif len(values) > 1:
                parts.append('(' + ' OR '.join(f'"{v}"' for v in values) + ')')
        
        return ' '.join(parts)
    
    def _format_field(self, operator: str, value: str, quoted: bool = False) -> str:
        """Format a field with its operator"""
        values = [v.strip() for v in value.split(',') if v.strip()]
        
        if not values:
            return ''
        
        if len(values) == 1:
            if quoted:
                return f'{operator}:"{values[0]}"'
            return f'{operator}:{values[0]}'
        
        # Multiple values - use OR logic
        if quoted:
            formatted = [f'{operator}:"{v}"' for v in values]
        else:
            formatted = [f'{operator}:{v}' for v in values]
        
        return '(' + ' OR '.join(formatted) + ')'
    
    def get_search_url(self, dork: str) -> str:
        """Get the full search URL for a dork"""
        return self.base_url + quote_plus(dork)


def print_banner():
    """Print DorkCraft CLI banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║                    DorkCraft CLI                         ║
║              Advanced OSINT Dork Builder                 ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_separator():
    """Print a separator line"""
    print("─" * 60)


def get_input(prompt: str, hint: str = "", optional: bool = True) -> Optional[str]:
    """Get user input with optional hint"""
    full_prompt = f"\n{prompt}"
    if hint:
        full_prompt += f"\n  ({hint})"
    if optional:
        full_prompt += "\n  [Press Enter to skip]"
    full_prompt += "\n> "
    
    value = input(full_prompt).strip()
    return value if value else None


def main():
    """Main interactive CLI"""
    print_banner()
    print("\nWelcome! Let's build your search dork interactively.\n")
    print("Tip: Use commas to separate multiple values (they'll be OR'd together)")
    print_separator()
    
    # Select search engine
    print("\nSelect Search Engine:")
    print("  1. Google (default)")
    print("  2. DuckDuckGo")
    print("  3. Bing")
    engine = input("\nChoice [1-3]: ").strip() or '1'
    
    if engine not in ['1', '2', '3']:
        print("Invalid choice, using Google")
        engine = '1'
    
    builder = DorkBuilder(engine)
    print(f"\nUsing: {builder.engine_name.upper()}")
    print_separator()
    
    # Collect dork parameters
    print("\n📋 Enter your search parameters:\n")
    
    domain = get_input(
        "Domain (site:)",
        "e.g., example.com or site1.com,site2.com"
    )
    
    intitle = get_input(
        "Title (intitle:)",
        "e.g., login or admin,dashboard"
    )
    
    inurl = get_input(
        "URL (inurl:)",
        "e.g., admin or /login,/admin"
    )
    
    filetype = get_input(
        "File Type (filetype:)",
        "e.g., pdf or pdf,doc,xls"
    )
    
    intext = get_input(
        "Content (intext:)",
        "e.g., password or confidential,secret"
    )
    
    exact = get_input(
        "Exact Phrase",
        "e.g., \"user credentials\" or phrase1,phrase2"
    )
    
    # Check if any parameters were provided
    has_params = any([domain, intitle, inurl, filetype, intext, exact])
    
    if not has_params:
        print("\n❌ No parameters provided. Exiting.")
        return
    
    # Build the dork
    print_separator()
    print("\n🔨 Building your dork...\n")
    
    dork = builder.build_dork(
        domain=domain,
        intitle=intitle,
        inurl=inurl,
        filetype=filetype,
        intext=intext,
        exact=exact
    )
    
    # Display results
    print_separator()
    print("\n✅ Generated Dork:\n")
    print(f"  {dork}\n")
    print_separator()
    
    # Search URL
    search_url = builder.get_search_url(dork)
    print(f"\n🔗 Search URL:\n")
    print(f"  {search_url}\n")
    print_separator()
    
    # Actions
    print("\n📌 What would you like to do?\n")
    print("  1. Copy dork to clipboard")
    print("  2. Open search in browser")
    print("  3. Both")
    print("  4. Exit")
    
    action = input("\nChoice [1-4]: ").strip()
    
    if action in ['1', '3']:
        try:
            import pyperclip
            pyperclip.copy(dork)
            print("\n✅ Dork copied to clipboard!")
        except ImportError:
            print("\n⚠️  pyperclip not installed. Install with: pip install pyperclip")
            print(f"\nManually copy: {dork}")
    
    if action in ['2', '3']:
        print(f"\n🌐 Opening search in {builder.engine_name}...")
        webbrowser.open(search_url)
    
    print("\n✨ Done! Thanks for using DorkCraft CLI.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Exiting gracefully.")
    except Exception as e:
        print(f"\n❌ Error: {e}")