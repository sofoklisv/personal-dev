import os
rootDir = '.\\Snapshot-Feature'

# pass Project Alias
ProjectAlias = 'Az'

# Get the Feature name from the folder label
for rootPath, dirList, fileList in os.walk(rootDir):
	FeatureName = rootPath[2:]
	break
print('Project Alias: {} \nReason For Deployment: {}\n'.format(ProjectAlias,FeatureName))

# Get a list of all the Server names
for rootPath, dirList, fileList in os.walk(rootDir):
	if rootPath.endswith('Server'):
		ServersNameList = dirList

# Get a list of all Database names
DBNameList = []
for rootPath, dirList, fileList in os.walk(rootDir):
	if rootPath.endswith('Database'):
		for DBName in dirList:
			DBNameList.append(DBName)

print('Servers: {}'.format(ServersNameList))
print('Databases: {}\n'.format(DBNameList))

# Get a list of all filepaths
FilepathList = []
for rootPath, dirList, fileList in os.walk(rootDir):
	for name in fileList:
		if name.endswith('.sql'):
			filepath = os.path.join(rootPath,name)
			FilepathList.append(filepath)

print('The {} directory contains {} sql files'.format(FeatureName,len(FilepathList)))

# Now for each of the servers and databases, we want to create
# a separate SqlDeploymentScript, which will reference objects
# in the correct order: Schemas, Tables, Indexes, Views, StorProcs
x=1
for server in ServersNameList:
	servername = '\\{}'.format(server)

	for db in DBNameList:
		dbname = '\\{}'.format(db)
		# Assign the production values to dev servers and dbs
		if server == 'bistakgendbdev':
			NewServerName = 'bistakgendblive'
		if server == 'UK-LD9-BA2':
			NewServerName = 'UK-LD9-BA1'

		for item in FilepathList:
			if item.find(servername) > -1 and item.find(dbname) > -1:
				SqlDeploymentFile = open("Az-SqlDeploymentScript-{}-{}-{}.sql".format(NewServerName,db,FeatureName),"a+")
				print(x)
				print('Server: {}\nDatabase: {}\nFile: {}\n'.format(servername,dbname,item))
				fread = open(item, "r")
				sqlcode = fread.read()

				SqlDeploymentFile.write('-- {} \n{}\n'.format(item,sqlcode)) 

				x+=1
SqlDeploymentFile.close()