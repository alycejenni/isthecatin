AWS_HEADERS = {
    'Cache-Control': 'public, max-age=86400'
}
INSIDE = 1
OUTSIDE = 0
SCHRODINGER = 2
ACCEPTED_FILES = {
    'jpg': 'img',
    'mp4': 'video',
    'png': 'img'
}
FILE_PREFIX = 'cat_'
BOOTSTRAP_URL = r'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'

REGEXES = {
    'file_timestamp': '.+_(\d+_\d+)[^\d]+'
}

BULK_EDIT_PAGE_SIZE = 36