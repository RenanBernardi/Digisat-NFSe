@echo off
echo Dando permissao total para usuario Todos na pasta C:\DigiSat
cacls c:\DigiSat /E /T /C /G "Todos":F
echo Dando permissao total para usuario Todos na pasta C:\Program Files\TecnoSpeed
cacls "C:\Program Files\TecnoSpeed" /E /T /C /G "Todos":F
echo.
echo.
echo Verifique se deu todos arquivos como "arquivos processado" significa que as permissoes foram alteradas com sucesso. Pressione qualquer tecla para continuar.
pause