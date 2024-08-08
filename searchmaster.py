import requests
from bs4 import BeautifulSoup
from googlesearch import search
from requests.exceptions import HTTPError, RequestException
import signal
import sys
import argparse
from colorama import init, Fore, Style
import random

# Initialize colorama
init(autoreset=True)

# Example dork queries
EXAMPLE_DORKS = [
    'intitle:"index of" "parent directory"',
    'filetype:sql "password"',
    'inurl:admin "login"',
    'intitle:"login" "username"',
    'inurl:php?id=',
]

# Global variables to store findings
findings_dork = []
findings_normal = []

def signal_handler(sig, frame):
    """
    Handle signals to suspend the tool and show collected results.
    """
    print(Fore.RED + "\nInterrupted! Displaying collected results...\n")
    print_findings("Summary of Dork Results (Collected so far):", findings_dork)
    print_findings("Summary of Normal Search Results (Collected so far):", findings_normal)
    sys.exit(0)

def fetch_google_results(query, num_results=10):
    """
    Fetch Google search results based on a query.
    
    Parameters:
    query (str): The search query (dork + user term).
    num_results (int): The number of search results to return.
    
    Returns:
    list: A list of dictionaries containing URLs and titles.
    """
    urls = []
    try:
        for url in search(query, num_results=num_results, lang="en"):
            urls.append(url)
    except Exception as e:
        print(Fore.RED + f"Error during Google search: {e}")
        return []

    results = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            # Check if the content type is HTML
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string.strip() if soup.title else 'No Title'
                results.append({'url': url, 'title': title})
            else:
                print(Fore.YELLOW + f"Skipped non-HTML content: {url}")
        except HTTPError as e:
            print(Fore.RED + f"HTTP error fetching {url}: {e}")
        except RequestException as e:
            print(Fore.RED + f"Request error fetching {url}: {e}")
        except Exception as e:
            print(Fore.RED + f"Error processing {url}: {e}")
    
    return results

def analyze_results(results, search_term):
    """
    Analyze results to find those that contain the search term.
    
    Parameters:
    results (list): List of result dictionaries containing URLs and titles.
    search_term (str): The term to search for in the page content.
    
    Returns:
    list: A list of dictionaries with URLs and titles of pages containing the search term.
    """
    findings = []
    for result in results:
        try:
            response = requests.get(result['url'], timeout=10)
            response.raise_for_status()
            
            content = response.text
            
            if search_term.lower() in content.lower():
                findings.append({
                    'url': result['url'],
                    'title': result['title']
                })
        except Exception as e:
            print(Fore.RED + f"Error analyzing {result['url']}: {e}")
    
    return findings

def filter_social_media(results):
    """
    Filter results for social media links.
    
    Parameters:
    results (list): List of result dictionaries containing URLs and titles.
    
    Returns:
    list: A list of filtered results that contain social media links.
    """
    social_media_domains = ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com']
    filtered_results = [result for result in results if any(domain in result['url'] for domain in social_media_domains)]
    return filtered_results

def filter_files(results):
    """
    Filter results for file links.
    
    Parameters:
    results (list): List of result dictionaries containing URLs and titles.
    
    Returns:
    list: A list of filtered results that contain file links.
    """
    file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
    filtered_results = [result for result in results if any(result['url'].lower().endswith(ext) for ext in file_extensions)]
    return filtered_results

def save_results_to_file(filename, findings):
    """
    Save the findings to an output file.
    
    Parameters:
    filename (str): The name of the file to save the results to.
    findings (list): The list of findings to save.
    """
    with open(filename, 'w') as file:
        for finding in findings:
            file.write(f"Title: {finding['title']}\n")
            file.write(f"URL: {finding['url']}\n")
            file.write("-" * 80 + "\n")
    print(Fore.CYAN + f"Results saved to {filename}")

