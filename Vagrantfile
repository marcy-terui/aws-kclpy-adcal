# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "chef/centos-6.6"

  config.omnibus.chef_version = "12.0.0"

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provision "chef_solo" do |chef|
    chef.cookbooks_path = ["cookbooks", "site-cookbooks"]
  end

  config.vm.define :stream do |node|
    node.vm.network :private_network, ip:"192.168.11.11", virtualbox__intnet: "adcal"
    node.vm.network :forwarded_port, id: "ssh", guest: 22, host: 2211
    # node.vm.synced_folder "stream/", "/stream"
    node.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["cookbooks", "site-cookbooks"]
      chef.add_recipe "stream"
      chef.json = {
        "aws_access_key" => ENV['AWS_ACCESS_KEY_ID'],
        "aws_secret_key" => ENV['AWS_SECRET_ACCESS_KEY'],
        "python" => {
          "install_method" => "source",
          "prefix_dir"     => "/usr/local"
        }
      }
    end
  end

  config.vm.define :kcl do |node|
    node.vm.network :private_network, ip:"192.168.11.22", virtualbox__intnet: "adcal"
    node.vm.network :forwarded_port, id: "ssh", guest: 22, host: 2222
    # node.vm.synced_folder "kcl/", "/kcl"
    node.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["cookbooks", "site-cookbooks"]
      chef.add_recipe "kcl"
      chef.json = {
        "aws_access_key" => ENV['AWS_ACCESS_KEY_ID'],
        "aws_secret_key" => ENV['AWS_SECRET_ACCESS_KEY'],
        "python" => {
          "install_method" => "source",
          "prefix_dir"     => "/usr/local"
        }
      }
    end
  end

  config.vm.define :graphite do |node|
    node.vm.network :private_network, ip:"192.168.11.33", virtualbox__intnet: "adcal"
    node.vm.network :forwarded_port, id: "ssh", guest: 22, host: 2233
    node.vm.network :forwarded_port, guest: 80, host: 8080
    # node.vm.synced_folder "graphite/", "/graphite"
    node.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["cookbooks", "site-cookbooks"]
      chef.add_recipe "graphite"
    end
  end
end
