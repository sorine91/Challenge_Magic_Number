import requests, json


def download_json(URL):
    """Download JSON from the internet and parse it

    Args:
        URL (str): URL to fetch the JSON from

    Returns:
        dict: Parsed JSON as a dictionary or None if an error occurs
    """
    try:
        resp = requests.get(URL)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"ERREUR : Impossible de récupérer le fichier JSON, {e}")
        return None
    except ValueError:
        print("ERREUR : La réponse n'est pas un fichier JSON valide")
        return None


def check_file_signature(file_path, magic_dict):
    """Check the file signature and determine the file type based on magic numbers

    Args:
        file_path (String): Path of the file to check
        magic_dict (Dict): A dictionary containing magic numbers and file type information

    Returns:
        extension (String): File extension or None if error
        mime (String): File MIME or None if error
    """
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
    except:
        print("ERREUR : Impossible de trouver le fichier fournis")

    try:
        signatures = []
        for extension, infos in magic_dict.items():
            for sign in infos["signs"]:
                offset, hex_sign = sign.split(",")
                offset = int(offset)
                bytes_sign = bytes.fromhex(hex_sign)
                signatures.append((extension, infos["mime"], offset, bytes_sign))

        signatures.sort(key=lambda x: len(x[3]), reverse=True)

        for extension, mime, offset, bytes_sign in signatures:
            if file_data[offset : offset + len(bytes_sign)] == bytes_sign:
                print(f'Le fichier peut-être un .{extension} avec le MIME "{mime}"')
                return extension, mime

        print("ERREUR : Aucune signature correspondante trouvée")
        return None, None
    except:
        print("ERREUR : Impossible de trouver la signature du fichier")
        return None, None


MAGIC_NUMBER_URL = "https://gist.githubusercontent.com/qti3e/6341245314bf3513abb080677cd1c93b/raw/80d7838ba189849e492a4f5f3da88c84390c1250/extensions.json"
magic_dict = download_json(MAGIC_NUMBER_URL)
if magic_dict:
    filepath = input("Entrez le fichier -> ")
    check_file_signature(filepath, magic_dict)
