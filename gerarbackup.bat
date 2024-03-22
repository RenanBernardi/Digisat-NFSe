@echo Parando o MongoDB e Sincronizador
net stop MongoDBDigisat
net stop SincronizadorDigisat
@echo Iniciando Backup do Banco de dados
set data=%date:~0,2%-%date:~3,2%-%date:~6,10%-%time:~0,2%-%time:~3,2%
xcopy  C:\DigiSat\SuiteG6\Dados\*.* "C:\DigiSat\SuiteG6\DadosBkp_%data%\"/E
@echo Backup Gerado com Sucesso! em C:\DigiSat\SuiteG6\DadosBkp_DD_MM_AAA_HH_MM
@echo Iniciar o MongoDB e Sincronizador
net start MongoDBDigisat
net start SincronizadorDigisat
PAUSE