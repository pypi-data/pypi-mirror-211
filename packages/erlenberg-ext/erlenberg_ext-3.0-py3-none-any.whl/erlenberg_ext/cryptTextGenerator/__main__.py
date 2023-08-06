from getpass import getpass
from erlenberg_ext.simpleCrypt import encrypt

def main():
    import argparse

    parser = argparse.ArgumentParser(description=
        """Tool to generate encrypted string""")
    parser.add_argument("-i", "--iterations", nargs='?', help = "iteration for key derivation function", type=int, default=390000)
    args = parser.parse_args()

    toEncrypt= getpass('Please input the text you want to encrypt\n> ')
    password= getpass('Please input a password\n> ')

    print(encrypt(toEncrypt, password, iterations=args.iterations))

if __name__ == "__main__":
	main()
