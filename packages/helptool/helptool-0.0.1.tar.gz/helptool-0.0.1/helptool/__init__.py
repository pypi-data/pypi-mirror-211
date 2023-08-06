class HelpTool():
    def __init__(self):
        self.tools = """
1) Port scan
2) Directory search
3) SSH Login
4) SSH Brute Force
5) Search exploit
6) View Exif data
7) Enum4linux (Get info about target)
8) Hping3 (Dos - DDos)

99) Exit
"""

        self.portScan = """
Port scan tools: nmap 
nmap usage: nmap <paramaters> <website address or ip address>  |  nmap -sS -sV 127.0.0.1
"""

        self.directorySearch = """
Directory search tools: dirb, gobuster, dirsearcher (https://github.com/Lessyzz/Directory-Searcher)

dirb usage: dirb <ip address> <wordlist>  |  dirb http://127.0.0.1/ /usr/share/wordlists/dirb/common.txt

gobuster usage: gobuster -e -u http://127.0.0.1/ -w /usr/share/wordlists/dirb/common.txt

dirsearcher usage: dirsearcher.py -u <url> -t <threads> -w <wordlist>
"""

        self.sshLogin = """
SSH Login tools: ssh
ssh usage: ssh <Username>@<Server IP>  |  ssh lessy@127.0.0.1
"""

        self.sshBruteForce = """
SSH Burte force tools: Hydra
hydra usage: hydra -l <username> -P <path to wordlist> <IP> ssh  |  hydra -l admin -P wordlist.txt 127.0.0.1 ssh              
"""

        self.searchExploit = """
Search exploit tools: searchsploit 
searchsploit usage: searchsploit apache 2.4.49
Also you need to update searchsploit, for update > searchsploit -u
"""

        self.viewExifData = """
Exif data viewer tools: exiftool, strings
exiftool usage: exiftool image.png
strings usage: string image.png        
"""

        self.enum4linux = """
enum4linux usage: enum4linux -a 127.0.0.1        
"""

        self.hping3 = """
hping3 usage: hping3 -S --flood -V 127.0.0.1
Another dos - ddos tools: Slowloris, Hulk, HOIC, LOIC, Tor's Hammer
        """

        self.run()

    def getInput(self):
        number = input("> ")

        match number:
            case "1":
                print(self.portScan)
            case "2":
                print(self.directorySearch)
            case "3":
                print(self.sshLogin)
            case "4":
                print(self.sshBruteForce)
            case "5":
                print(self.searchExploit)
            case "6":
                print(self.viewExifData)
            case "7":
                print(self.enum4linux)
            case "8":
                print(self.hping3)
            
            
            case "99":  
                exit()


    def run(self):
        while True:
            print(self.tools)
            self.getInput()


HelpToolRun = HelpTool()