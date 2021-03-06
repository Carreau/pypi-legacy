import zipfile
import tarfile
import gzip
import bz2
import StringIO
import sys


def trim_docstring(text):
    """
    Trim indentation and blank lines from docstring text & return it.

    See PEP 257.
    """
    if not text:
        return text
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = text.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def extractPackageReadme(content, filename, filetype):
    '''Extract the README from a file and attempt to turn it into HTML.

    Return the source text and html version or empty strings in either case if
    extraction fails.
    '''
    text = ''
    if filename.endswith('.zip') or filename.endswith('.egg'):
        try:
            t = StringIO.StringIO(content)
            t.filename = filename
            zip = zipfile.ZipFile(t)
            l = zip.namelist()
        except zipfile.error:
            return '', ''
        for entry in l:
            parts = entry.split('/')
            if len(parts) != 2:
                continue
            filename = parts[-1]
            if filename.count('.') > 1:
                continue
            if filename.count('.') == 1:
                name, ext = filename.split('.')
            else:
                # just use the filename and assume a readme is plain text
                name = filename
                ext = 'txt'
            if name.upper() != 'README':
                continue
            if ext not in ('txt', 'rst', 'md'):
                return

            # grab the content and parse if it's something we might understand,
            # based on the file extension
            text = zip.open(entry).read()

            # we can only deal with UTF-8 so make it UTF-8 safe
            text = text.decode('utf-8', 'replace').encode('utf-8')

            if text:
                return text

    elif (filename.endswith('.tar.gz') or filename.endswith('.tgz') or
            filename.endswith('.tar.bz2') or filename.endswith('.tbz2')):
        # open the tar file with the appropriate compression
        ext = filename.split('.')[-1]
        if ext[-2:] == 'gz':
            file = StringIO.StringIO(content)
            file = gzip.GzipFile(filename, fileobj=file)
        else:
            file = StringIO.StringIO(bz2.decompress(content))
        try:
            tar = tarfile.TarFile(filename, 'r', file)
            l = tar.getmembers()
        except tarfile.TarError:
            return '', ''
        for entry in l:
            parts = entry.name.split('/')
            if len(parts) != 2:
                continue
            filename = parts[-1]
            if filename.count('.') > 1:
                continue
            if filename.count('.') == 1:
                name, ext = filename.split('.')
            else:
                # just use the filename and assume a readme is plain text
                name = filename
                ext = 'txt'
            if name.upper() != 'README':
                continue
            if ext not in ('txt', 'rst', 'md'):
                continue
            # grab the content and parse if it's something we might understand,
            # based on the file extension
            try:
                text = tar.extractfile(entry).read()

                # we can only deal with UTF-8 so make it UTF-8 safe
                text = text.decode('utf-8', 'replace').encode('utf-8')
            except:
                # issue 3521663: extraction may fail if entry is a symlink to
                # a non-existing file
                continue

            if text:
                return text

    return text
