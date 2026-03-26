

echo off
cls
echo          Hola!
echo Bienvenido a este script
echo.
echo ************************************ 
echo Hecho por Luis Reyes
echo ************************************ 
echo.

echo Primero buscaremos sus datos de red
ipconfig /all > Reporte-datos-red.txt
echo Reporte creado exitosamente
echo.

echo Ahora probaremos su conectividad a la red 
ping 8.8.8.8 > Reporte-conectividad-red.txt
echo Reporte creado exitosamente
echo.

echo Seguido probaremos su DNS
nslookup www.youtube.com > Reporte-conectividad-DNS.txt
echo Reporte creado exitosamente
echo.

echo Seguido buscaremos sus conexiones activas
netstat -ano > Reporte-conexiones-activas.txt
echo Reporte creado exitosamente
echo.

echo Ahora buscaremos las direcciones ip en tu red local
arp -a > Reporte-ip-locales.txt
echo Reporte creado exitosamente
echo.

echo Seguiremos buscando los programas que usan cada puerto
arp -b > Reporte-uso-puertos.txt
echo Reporte creado exitosamente
echo.