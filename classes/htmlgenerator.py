import re
import cv2
from PIL import Image

IMAGE_REGEX = 'jpg|webp'
AUDIO_REGEX = 'opus'
VIDEO_REGEX = 'mp4'
TEXT_REGEX = re.compile(r'(?!.*(<adjunto:|\(archivo adjunto\))).*')
LINK_REGEX = re.compile(r'((http|https):\/\/[\w\/\-?=%.]+\.[\w\/\-?=%&+.]+)')
# LINK_REGEX = re.compile(r'((https|http):\/\/.+)')
# TEXT_REGEX = re.compile(r'(^[^<].+)')
# FILE_REGEX = re.compile(f'(\<.+\: .+\.)({IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX})')
# FILENAME_REGEX = re.compile(f'\<.+\: (.+\.[{IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX}]+)')

# FILE_REGEX = re.compile(f'(\<.+\: .+\.)({IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX})')
# FILENAME_REGEX = re.compile(f'\<.+\: (.+\.[{IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX}]+)')


FILE_REGEX = re.compile(f'((?:<.*: )?(.+.)({IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX})|((.+.)({IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX})))')
# FILE_REGEX = re.compile(f'((?:<.* )?(.+\.)({IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX})(?:\s\(.+\)|>)?)')
FILENAME_REGEX = re.compile(f'([a-zA-Z0-9\-]+\.({IMAGE_REGEX}|{AUDIO_REGEX}|{VIDEO_REGEX}))')
# ((?:<.* )?(.+\.)(jpg|mp4|opus)(?:\s\(.+\)|>)?)

class LineType(object):
    UNDEFINED = 0
    TEXT = 1
    LINK = 2
    IMAGE = 3
    AUDIO = 4
    VIDEO = 5

