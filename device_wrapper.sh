#!/bin/bash

# 22.11.2018
# Wrapper zum Starten von SMC100.py 

# Exportieren der Variable TANGO_HOST fuer die Bash-Shell

#export TANGO_HOST=angstrom.hhg.lab:10000
export TANGO_HOST=10.6.16.78:10000

#TANGOHOST=angstrom.hhg.lab
TANGOHOST=10.6.16.78

#Umleiten der Ausgabe in eine Log-Datei
exec &>> /home/pi/Tango_Devices/SMC100/device.log

echo "---------------------------"
echo $(date)
echo "Tangohost: " $TANGOHOST

# Warten bis der Tangohost sich meldet
while ! timeout 0.2 ping -c 1 -n $TANGOHOST &> /dev/null
do
  :
# mache nix  
done

echo "ping Tangohost successful!"
echo "starting SMC100 device"

# Fork/exec
(
  exec /usr/bin/python /home/pi/Tango_Devices/SMC100/SMC100.py hhg &
) 
&>> /home/pi/Tango_Devices/SMC100/device.log 

sleep 1

# Testen, ob der PySerialDS- Prozess laeuft, 
# dann das Achsen-Device starten


if pgrep -fl "SMC100.py";
then 
(
  echo "starting SMC100 successful!"
)
fi

exit 0
