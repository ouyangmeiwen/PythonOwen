# install Damang database by script

## create dir and user

```bash
sudo groupadd -g 12349 dinstall
sudo useradd -u 12345 -g dinstall -m -d /home/dmdba -s /bin/bash dmdba
sudo passwd dmdba

sudo mkdir /opt/dmdbms
sudo chown dmdba:dinstall /opt/dmdbms
sudo chmod 775 /opt/dmdbms

mkdir /data/dmdata
sudo chown dmdba:dinstall /data/dmdata

```

## install

```bash
sudo mkdir /mnt/dm
sudo mount dm8_20250117_FTarm2000_kylin10_sp1_64.iso /mnt/dm
cd /mnt/dm
sudo su dmdba
./DMInstall.bin -i

exit
sudo /opt/dmdbms/script/root/root_installer.sh
```

## init

```bash
sudo su dmdba
cd  /opt/dmdbms/bin
export DM_PASSWD=Iv002161
./dminit db_name=DAMENG instance_name=DMSERVER port_num=5236 path=/data/dmdata SYSDBA_PWD=$DM_PASSWD SYSAUDITOR_PWD=$DM_PASSWD CASE_SENSITIVE=0 CHARSET=1

exit
cd /opt/dmdbms/script/root/
sudo ./dm_service_installer.sh -t dmserver -p DMSERVER -dm_ini /data/dmdata/DAMENG/dm.ini

sudo systemctl enable DmServiceDMSERVER.service
sudo systemctl start DmServiceDMSERVER.service
```

## create app user

```bash
cd /opt/dmdbms/bin
./disql SYSDBA/Iv002161
```

Execute SQL follow:

```sql
create tablespace "invengo" datafile 'invengo.dbf' size 64 CACHE = NORMAL;

create user "invengodba" identified by "Iv002161" 
    default tablespace "invengo" 
    default index tablespace "invengo";

grant "RESOURCE","PUBLIC","SOI" to "invengodba";
```

```bash
exit
```

## clear

```bash
sudo umount /mnt/dm
sudo rm -r /mnt/dm

```