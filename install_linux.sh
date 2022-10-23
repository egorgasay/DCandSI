exists=$(command -v python3.10)
length1=${#exists}
exists=$(command -v py)
length2=${#exists}

if [[ $"length1" -lt 1 ]] && [[ $"length2" -lt 1 ]]
then
    echo 'Please, install Python3.10 and come back'
else
    echo 'Choose:'
    echo '1 Ubuntu'
    echo '2 Debian'
    echo '3 Other'
    read x
    if [[ $x -eq 1 ]]
    then
        echo '1 Ubuntu'
        sudo apt update && sudo apt upgrade -y
    elif [[ $x -eq 2 ]]
    then
        echo '2 Debian'
        sudo apt-get update && sudo apt-get dist-upgrade -y
        
    else
        echo 'We can not install packages in your system automatically'
        echo 'Please, install it manualy'
        echo 'Packages: unixodbc-dev, libpq-dev, docker'
        echo 'After installation: bash run_linux.sh'
	exit
    fi
    apt-get install unixodbc-dev -y
    apt-get install libpq-dev -y
    apt-get install docker -y
    python3.10 -m pip install -r requirements.txt
    docker build . -t dcsi
fi
