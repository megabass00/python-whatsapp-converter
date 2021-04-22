import re
import datetime

# patterns
DATE_REGEX = r'\d{1,2}\/\d{1,2}\/\d{1,2}'
TIME_REGEX = r'\d{1,2}:\d{1,2}(?::\d{1,2})?'
USER_REGEX = r'[a-zA-Z0-9 ]*'
MESSAGE_REGEX = r'.+'

# LINE_REGEX = re.compile(f'\[({DATE_REGEX})\s({TIME_REGEX})\]\s({USER_REGEX})\:[ |\u200e]+({MESSAGE_REGEX})')
LINE_REGEX = re.compile(f'(?:\[)?({DATE_REGEX})\s({TIME_REGEX})(?:\])?\s(?:-\s)?({USER_REGEX})\:[ |\u200e]+({MESSAGE_REGEX})')
# FULL_REGEX =             '(\[)?(\d{1,2}\/\d{1,2}\/\d{1,2})\s(\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2})(\])?\s(-\s)?([a-zA-Z0-9 ]*)\:[ |‎]+(.+)'
# ANDROID_REGEX = '(\d{1,2}\/\d{1,2}\/\d{1,2})\s(\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2})\s?\-\s([a-zA-Z0-9 ]*)\:[ |‎]+(.+)'

DATETIME_FORMAT = '%d/%m/%y %H:%M'
DATETIME_WITH_SECONDS_FORMAT = '%d/%m/%y %H:%M:%S'
# DATETIME_FORMAT = '%d/%m/%y %H:%M:%S'
TIME_EXPORT_FORMAT = '%H:%M'
DATE_EXPORT_FORMAT = '%A, %d %b %y'

class ChatLine(object):
    dateTime = None
    user = ''
    message = ''

    def __init__(self, line):
        self.line = line.strip()
        match = LINE_REGEX.search(line)
        if match is None:
            print('ERROR: Unable to parse', f'{line}')
        else:
            dateStr = '{} {}'.format(match.group(1), match.group(2))
            try:
                self.dateTime = datetime.datetime.strptime(dateStr, DATETIME_FORMAT)
            except ValueError:
                self.dateTime = datetime.datetime.strptime(dateStr, DATETIME_WITH_SECONDS_FORMAT)

            self.user = match.group(3)
            self.message = match.group(4)

    def getTime(self):
        if self.dateTime is None: return 'No avaible'
        return self.dateTime.strftime(TIME_EXPORT_FORMAT)
    
    def getDay(self):
        if self.dateTime is None: return 'No avaible'
        return self.dateTime.strftime(DATE_EXPORT_FORMAT)

    def getUser(self):
        if self.user is None: return 'No avaible'
        return self.user

    def getMessage(self):
        if self.message is None or self.user is None: return 'No avaible'
        return f'{self.user}: {self.message}'
