#!/bin/bash


if [ `whoami` != "root" ];
then
	echo "The script can be run with root privilege only."
	exit -1
fi

dist_id=`cat /etc/lsb-release | grep DISTRIB_ID | awk -F= '{print $2}'`
dist_ver=`cat /etc/lsb-release | grep DISTRIB_RELEASE | awk -F= '{print $2}'`
if [[ $dist_id != "Ubuntu" ]] && [[ $dist_ver != "14.04" ]];
then
	echo "FNAT system supports Ubuntu 14.04 only."
	exit -2
fi

if [ $# != 1 ];
then
	echo "Bad syntax."
	echo ""
	echo "    fnat_deploy.sh fnat_sourcecode_folder."
	echo ""
	exit -3
fi

echo "Start to deploy FNAT system..."

echo "Install system dependencies..."
apt-get -y install apache2 php5 libapache2-mod-php5 mysql-server mysql-client php5-mysql git-core python-nose python-pip 
pip install uiautomator

echo "Download FNAT source code..."
git clone https://github.com/lizhouw/FNAT $1

echo "Configure apache server..."
cp $1/www/* /var/www/html/
rm -f /var/www/html/index.html
service apache2 restart

echo ""
echo ""
echo "=======================  NOTICE  ================================"
echo "Please run command 'mysql -u root -p' to activate mysql client"
echo "and run 'source $1/create_fnat_base.sql' to create FNAT database."
echo "After that, the FNAT system is deployed successfully."



