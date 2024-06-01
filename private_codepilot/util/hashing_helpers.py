"""Hashing Helpers"""

import hashlib


def md5_of_list(lst):
    # Convert list to string
    list_str = str(lst)
    # Encode the string to bytes
    list_bytes = list_str.encode("utf-8")
    # Create MD5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the bytes
    md5_hash.update(list_bytes)
    # Get the hexadecimal representation of the hash
    hash_result = md5_hash.hexdigest()
    return hash_result
