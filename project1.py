from pathlib import Path
import shutil
def error() -> None:
    '''print error'''
    print('ERROR')
        
def print_path(pathlist:[])->None:
    '''print element from given list'''
    for element in pathlist:
        print(element)


def read_command1()->(Path):
    '''read the first input to find whether return file path from only directory or
    both directory and subdirectory
     '''
    while True:
        line1= input()
        start = line1[0]
        path = Path(line1[2:])
        if not path.is_dir() or (start != 'D' and start != 'R')or len(line1)<2:
            error()
            continue
        return (start,path)                  
        
def get_paths_forD(folder:Path)->list[Path]:
    '''This function returns a list of file path from a given directory but not
    consider the file in the subdirectory if it exists
    folder:the direcory path where to get file path
    return: a list of file path from the directory but not subdirectory
    
    '''
    paths_of_files=[]
    for path in Path(folder).iterdir():
        if path.is_file():#check the path only from directory but not subdirectory
           paths_of_files.append(path)
    for i in paths_of_files:
        print(i)
    return paths_of_files
def get_paths_forR(folder:Path)->[Path]:
    '''This function returns a list of file path from a given directory and its
    subdirectory
    folder:the direcory path where to get file path
    return: a list of file path from both the direcory and its subdirectory


    '''
    paths_of_files=[]
    subdir=[]#a list contains the path of subdirectory
    good_file=[]
    isfolder=False
    for path in Path(folder).iterdir():
        if path.is_file():
            paths_of_files.append(path)#add normal file
        else:
            subdir.append(path)#save the subdir path for next processing
            isfolder=True
    for i in paths_of_files:
        print(i)
    
    if isfolder:
        for path in subdir:
            paths_of_files.append(get_paths_forR(path))#use recursion to get the path from subdir
        isfolder=False
    for i in paths_of_files:
        if type(i)==list:
            for x in i:
                good_file.append(x)#move the path from dir and subdir into one list
        else:
            good_file.append(i)
    return good_file
      
        


    


def narrow_search(letter: str, request: str or int or None, paths: list[Path]) -> list[Path]:
    '''This function search interesting files from the list of file path in previous step(get_paths_forD or get_paths_forR)
    and return a list contains the paths of the interesting files
    letter: the first letter show what kind of file path should be search and return
    request:the request context that files will be evaluated
    paths:the list of file path from the previous step
    '''
    if letter == 'A':
        return paths
    interesting_files = []
    for file in paths:
        if letter == 'N' and file.name == request:
            interesting_files.append(file)#add file that has same name with request to list
        elif letter == 'E' and (file.suffix == request or file.suffix[1:] == request):
            interesting_files.append(file)#add file that has same extension with request to list
        elif letter == '<' and file.stat().st_size < int(request):  
            interesting_files.append(file)#add file that has smaller size than request to list
        elif letter == '>' and file.stat().st_size > int(request):  
            interesting_files.append(file)#add file that has larger size than request to list
        elif letter == 'T':  
            try:
                contents = file.read_text()
                if request in contents:
                    interesting_files.append(file)#add file that contains text same as request to list
                    continue
            except UnicodeDecodeError: #If we try to read a file that is not a text file 
                continue
    return interesting_files



def take_action(letter:str,files:list[Path])->None:
    '''This function take action on interesting files searched in the previous 
    step
    letter:the first letter show what kind of action to take on the interesting files 
    files:list of interesting file from the previous step
    '''

    for file in files:
        if letter=='T':
            file.touch(exist_ok=True)#change the modify time to now
        elif letter=='D':
            dup_file=file.parent/Path(file.name+'.dup')#make a copy of the file and end with .dup   
            shutil.copyfile(file,dup_file)
        elif letter=='F':
            try:
                with file.open() as openfile:
                    print(openfile.readline(),end='')#read and print the first line of file or print NOT TEXT if it is not textfile
            except UnicodeDecodeError:
                print('NOT TEXT')
                        

def read_command2()->(str,any):
    '''read the second input to see what kind of file to search for'''
    while True:
        line2=input()
        start=line2[0]
        if start=='A'and len(line2.strip())==1:
            return ('A',None)
        elif  start=='N' or start=='E' or start=='T':
            if len(line2[2:])>0:
                return (start,line2[2:])
        elif start=='<'or start=='>':
            if len(line2[2:])>0 and line2[2:].isdigit():
                return (start,line2[2:])
        error()

def read_command3()->str:
    '''read the third input to see what kind of action to take on interesting file'''
    while True:
        line3=input()
        start=line3[0]
        if start=='F' or start=='D' or start=='T' and len(line3.strip())==1:
            return start
        else:
            error()


            
def run()->None:
    start,path=read_command1()
    if start=='D':
        good_file=get_paths_forD(path)
    if start=='R':
        good_file=get_paths_forR(path)
    
    start1,request=read_command2()
    interesting_files=narrow_search(start1,request,good_file)
    if len(interesting_files)==0:
        return
    print_path(interesting_files)
    start2=read_command3()
    take_action(start2,interesting_files)
if __name__ == '__main__':
    run()
