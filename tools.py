# tools.py
import subprocess
import os
def check_and_install_tools():
    try:
        subprocess.run(["subfinder", "-h"], capture_output=True, text=True)
    except FileNotFoundError:
        print("subfinder not found")


def get_subdomains(url):
    subdomains = set()
    try:
        print("\033[93mFetching subdomains ...\033[0m")
        result = subprocess.run(["subfinder", "-d", url, "-silent"], capture_output=True, text=True)
        subdomains.update(result.stdout.split())
    except Exception as e:
        print(f"\033[91mError running subfinder: {e}\033[0m")
    return list(subdomains)

def filter_and_save_subdomains(subdomains, directory):
    try:
        subdomains_input = "\n".join(subdomains)
        result = subprocess.run(
            ["httpx", "-silent", "-status-code", "-no-color"],
            input=subdomains_input,
            capture_output=True,
            text=True
        )

        response_200 = []
        response_302 = []
        response_403 = []
        response_404 = []

        for line in result.stdout.splitlines():
            if "200" in line:
                response_200.append(line.split()[0])
            elif "302" in line:
                response_302.append(line.split()[0])
            elif "403" in line:
                response_403.append(line.split()[0])
            elif "404" in line:
                response_404.append(line.split()[0])

        with open(os.path.join(directory, "Response-200.txt"), "w") as file_200:
            for item in response_200:
                file_200.write(f"{item}\n")

        with open(os.path.join(directory, "Response-302.txt"), "w") as file_302:
            for item in response_302:
                file_302.write(f"{item}\n")

        with open(os.path.join(directory, "Response-403.txt"), "w") as file_403:
            for item in response_403:
                file_403.write(f"{item}\n")
        
        with open(os.path.join(directory, "Response-404.txt"), "w") as file_404:
            for item in response_404:
                file_404.write(f"{item}\n")

        print(f"\033[92mResults have been saved to\n{directory}/Response-200.txt\n{directory}/Response-302.txt\n{directory}/Response-403.txt\n{directory}/Response-404.txt.\033[0m")

    except Exception as e:
        print(f"\033[91mError running httpx: {e}\033[0m")
