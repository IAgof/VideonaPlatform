# VideonaPlatform

Code repository for Videona social video platform at http://videona.com

For provisioning environment a stack of vagrant+ansible+docker+docker-compose is used

To create dev environment run vagrant up

If you want to use LXC containers for host machine, first you need to install the vagrant plugin and later specify lxc 
provider on vagrant up:

vagrant plugin install vagrant-lxc
vagrant up --provider=lxc