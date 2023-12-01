import re


# Check input for a valid URL address.
def is_valid_url(url):
    # Compiles a regular expression pattern to match a valid URL.
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # Matches the protocols http, https, ftp, ftps
        r'(?:[\w-]+\.?)+'  # Matches the domain name
        r'(?::\d+)?'  # Matches an optional port number
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Returns whether the given URL matches the compiled regex pattern.
    return re.match(regex, url) is not None
