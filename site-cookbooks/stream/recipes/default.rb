#
# Cookbook Name:: stream
# Recipe:: default
#
# Copyright 2014, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

include_recipe 'python::default'
include_recipe 'supervisord::default'

python_pip "boto"
python_pip "tweepy"

file "/etc/boto.cfg" do
  owner "root"
  group "root"
  mode "0644"
  content <<-EOH
[Credentials]
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
     :name => "stream",
     :command => "/usr/local/bin/python /vagrant/stream/tw_stream_to_kinesis.py"
    })
  notifies :restart, "service[supervisord]"
end
