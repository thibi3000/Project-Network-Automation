# -*- mode: ruby -*-
# vi: set ft=ruby :

# Edit these
hostname            = "vagrant.dev"
server_ip           = "192.168.33.10"
mysql_root_password = "root"

Vagrant.configure(2) do |config|
  # OS to install on VM
  config.vm.box = "ubuntu/trusty64"

  # Map local port 8080 to VM port 80
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # IP to access VM
  config.vm.network "private_network", ip: server_ip

  # Set up default hostname
  config.vm.hostname = hostname

  # Sync current directory to "/var/www" directory on the VM
  # also set sync implementation to NFS for better performance,
  # if running on Windows or a non-NFS supported system just
  # remove the last "," and the next 3 lines
  config.vm.synced_folder ".", "/var/www",
    id: "core",
    :nfs => true,
    :mount_options => ['nolock,vers=3,udp,noatime']

  config.vm.provider "virtualbox" do |vb|
    # Set VM name
    vb.name = "Vagrant Dev"

    # Customize the amount of memory on the VM
    vb.memory = "1024"

    # Customize # of CPUs
    vb.cpus = 1

    # Set the timesync threshold to 10 seconds, instead of the default 20 minutes.
    # If the clock gets more than 15 minutes out of sync (due to your laptop going
    # to sleep for instance) then some 3rd party services will reject requests.
    vb.customize ["guestproperty", "set", :id, "/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold", 10000]

    # Prevent VMs running on Ubuntu to lose internet connection
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  # Update repository
  config.vm.provision "shell", inline: "sudo apt-get update"

  # Install base utilities
  config.vm.provision "shell", inline: "sudo apt-get install -qq curl unzip git-core ack-grep software-properties-common build-essential"

  # Install basic LAMP stack
  # Apache
  config.vm.provision "shell", inline: "sudo apt-get install -qq apache2"
  # Enable mod_rewrite
  config.vm.provision "shell", inline: "sudo a2enmod rewrite"
  # Restart Apache
  config.vm.provision "shell", inline: "sudo service apache2 restart"

  # PHP
  config.vm.provision "shell", inline: "sudo apt-get install -qq php5 php5-mysql php5-curl php5-gd php5-gmp php5-mcrypt php5-intl"
  # Enable mcrypt
  config.vm.provision "shell", inline: "sudo php5enmod mcrypt"
  # Restart Apache
  config.vm.provision "shell", inline: "sudo service apache2 restart"

  # MySQL
  # Set username and password to 'root'
  config.vm.provision "shell", inline: "sudo debconf-set-selections <<< \"mysql-server mysql-server/root_password password #{mysql_root_password}\""
  config.vm.provision "shell", inline: "sudo debconf-set-selections <<< \"mysql-server mysql-server/root_password_again password #{mysql_root_password}\""

  # Install MySQL
  config.vm.provision "shell", inline: "sudo apt-get install -qq mysql-server"

  # Adding grant privileges to mysql root user from everywhere
  # http://stackoverflow.com/questions/7528967/how-to-grant-mysql-privileges-in-a-bash-script
  Q1  = "GRANT ALL ON *.* TO 'root'@'%' IDENTIFIED BY '#{mysql_root_password}' WITH GRANT OPTION;"
  Q2  = "FLUSH PRIVILEGES;"
  SQL = "#{Q1}#{Q2}"

  config.vm.provision "shell", inline: "mysql -uroot -p#{mysql_root_password} -e \"#{SQL}\""

end
