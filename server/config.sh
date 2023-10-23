# Install docker 
GO to https://docs.docker.com/desktop/

# Create a Docker network named "mm-network"
docker network create mm-network

# Start a MySQL container for Master A on the "mm-network" with specified environment variables and port mapping
docker run -d --name mysql-masterA --network mm-network -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=amazon -e MYSQL_USER=master -e MYSQL_PASSWORD=masterroot -p 3306:3306 mysql:latest

# Start a MySQL container for Master B on the "mm-network" with specified environment variables and port mapping
docker run -d --name mysql-masterB --network mm-network -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=amazon -e MYSQL_USER=master -e MYSQL_PASSWORD=masterroot -p 3307:3306 mysql:latest

# Access the MySQL container for Master A and configure it
docker exec -it mysql-masterA mysql -uroot -proot

# Configure Master A
# Set the server ID for Master A to 1
SET GLOBAL server_id = 1123;
# Modify the authentication method for 'root' and 'master' users
ALTER USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'root';
ALTER USER 'master'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'masterroot';
GRANT REPLICATION SLAVE ON *.* TO 'root'@'%';
GRANT REPLICATION SLAVE ON *.* TO 'master'@'%';
# Flush privileges to apply the changes
FLUSH PRIVILEGES;
# Show the master status
show master status\G
# Exit the MySQL prompt
exit

# Access the MySQL container for Master B and configure it
docker exec -it mysql-masterB mysql -uroot -proot

# Configure Master B
# Set the server ID for Master B to 2
SET GLOBAL server_id = 4561;
# Modify the authentication method for 'root' and 'master' users
ALTER USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'root';
ALTER USER 'master'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'masterroot';
GRANT REPLICATION SLAVE ON *.* TO 'root'@'%';
GRANT REPLICATION SLAVE ON *.* TO 'master'@'%';
# Flush privileges to apply the changes

FLUSH PRIVILEGES;
# Show the master status for Master B
show master status\G
# Exit the MySQL prompt
exit

# Configure Master A to replicate from Master B
# Access the MySQL container for Master B and configure it
docker exec -it mysql-masterA mysql -uroot -proot

# Show the master status for Master A
show master status\G;
# Stop the slave
STOP SLAVE;
# Change the replication master to Master B
CHANGE MASTER TO
    MASTER_HOST='mysql-masterB',
    MASTER_PORT=3306,
    MASTER_USER='master',
    MASTER_PASSWORD='masterroot',
    MASTER_LOG_FILE='binlog.000004',  # Use the correct file and position from Master B
    MASTER_LOG_POS=1332;               # Use the correct position from Master B
# Start the slave
START SLAVE;
# Show the slave status
SHOW SLAVE STATUS\G;

# Exit

# Configure Master B to replicate from Master A
# Access the MySQL container for Master B and configure it
docker exec -it mysql-masterB mysql -uroot -proot
# Show the master status for Master B
show master status\G;
# Stop the slave
STOP SLAVE;
# Change the replication master to Master A
CHANGE MASTER TO
    MASTER_HOST='mysql-masterA',
    MASTER_PORT=3306,
    MASTER_USER='master',
    MASTER_PASSWORD='masterroot',
    MASTER_LOG_FILE='binlog.000004',  # Use the correct file and position from Master A
    MASTER_LOG_POS=1332;               # Use the correct position from Master A
# Start the slave
START SLAVE;
# Show the slave status
show slave status\G;
# Exit
