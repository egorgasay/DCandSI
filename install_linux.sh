exists=$(command -v python3.10)
length1=${#exists}
exists=$(command -v py)
length2=${#exists}

if [[ $"length1" -lt 0 ]] && [[ $"length2" -lt 0 ]]; then
    echo 'Please, install Python3.10 and come back'
else
    echo 'Choose:'
    echo '1 Ubuntu'
    echo '2 Debian'
    echo '3 Other'
    read x
    if [[ "$x"=='1' ]]; then
        sudo apt update && sudo apt upgrade -y
        apt-get install unixodbc-dev -y
        apt-get install libpq-dev -y
        python3.10 -m pip install -r requirements.txt
    elif [[ "$x"=='1' ]]; then
        sudo apt-get update && sudo apt-get dist-upgrade -y
        apt-get install unixodbc-dev -y
        apt-get install libpq-dev -y
        python3.10 -m pip install -r requirements.txt
    else
        echo 'We can not install packages in your system automatically'
        echo 'Please, install it manualy'
        echo 'Packages: unixodbc-dev, libpq-dev'
        echo 'After installation: python3.10 -m pip install -r requirements.txt'
    fi
fi
