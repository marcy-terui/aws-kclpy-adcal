#
# Cookbook Name:: supervisord
# Recipe:: default
#
# Copyright 2014, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

if node['platform'] == "amazon" then
  releasever = "6"
else
  releasever = "$releasever"
end

yum_repository "epel" do
  description "epel repo"
  baseurl "https://dl.fedoraproject.org/pub/epel/#{releasever}/$basearch/"
  gpgkey  "http://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-#{releasever}"
  enabled true
end

package "supervisor"

service "supervisord" do
  supports :status => true, :restart => true, :reload => true
  action [:enable, :start]
end
