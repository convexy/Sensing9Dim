# AE-LSM9DS1-I2C
sudo apt-get -y update
sudo apt-get -y dist-upgrade
sudo apt-get -y autoremove
sudo apt-get -y install i2c-tools
sudo apt-get -y install python3-smbus
sudo raspi-config
	3 Interface Options
		P5 I2C
			Yes

