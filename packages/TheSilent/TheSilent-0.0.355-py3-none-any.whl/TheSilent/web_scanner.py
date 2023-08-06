from ftplib import FTP, FTP_TLS
from TheSilent.clear import clear
from TheSilent.command_injection_scanner import command_injection_scanner
from TheSilent.directory_traversal_scanner import directory_traversal_scanner
from TheSilent.html_lint import html_lint
from TheSilent.link_scanner import link_scanner
from TheSilent.python_injection_scanner import python_injection_scanner
from TheSilent.sql_injection_scanner import sql_injection_scanner
from TheSilent.xss_scanner import xss_scanner

CYAN = "\033[1;36m"

# scans for security flaws and bad practices
def web_scanner(url, secure=True, tor=False, delay=1, report=True):
    clear()
    
    my_html_lint_list = []
    my_directory_traversal_scanner_list = []
    my_command_injection_scanner_list = []
    my_python_injection_scanner_list = []
    my_sql_injection_scanner_list = []
    my_xss_scanner_list = []
    
    my_link_scanner = link_scanner(url=url, secure=secure, tor=tor, delay=delay)
    for my_url in my_link_scanner:
        my_html_lint = html_lint(url=my_url, secure=secure, tor=tor)
        my_directory_traversal_scanner = directory_traversal_scanner(url=my_url, secure=secure, tor=tor, delay=delay)
        my_command_injection_scanner = command_injection_scanner(url=my_url, secure=secure, tor=tor, delay=delay)
        my_python_injection_scanner = python_injection_scanner(url=my_url, secure=secure, tor=tor, delay=delay)
        my_sql_injection_scanner = sql_injection_scanner(url=my_url, secure=secure, tor=tor, delay=delay)
        my_xss_scanner = xss_scanner(url=my_url, secure=secure, tor=tor, delay=delay)
        
        for vuln in my_html_lint:
            my_html_lint_list.append(vuln)
            
        for vuln in my_directory_traversal_scanner:
            my_directory_traversal_scanner_list.append(vuln)
            
        for vuln in my_command_injection_scanner:
            my_command_injection_scanner_list.append(vuln)
            
        for vuln in my_python_injection_scanner:
            my_python_injection_scanner_list.append(vuln)
            
        for vuln in my_sql_injection_scanner:
            my_sql_injection_scanner_list.append(vuln)
            
        for vuln in my_xss_scanner:
            my_xss_scanner_list.append(vuln)
            
    clear()
    
    new_url = url.replace("http://", "")
    new_url = new_url.replace("https://", "")
    ftp_verify = False

    try:
        ftp = FTP(new_url, timeout=15)
        ftp.login()
        ftp.close()
        ftp_verify = True
        
    except:
        pass

    try:
        ftp = FTP_TLS(new_url, timeout=15)
        ftp.login()
        ftp.close()
        ftp_verify = True
        
    except:
        pass
    
    print(CYAN + "anonymous ftp:")
    if report:
        if ftp_verify:
            with open(new_url +  ".txt", "a") as f:
                f.write("anonymous ftp: True\n")

    print(CYAN + str(ftp_verify))
    
    print(CYAN + "")
    print(CYAN + "command injection:")
    for i in my_command_injection_scanner_list:
        if report:
            if "http://" in url:
                with open(url[7:] +  ".txt", "a") as f:
                    f.write(i + "\n")
                    
            elif "https://" in url:
                with open(url[8:] +  ".txt", "a") as f:
                    f.write(i + "\n")

            else:
                with open(url +  ".txt", "a") as f:
                    f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "directory traversal:")
    for i in my_directory_traversal_scanner_list:
        if report:
            if "http://" in url:
                with open(url[7:] +  ".txt", "a") as f:
                    f.write(i + "\n")
                    
            elif "https://" in url:
                with open(url[8:] +  ".txt", "a") as f:
                    f.write(i + "\n")

            else:
                with open(url +  ".txt", "a") as f:
                    f.write(i + "\n")

        print(CYAN + i)
        
    print(CYAN + "")
    print(CYAN + "html lint:")
    for i in my_html_lint_list:
        if report:
            if "http://" in url:
                with open(url[7:] +  ".txt", "a") as f:
                    f.write(i + "\n")
                    
            elif "https://" in url:
                with open(url[8:] +  ".txt", "a") as f:
                    f.write(i + "\n")

            else:
                with open(url +  ".txt", "a") as f:
                    f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "python injection:")
    for i in my_python_injection_scanner_list:
        if report:
            if "http://" in url:
                with open(url[7:] +  ".txt", "a") as f:
                    f.write(i + "\n")
                    
            elif "https://" in url:
                with open(url[8:] +  ".txt", "a") as f:
                    f.write(i + "\n")

            else:
                with open(url +  ".txt", "a") as f:
                    f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "sql injection:")
    for i in my_sql_injection_scanner_list:
        if report:
            if "http://" in url:
                with open(url[7:] +  ".txt", "a") as f:
                    f.write(i + "\n")
                    
            elif "https://" in url:
                with open(url[8:] +  ".txt", "a") as f:
                    f.write(i + "\n")

            else:
                with open(url +  ".txt", "a") as f:
                    f.write(i + "\n")

        print(CYAN + i)

    print(CYAN + "")
    print(CYAN + "xss:")
    for i in my_xss_scanner_list:
        if report:
            if "http://" in url:
                with open(url[7:] +  ".txt", "a") as f:
                    f.write(i + "\n")
                    
            elif "https://" in url:
                with open(url[8:] +  ".txt", "a") as f:
                    f.write(i + "\n")

            else:
                with open(url +  ".txt", "a") as f:
                    f.write(i + "\n")
                
        print(CYAN + i)