class HtmlGenerator(object):
    def __init__(self, chatline=None):
        self.chatline = chatline
        if chatline is not None:
            self.type = self.getType(chatline.message)
        else:
            self.type = LineType.UNDEFINED

    def getType(self, message):
        if LINK_REGEX.match(message):
            return LineType.LINK

        if TEXT_REGEX.match(message):
            return LineType.TEXT
        
        match = FILE_REGEX.match(message)
        if match is not None:
            extension = match.group(3)
            if re.compile(IMAGE_REGEX).match(extension):
                return LineType.IMAGE
            elif re.compile(AUDIO_REGEX).match(extension):
                return LineType.AUDIO
            elif re.compile(VIDEO_REGEX).match(extension):
                return LineType.VIDEO
        
        return LineType.UNDEFINED

    def getMessage(self):
        if (self.type == LineType.TEXT):
            return self.chatline.message
        elif (self.type == LineType.LINK):
            return self.chatline.message
        elif (self.type == LineType.IMAGE or self.type == LineType.AUDIO or self.type == LineType.VIDEO):
            search = FILENAME_REGEX.search(self.chatline.message)
            return search.group(1)
        return ''

    def generateVideoThumbnail(self, inPath, outPath, w=100, h=70):
        try:
            cap = cv2.VideoCapture(inPath)
            videoLength = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
            # print('Video length', videoLength)
            while cap.isOpened():
                try:
                    ret, frame = cap.read()
                    cv2.imwrite(outPath, frame)
                    break
                except:
                    pass
            cap.release()
            img = Image.open(outPath)
            img = img.resize((w, h), Image.ANTIALIAS)
            img.save(outPath)
        except Exception as e:
            print('Error generating thumbnail from', inPath, e)
            return e

    def htmlOLD(self, isSender):
        # TEXT
        if (self.type == LineType.TEXT):
            if (isSender):
                return '''
                        <div class="message sent">
                            {0}
                            <span class="metadata">
                                <span class="time">{1}</span>
                                <span class="tick">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="15" id="msg-dblcheck-ack" x="2063" y="2076"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.88a.32.32 0 0 1-.484.032l-.358-.325a.32.32 0 0 0-.484.032l-.378.48a.418.418 0 0 0 .036.54l1.32 1.267a.32.32 0 0 0 .484-.034l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.88a.32.32 0 0 1-.484.032L1.892 7.77a.366.366 0 0 0-.516.005l-.423.433a.364.364 0 0 0 .006.514l3.255 3.185a.32.32 0 0 0 .484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z" fill="#4fc3f7"/></svg>
                                </span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.chatline.getTime())
            else:
                return '''
                        <div class="message received">
                            {0}
                            <span class="metadata">
                                <span class="time">{1}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.chatline.getTime())
        
        # LINK
        if (self.type == LineType.LINK):
            fullMessage = self.getMessage()
            search = LINK_REGEX.search(fullMessage)
            link = search.group(1)
            textMessage = fullMessage.replace(link, '')
            print('** LINK full', fullMessage)
            print('** LINK enlace', link)
            print('** LINK text', textMessage)

            if (isSender):
                return '''
                        <div class="message sent">
                            {0}
                            <a href="{1}" target="_blank">{1}</a>
                            <span class="metadata">
                                <span class="time">{2}</span>
                                <span class="tick">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="15" id="msg-dblcheck-ack" x="2063" y="2076"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.88a.32.32 0 0 1-.484.032l-.358-.325a.32.32 0 0 0-.484.032l-.378.48a.418.418 0 0 0 .036.54l1.32 1.267a.32.32 0 0 0 .484-.034l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.88a.32.32 0 0 1-.484.032L1.892 7.77a.366.366 0 0 0-.516.005l-.423.433a.364.364 0 0 0 .006.514l3.255 3.185a.32.32 0 0 0 .484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z" fill="#4fc3f7"/></svg>
                                </span>
                            </span>
                        </div>
                '''.format(textMessage, link, self.chatline.getTime())
            else:
                return '''
                        <div class="message received">
                            {0}
                            <a href="{1}" target="_blank">{1}</a>
                            <span class="metadata">
                                <span class="time">{2}</span>
                            </span>
                        </div>
                '''.format(textMessage, link, self.chatline.getTime())

        # IMAGE
        elif (self.type == LineType.IMAGE):
            if (isSender):
                return '''
                        <div class="message sent">
                            <a href='attach/{0}' class='glightbox'>
                                <img src='attach/{0}' class='media' />
                            </a>
                            <span class="metadata">
                                <span class="time">{1}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.chatline.getTime())
            else:
                return '''
                        <div class="message received">
                            <a href='attach/{0}' class='glightbox'>
                                <img src='attach/{0}' class='media' />
                            </a>
                            <span class="metadata">
                                <span class="time">{1}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.chatline.getTime())

        # AUDIO
        elif (self.type == LineType.AUDIO):
            if (isSender):
                return '''
                        <div class="message sent">
                            <audio controls class='media' />
                                <source src='attach/{0}' type='audio/x-wav'>
                            </audio>
                            <span class="metadata">
                                <span class="time">{1}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.chatline.getTime())
            else:
                return '''
                        <div class="message received">
                            <audio controls class='media' />
                                <source src='attach/{0}' type='audio/x-wav'>
                            </audio>
                            <span class="metadata">
                                <span class="time">{1}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.chatline.getTime())

        # VIDEO
        elif (self.type == LineType.VIDEO):
            if (isSender):
                return '''
                        <div class="message sent">
                            <a href='attach/{0}' class='glightbox'>
                                <img src='img/{1}' class='media' />
                            </a>
                            <span class="metadata">
                                <span class="time">{2}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.getMessage().replace('mp4', 'png'), self.chatline.getTime())
            else:
                return '''
                        <div class="message received">
                            <a href='attach/{0}' class='glightbox'>
                                <img src='img/{1}' class='media' />
                            </a>
                            <span class="metadata">
                                <span class="time">{2}</span>
                            </span>
                        </div>
                '''.format(self.getMessage(), self.getMessage().replace('mp4', 'png'), self.chatline.getTime())

        return ''



    def generateInfoMessage(self, message):
        return f'''
            <div class="info-message">
                <div>{message}</div>
            </div>
        '''

    def html(self, isSender=True, firstMessage=False):
        className = 'sent' if isSender else 'received'
        htmlChunk = f'<div class="message {className}">'

        if firstMessage and not isSender: # USERNAME
            htmlChunk += f'<span class="username">{self.chatline.getUser()}</span>'

        if (self.type == LineType.TEXT): # TEXT
            htmlChunk += self.getMessage()

        if (self.type == LineType.LINK): # LINK
            fullMessage = self.getMessage()
            search = LINK_REGEX.search(fullMessage)
            link = search.group(1)
            textMessage = fullMessage.replace(link, '')
            # print('** LINK full', fullMessage)
            # print('** LINK enlace', link)
            # print('** LINK text', textMessage)
            htmlChunk += f'{textMessage}<a href="{link}" target="_blank">{link}</a>'

        if (self.type == LineType.IMAGE): # IMAGE
            htmlChunk += f'''
                <a href='attach/{self.getMessage()}' class='glightbox'>
                    <img src='attach/{self.getMessage()}' class='media' />
                </a>
            '''
        
        if (self.type == LineType.AUDIO): # AUDIO
            htmlChunk += f'''
                <audio controls class='media' />
                    <source src='attach/{self.getMessage()}' type='audio/x-wav'>
                </audio>
            '''
        
        if (self.type == LineType.VIDEO): # VIDEO
            htmlChunk += f'''
                <a href='attach/{self.getMessage()}' class='glightbox'>
                    <img src='img/{self.getMessage().replace('mp4', 'png')}' class='media' />
                </a>
            '''

        # TIME INFO
        if isSender:
            htmlChunk += f'''
                <span class="metadata">
                    <span class="time">{self.chatline.getTime()}</span>
                    <span class="tick">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="15" id="msg-dblcheck-ack" x="2063" y="2076"><path d="M15.01 3.316l-.478-.372a.365.365 0 0 0-.51.063L8.666 9.88a.32.32 0 0 1-.484.032l-.358-.325a.32.32 0 0 0-.484.032l-.378.48a.418.418 0 0 0 .036.54l1.32 1.267a.32.32 0 0 0 .484-.034l6.272-8.048a.366.366 0 0 0-.064-.512zm-4.1 0l-.478-.372a.365.365 0 0 0-.51.063L4.566 9.88a.32.32 0 0 1-.484.032L1.892 7.77a.366.366 0 0 0-.516.005l-.423.433a.364.364 0 0 0 .006.514l3.255 3.185a.32.32 0 0 0 .484-.033l6.272-8.048a.365.365 0 0 0-.063-.51z" fill="#4fc3f7"/></svg>
                    </span>
                </span>
            '''
        else:
            htmlChunk += f'''
                <span class="metadata">
                    <span class="time">{self.chatline.getTime()}</span>
                </span>
            '''
        
        htmlChunk += '</div>'
        return htmlChunk
