# ODK Connector
ODK Connector is a [cartoview](github.com/cartologic/cartoview) app to integrate [ODK](https://opendatakit.org/) with [cartoview](github.com/cartologic/cartoview) to enable you to view the location of your ODK surveys.

[Open Data Kit (ODK)](https://opendatakit.org) enables you to design and perform surveys from your mobile to learn more about ODK click [here](https://opendatakit.org/)

## Installation
#### Install [Cartoview](https://github.com/cartologic/cartoview)
#### Install ODK Aggregate
First you have to install ODK Aggregate server to upload and manage the surevys form, and also to manage the users who collect the data

ODK Aggregate will be deployed locally on a Tomcat server backed with PostgreSQL database server through the following steps:

1. Download ODK Aggregate installer for windows from [here](https://opendatakit.org/downloads/download-info/odk-aggregate-windows-installer-exe/)
2. Create PostGIS database
3. Double-click the installer file and go through the installation process to generate the WAR file for your server instance.
4. In Choose Platform dialog select PostgreSQL
5. Proceed till you complete the installation process.
3. Go to the installation directory and copy the generated WAR file to tomcat (webapps directory) that installed with Cartoview where located under ``` <CartoView Installation Directory>\tomcat 8 ```
4. Now ODK Aggregate will be ready on ``` http://<Tomcat Server URL>/<ODK Aggregate Instance Name> ```

#### Install ODK Connector
1. Download the ODK Connector app package form [here](http://cartologic.com/cartoview2/apps/)
2. in your [cartoview](github.com/cartologic/cartoview) installation, login as admin
3. go to *"Apps"* then *"Manage Apps"* then "Install new app"*
4. upload the downloaded package and click install
5. wait untill the installation finish
