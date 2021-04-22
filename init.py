import shutil, webbrowser, os, locale
from pathlib import Path
from zipfile import ZipFile
from classes.interface import Interface
from classes.chatline import ChatLine
from classes.htmlgenerator import HtmlGenerator, LineType


# tmpFolder = os.path.join(Path().absolute(), 'temp')
# templateFolder = os.path.join(Path().absolute(), 'template')

# talker = 'Miguel Pumuki Valencia'
# inFile = 'C:\\Users\\usuario\\Projects\\SCRIPTS\\whatsapp-chat-converter\\test.zip'
# outFolder = 'C:\\Users\\usuario\\Projects\\SCRIPTS\\whatsapp-chat-converter\\export'

# chatlines = []
# userName = 'Luis Izquierdo'

os.system('cls') 
if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, '')
    ui = Interface()










# # unzip in file
# listOfFileNames = []
# with ZipFile(inFile, 'r') as zipObj:
#     zipObj.extractall(tmpFolder)
#     for name in zipObj.namelist():
#         fullPath = os.path.join(tmpFolder, name)
#         # print(fullPath)
#         listOfFileNames.append(fullPath)


# # parse conversation file
# chatFile = open(os.path.join(tmpFolder, '_chat.txt'), encoding="utf8")
# lines = chatFile.readlines()
# for line in lines:
#     # print(line)
#     cl = ChatLine(line)
#     chatlines.append(cl)

# chatFile.close()


# # create export folder
# shutil.rmtree(outFolder)
# os.mkdir(outFolder)


# # copy files to export folder
# shutil.copyfile(os.path.join(templateFolder, 'style.css'), os.path.join(outFolder, 'style.css'))
# shutil.copytree(os.path.join(templateFolder, 'js'), os.path.join(outFolder, 'js'))
# shutil.copytree(os.path.join(templateFolder, 'css'), os.path.join(outFolder, 'css'))
# shutil.copytree(os.path.join(templateFolder, 'img'), os.path.join(outFolder, 'img'))

# # copy chat files to export folder
# shutil.copytree(tmpFolder, os.path.join(outFolder, 'attach'))


# # generate html
# conversationHTML = ''
# for cl in chatlines:
#     hg = HtmlGenerator(cl)
#     isSender = (userName == cl.user) 
#     if hg.type == LineType.VIDEO:
#         print('Generating thumb from', hg.getMessage())
#         hg.generateVideoThumbnail(
#             os.path.join(tmpFolder, hg.getMessage()), 
#             os.path.join(outFolder, 'img', hg.getMessage().replace('mp4', 'png'))
#         )
#     if hg.type == LineType.UNDEFINED:
#         print('Unable parser', cl.line)

#     conversationHTML += hg.html(isSender)

# # write file
# templatefile = open(os.path.join('template', 'index.html'), encoding="utf8")
# html = ''.join(templatefile.readlines()).replace('{conversation}', conversationHTML).replace('{username}', userName)
# # print(html)


# # save conversation on index file
# exportFile = open(os.path.join(outFolder, 'index.html'), 'w', encoding="utf8")
# exportFile.write(html)


# # open generated conversation on browser
# webbrowser.open(os.path.join(outFolder, 'index.html'))


# # remove temp folder
# shutil.rmtree(tmpFolder)