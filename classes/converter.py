import shutil, os 
from pathlib import Path
from zipfile import ZipFile
from classes.chatline import ChatLine
from classes.htmlgenerator import HtmlGenerator, LineType

class Converter(object):

    tmp = os.path.join(Path().absolute(), 'temp')
    templateFolder = os.path.join(Path().absolute(), 'template')
    initialInfoMessage = 'Los mensajes y las llamadas están cifrados de extremo a extremo. Nadie fuera de este chat, ni siquiera WhatsApp, puede leerlos ni escucharlos. Toca para obtener más información.'

    def __init__(self, inFile, chatLines, senderName, outPath):
        self.inFile = inFile
        self.chatLines = chatLines
        self.senderName = senderName
        self.outPath = outPath

    def parse(self):
        os.mkdir(self.tmp)
        with ZipFile(self.inFile, 'r') as zipObj:
            zipObj.extractall(self.tmp)

    def export(self):
        print(f'Exporting {len(self.chatLines)} lines in {self.outPath}')

        # copy files to export folder
        shutil.copyfile(os.path.join(self.templateFolder, 'style.css'), os.path.join(self.outPath, 'style.css'))
        shutil.copytree(os.path.join(self.templateFolder, 'js'), os.path.join(self.outPath, 'js'))
        shutil.copytree(os.path.join(self.templateFolder, 'css'), os.path.join(self.outPath, 'css'))
        shutil.copytree(os.path.join(self.templateFolder, 'img'), os.path.join(self.outPath, 'img'))

        # copy chat files to export folder
        shutil.copytree(self.tmp, os.path.join(self.outPath, 'attach'))

        # generate html
        hg = HtmlGenerator()
        conversationHTML = hg.generateInfoMessage(self.initialInfoMessage)
        # conversationHTML = ''
        currentUser = ''
        currentDay = ''
        for cl in self.chatLines:
            hg = HtmlGenerator(cl)
            if hg.type == LineType.UNDEFINED:
                print('Unable parser', cl.line)
                continue

            isSender = (self.senderName == cl.user) 
            firstMessage = (cl.user != currentUser)
            sameDay = (cl.getDay() != currentDay)
            if cl.user != currentUser:
                currentUser = cl.user
            
            if cl.getDay() != currentDay:
                currentDay = cl.getDay()

            if sameDay:
                conversationHTML += hg.generateInfoMessage(currentDay)
            
            if hg.type == LineType.VIDEO:
                print('Generating thumb from', hg.getMessage())
                hg.generateVideoThumbnail(
                    os.path.join(self.tmp, hg.getMessage()), 
                    os.path.join(self.outPath, 'img', hg.getMessage().replace('mp4', 'png'))
                )
            
            conversationHTML += hg.html(isSender, firstMessage)

        # write file
        templatefile = open(os.path.join('template', 'index.html'), encoding="utf8")
        html = ''.join(templatefile.readlines()).replace('{conversation}', conversationHTML).replace('{username}', self.senderName)

        # save conversation on index file
        exportFile = open(os.path.join(self.outPath, 'index.html'), 'w', encoding="utf8")
        exportFile.write(html)

        # remove temp folder
        shutil.rmtree(self.tmp)
        return True

    def getRandomColor(self):
        rgb = ""
        for _ in "RGB":
            i = random.randrange(0, 2**8)
            rgb += i.to_bytes(1, "big").hex()
        return rgb