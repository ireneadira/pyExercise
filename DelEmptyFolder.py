import os

def delNullFile(path):
    for i,j,k in os.walk(path):
        for sonpath in j:
            if os.listdir(i + '/' + sonpath):
                # print('not dir ' + i + '/' + sonpath)
                pass
            else:
                print('delete dir ' + i + '/' + sonpath)
                os.rmdir(i + '/' + sonpath)

if __name__ == '__main__':
    delNullFile('F:/testDir_630')