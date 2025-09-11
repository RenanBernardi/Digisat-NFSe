net stop MongoDBDigisat
net stop SincronizadorDigisat
cd/
cd digisat
cd suiteg6
cd mongodb
cd bin
mongod.exe --dbpath c:\digisat\suiteg6\dados\ --repair
net start MongoDBDigisat
net start SincronizadorDigisat
