# main.py

import os
from tools import check_and_install_tools, get_subdomains, filter_and_save_subdomains
from display import display_interface

def main(url):
    display_interface()
    
    # Check and install tools if necessary
    check_and_install_tools()
    
    # Extract the main domain name for directory creation
    main_domain = url.split("//")[-1].split("/")[0]
    
    # Create a directory named after the main domain
    if not os.path.exists(main_domain):
        os.makedirs(main_domain)
    
    subdomains = get_subdomains(url)
    if subdomains:
        print(f"\033[92mFound {len(subdomains)} subdomains\033[0m")
        
        # Save all subdomains to a file
        with open(os.path.join(main_domain, "All_Subdomains.txt"), "w") as file_all:
            for item in subdomains:
                file_all.write(f"{item}\n")
        
        filter_and_save_subdomains(subdomains, main_domain)
    else:
        print("\033[91mNo subdomains found\033[0m")

if __name__ == "__main__":
    target_url = input("\033[96mEnter the URL: \033[0m").strip()
    main(target_url)
