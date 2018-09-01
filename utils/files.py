from os.path import dirname, join, isfile

# Constants
PROJECT_ROOT_DIRECTORY = dirname(dirname(__file__))
DUMP_FILE_SUFFIX = "_dump.csv"

def getFullPath(*path):
    return join(PROJECT_ROOT_DIRECTORY, *path)

def getUserLastDumpFilePath(userId):
    return getFullPath('resources', 'dump_files', "{0}{1}".format(userId, DUMP_FILE_SUFFIX))

def writeToCsvFile(userId, headers, rows):
    target = open(getUserLastDumpFilePath(userId),'w+')
    target.truncate()

    # #dump same data to file without format
    rows[0] = headers
    for i in range(len(rows)):
        value = ', '.join([ rows[i][index] for index in range(len(rows[i])) ])                    
        target.write(value + "\n")

    target.close()
