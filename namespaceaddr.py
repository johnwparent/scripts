import re
import mmap
import os
import glob

class namespacer():
    def __init__(self, file_):
        self.open = "namespace kwiver {\nnamespace vital  {\nnamespace python {\n"
        self.close = "\n}\n}\n}\n"
        self.file_ = file_
        self.file = open(file_, "r+")
        self.mf = mmap.mmap(self.file.fileno(), 0, access=mmap.ACCESS_WRITE)
        self.mf.seek(0)

    def closer(self):
        self.mf.close()
        self.file.close()

    def get_last_include(self):
        all_inc = re.findall(b'#include .*\n',self.mf)
        return all_inc[-1]
    
    def is_done(self):
        namespace_ = re.findall(b'namespace kwiver {\nnamespace vital  {\nnamespace python {', self.mf)
        if namespace_:
            return True
        return False

    def insert_close_pos(self):
        # find position of eof, or endif, something to denote end of namespace
        all_if = re.findall(b'#endif\n',self.mf)
        if not all_if:
            #need eof instead
            self.closer()
            self.file = open(self.file_,"a")
            self.file.write(self.close)
        else:
            
            loc = self.mf.find(all_if[-1])
            self.mf.seek(loc-1, os.SEEK_CUR)
            rest_of_file = self.mf[loc-1:]
            self.mf.resize(self.mf.size()+len(self.close))
            self.mf.flush()
            self.mf.write(str.encode(self.close)+rest_of_file)
            self.mf.flush()

        
    def insert_open_pos(self):
        last_inc = self.get_last_include()
        loc = self.mf.find(last_inc)
        self.mf.seek(loc+len(last_inc)+1, os.SEEK_CUR)
        rest_of_file = self.mf[loc+len(last_inc)+1:]
        self.mf.resize(self.mf.size()+len(self.open))
        self.mf.write(str.encode(self.open)+rest_of_file)
        self.mf.flush()
        self.mf.seek(0)

    def add_namespace(self):
        if self.is_done():
            print("File already has namespace: "+self.file_ )
            return
        self.insert_open_pos()
        self.insert_close_pos()
        self.closer()

def main():
    # os.chdir(os.getcwd())
    all_cxx = glob.glob("*.cxx")
    all_h = glob.glob("*.h")
    all_txx = glob.glob("*.txx")
    for filename in all_cxx:
        namespacer(filename).add_namespace()
    for filename in all_h:
        namespacer(filename).add_namespace()
    for filename in all_txx:
        namespacer(filename).add_namespace()
    


if __name__ == '__main__':
    main()
