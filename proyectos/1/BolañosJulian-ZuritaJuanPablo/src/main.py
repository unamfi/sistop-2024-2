from models import FiUnamFS

directory_path = 'D:/workspace/sistemasOp/sistop-2024-2/proyectos/1/FiUnamFS.img'

fiunamfs = FiUnamFS(path = directory_path, directory_entry_size = 64)
fiunamfs.showDetails()

files = fiunamfs.getFiles()
for file in files:
    print(file)