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

echo "Start to deploy FNAT system..."

echo "Install system dependencies..."
apt-get -y install apache2 php5 libapache2-mod-php5 mysql-server mysql-client python-mysqldb php5-mysql git-core python-nose python-pip 
pip install uiautomator
pip install nose-testconfig

echo "Configure apache server..."
cp $1/www/* /var/www/html/
cp $1/flukenetworks-logo.png /usr/share/apache2/icons/
rm -f /var/www/html/index.html
mkdir /var/www/html/fnat_log
chmod 777 fnat_log
service apache2 restart

echo ""
echo ""
echo "=======================  NOTICE  ================================"
echo "Please run command 'mysql -u root -p' to activate mysql client"
echo "and run 'source $1/create_fnat_base.sql' to create FNAT database."
echo "After that, the FNAT system is deployed successfully."



