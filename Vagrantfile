# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true

  config.vm.define "vagrant" do |vagrant|
      vagrant.vm.box = "geerlingguy/centos7"
      vagrant.vm.hostname = "vagrant"
      vagrant.vm.network "private_network", ip: "192.168.60.10"
      vagrant.hostmanager.aliases = %w(baunilha.test)
      vagrant.vm.synced_folder ".", "/opt/baunilha", create: true
  end

end