def display_banner():
    """
    Display a colorful banner for the tool.
    """
    banners = [
        """
        ____   ____  _____  _      ____   _____ 
       |  _ \\ / __ \\|  __ \\| |    / __ \\ / ____|
       | |_) | |  | | |  | | |   | |  | | (___  
       |  _ <| |  | | |  | | |   | |  | |\\___ \\ 
       | |_) | |__| | |__| | |___| |__| |____) |
       |____/ \\____/|_____/|______\\____/|_____/ 
        """,
        """
        _____                _          _      
       / ____|              | |        | |     
      | (___   ___ _ __   __| | ___  ___| | ___ 
       \\___ \\ / _ \\ '_ \\ / _` |/ _ \\/ __| |/ _ \\
       ____) |  __/ | | | (_| |  __/\\__ \\ |  __/
      |_____/ \\___|_| |_|\\__,_|\\___||___/_|\\___|
        """,
        """
        __     __          _        _   
        \\ \\   / /         | |      | |  
         \\ \\_/ /__  _ __ | |_ __ _| |_ 
          \\   / _ \\| '_ \\| __/ _` | __|
           | | (_) | | | | || (_| | |_ 
           |_|\\___/|_| |_|\\__\\__,_|\__|
        """
    ]
    banner = random.choice(banners)
    print(Fore.CYAN + Style.BRIGHT + banner)

def print_findings(title, findings):
    """
    Print the findings with clear formatting.
    
    Parameters:
    title (str): The title of the findings section.
    findings (list): The list of findings to print.
    """
    print(Fore.YELLOW + "\n" + title + Fore.RESET)
    if findings:
        for i, finding in enumerate(findings, start=1):
            print(Fore.GREEN + f"{i}. {finding['title']}")
            print(Fore.GREEN + f"   URL: {finding['url']}")
            print(Fore.RESET + "-" * 80)  # Separator line for clarity
    else:
        print(Fore.RED + "No results found.")
    print("\n")  # Newline for better spacing

def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
    Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="SearchMaster - An advanced Google search tool.")
    parser.add_argument('-d', '--dork', action='store_true', help='Perform a dork scan.')
    parser.add_argument('-n', '--normal', action='store_true', help='Perform a normal scan.')
    parser.add_argument('-a', '--all', action='store_true', help='Perform both dork and normal scans.')
    parser.add_argument('-o', '--output', type=str, help='Output file to save results.')
    parser.add_argument('-u', '--unavailable', action='store_true', help='Show unavailable URLs.')
    parser.add_argument('-v', '--available', action='store_true', help='Show available URLs.')
    parser.add_argument('-s', '--social', action='store_true', help='Filter results for social media links.')
    parser.add_argument('-f', '--file', action='store_true', help='Filter results for file links.')
    parser.add_argument('-r', '--results', type=int, default=10, help='Number of search results to retrieve.')
    parser.add_argument('search_term', nargs='?', default=None, help='The term to search for.')
    
    return parser.parse_args()

def main():
    """
    Main function to run the tool based on command-line arguments.
    """
    # Display banner
    display_banner()

    # Parse arguments
    args = parse_args()

    # Set up signal handler for graceful exit
    signal.signal(signal.SIGINT, signal_handler)

    if not args.search_term:
        print(Fore.RED + "Error: Search term is required.")
        sys.exit(1)
    
    if not any([args.dork, args.normal, args.all]):
        print(Fore.RED + "Error: At least one scan type must be specified.")
        sys.exit(1)
    
    global findings_dork, findings_normal
    findings_dork = []
    findings_normal = []

    if args.dork or args.all:
        print(Fore.CYAN + "Performing dork scan...")
        for dork in EXAMPLE_DORKS:
            dork_query = f"{dork} {args.search_term}"
            print(Fore.YELLOW + f"Searching with dork: {dork_query}")
            dork_results = fetch_google_results(dork_query, num_results=args.results)
            findings_dork.extend(analyze_results(dork_results, args.search_term))
        
        if args.social:
            findings_dork = filter_social_media(findings_dork)
        
        if args.file:
            findings_dork = filter_files(findings_dork)
        
        if args.output:
            save_results_to_file(args.output, findings_dork)
        
        print_findings("Dork Scan Results:", findings_dork)

    if args.normal or args.all:
        print(Fore.CYAN + "Performing normal scan...")
        normal_results = fetch_google_results(args.search_term, num_results=args.results)
        findings_normal.extend(analyze_results(normal_results, args.search_term))
        
        if args.social:
            findings_normal = filter_social_media(findings_normal)
        
        if args.file:
            findings_normal = filter_files(findings_normal)
        
        if args.output:
            save_results_to_file(args.output, findings_normal)
        
        print_findings("Normal Scan Results:", findings_normal)

if __name__ == "__main__":
    main()
