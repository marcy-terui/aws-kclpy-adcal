#
# Cookbook Name:: kcl
# Recipe:: default
#
# Copyright 2014, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

include_recipe 'python::default'
include_recipe 'supervisord::default'

package "java-1.8.0-openjdk"
python_pip "amazon_kclpy"

directory "/root/.aws" do
  owner "root"
  group "root"
  mode "0755"
end

file "/root/.aws/credentials" do
  owner "root"
  group "root"
  mode "0644"
  content <<-EOH
[default]
aws_access_key_id = #{node['aws_access_key']}
aws_secret_access_key = #{node['aws_secret_key']}
EOH
end

template "/etc/supervisord.conf" do
  cookbook "supervisord"
  source "supervisord.conf.erb"
  owner "root"
  group "root"
  mode "0644"
  variables({
     :name => "kcl",
     :command => "exec $(/usr/local/bin/amazon_kclpy_helper.py --print_command --java /usr/bin/java --properties /vagrant/kcl/kcl.properties)"
    })
  notifies :restart, "service[supervisord]"
end
