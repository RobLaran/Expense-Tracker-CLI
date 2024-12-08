import os
import shutil

class FileOrganizer():
    def __init__(self):
        pass

    def current_dir(self):
        return os.getcwd()
    
    def list(self):
        entries = os.listdir(self.current_dir()) 
        return entries
        
    def checkFile(self, file):
        return os.path.isfile(file)

    
    def change_dir(self, path):
        os.chdir(path)
        
    def return_(self): 
        self.change_dir('..')
        return self.current_dir()

    def delete_file(self, filename):
        os.remove(filename)
        
    def delete_dir(self, dirname):
        os.rmdir(dirname)
        
    def delete_item(self, filename):
        if '.' in filename:
            os.remove(filename)
        else:
            shutil.rmtree(filename)
        
    def create_dir(self, dirname):
        os.mkdir(dirname)
    
    def create_file(self, filename):
        os.system(f'type nul > {filename}')
        
    def create_item(self, filename):
        if '.' in filename:
            os.system(f'type nul > {filename}')
        else:
            os.mkdir(filename)
        
    def move(self, file, path):
        for item in file.split(" "):
            shutil.move(item, path)
            
    def copy(self, file):
        if '.' in file:
            name = file.split('.')[0]
            ext = file.split('.')[1]
            shutil.copy2(file, f'./{name}(2).{ext}')
        else:
            shutil.copytree(file,f'./{file}(2)')
        
    def rename(self, filename, newname):
        if '.' in filename:
            ext = filename.split('.')[1]
            file = filename.split('.')[0]   
            print(file+ext)         
            os.rename((f'{filename}'), (f'{newname}.{ext}'))
        
    def file_exists(self, filename):
        return os.path.exists(filename)
    
    def search(self, searched_term):
        for root, dirs, files in os.walk(self.current_dir()):
            for file in files:
              if searched_term.lower() in file.lower():
                print("Found at " + os.path.abspath(file))

    def textpreview(self, textfile):
        try:
            if os.path.exists(textfile):
                with open(textfile) as file:
                    print(file.read(100))
        except:
            print('cannot read file')
            
    def get_abspath(self, file):
        return os.path.abspath(file)

    def organize(self):
        text_ext = ['.txt', '.doc', '.docx', '.pdf', '.wps']
        video_ext = ['.avi', '.mp4', '.mov', '.filv']
        audio_ext = ['.wav', '.mp3', '.m4a']
        image_ext = ['.jpg', '.jpeg', '.gif', '.png', '.webp', '.svg']

        files = self.list()
                
        for file in files:
            if os.path.splitext(file)[1] in text_ext:
                if not self.file_exists('Texts'): 
                    self.create_dir('Texts')
                    self.move(file, 'Texts')
                else:
                    self.move(file, 'Texts')
                print(f'{file} moved to Texts')
            elif os.path.splitext(file)[1] in video_ext:
                if not self.file_exists('Videos'): 
                    self.create_dir('Videos')
                    self.move(file, 'Videos')
                else:
                    self.move(file, 'Videos')
                print(f'{file} moved to Videos')
            elif os.path.splitext(file)[1] in audio_ext:
                if not self.file_exists('Audios'): 
                    self.create_dir('Audios')
                    self.move(file, 'Audios')
                else:
                    self.move(file, 'Audios')
                print(f'{file} moved to Audios')
            elif os.path.splitext(file)[1] in image_ext:
                if not self.file_exists('Images'): 
                    self.create_dir('Images')
                    self.move(file, 'Images')
                else:
                    self.move(file, 'Images')
                print(f'{file} moved to Images')
        
    def open(self):
        response = None    

        while response != 'R':
            response = input("FILE_ORG:\\\\" + self.current_dir() + "$ ").upper().strip()
        
            if response == 'LS':  
                self.list()

            elif response == 'PRVW':
                textfile = input('text file: ')
                self.textpreview(textfile)
                
            elif response == 'CD':
                path = input('dir: ')
                self.change_dir(path)
                
            elif response == 'RM':
                file = input('filename: ')
                self.delete_file(file)

            elif response == 'RN':
                filename = input('filename: ')                
                newname = input('new name: ')
                self.rename(filename, newname)
                
            elif response == 'RMDIR':
                file = input('filename: ')
                self.delete_dir(file)
                
            elif response == 'MKF':
                file = input('filename: ')
                self.create_file(file)
                
            elif response == 'MKDIR':
                file = input('filename: ')
                self.create_dir(file)
                
            elif response == 'MV':
                file = input('filename: ')    
                path = input('path: ')
                self.move(file,path)
                
            elif response == 'CP':
                file = input('filename: ')
                tocopy = input('path: ')
                self.copy(file, tocopy)
                
            elif response == 'SRCH':
                searched = input('search: ')
                self.search(searched)
                
            elif response == 'ORG':
                self.organize()
                                
            elif response == 'EXST':
                filename = input('filename: ')
                print(self.file_exists(filename))
                
            elif response == 'SIZE':
                filename = input('filename: ')
                file_stat = os.stat(filename)
                print(file_stat.st_size)