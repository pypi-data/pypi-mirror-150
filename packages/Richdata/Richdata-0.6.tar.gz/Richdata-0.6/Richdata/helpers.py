import re


def camel_to_snake(name):
    """
    Pasa de notacion CamelCase a Snake
    Ejemplos:
    print(camel_to_snake('camel2_camel2_case'))  # camel2_camel2_case
    print(camel_to_snake('getHTTPResponseCode'))  # get_http_response_code
    print(camel_to_snake('HTTPResponseCodeXYZ'))  # http_response_code_xyz
    :param name:
    :return:
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def snake_to_camel(name):
    """
    Pasa de notacion Snake a CamelCase
    :param name:
    :return:
    """
    name = ''.join(word.title() for word in name.split('_'))
    return name


# Print iterations progress
def progress_bar(iteration, total, prefix='Progress:', suffix='Complete', decimals=1, length=100, fill='█',
                 print_end="\r"):
    """
    Call in a loop to create full compatible terminal and jupyter notebooks progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()

def uuid_to_date(uuid):
    # convert to unix_epoch
    seconds_since_unix_epoch = int(uuid[:8], base=16)
    # convert to datetime
    from datetime import timedelta, date
    date = timedelta(seconds=seconds_since_unix_epoch) + date(1970, 1, 1)
    # return
    return seconds_since_unix_epoch


def date_to_uuid(date):
    import time,datetime
    # return Math.floor(date.getTime() / 1000).toString(16) + "0000000000000000";
    seconds_since_unix_epoch= datetime.datetime.timestamp(date)*1000
    return seconds_since_unix_epoch