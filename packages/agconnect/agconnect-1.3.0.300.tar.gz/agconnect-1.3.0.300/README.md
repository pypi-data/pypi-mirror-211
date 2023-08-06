# Huawei AppGallery Connect Python Server SDK

## Overview

AppGallery Connect is dedicated to providing one-stop services for app creation, development,
distribution, operations, and engagement, and building a smart app ecosystem for all scenarios.
By opening up a wide range of services and capabilities, which are built upon Huawei's profound
experience in globalization, quality, security, and project management, AppGallery Connect substantially
simplifies app development and O&M, improves app version quality, and helps apps attract a wider
scope of users and generate higher revenue.You can access the services listed below.

This module contains Server SDKs for following AGC Services:

1.Auth Service
2.Cloud Function
3.Cloud DB
4.Cloud Storage

For more information, visit
the [AppGallery Connect Introduction](https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-Guides/agc-introduction-0000001057492641)

## Auth Service Overview

Auth Service provides an SDK and backend services, supports multiple authentication modes,
and provides a powerful management console, enabling you to easily develop and manage user authentication,helps
you quickly build a secure and reliable user authentication system for your app by directly integrating
cloud-based Auth Service capabilities into your app.

## Documentation

- [Auth Service Introduction](https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-Guides/agc-auth-introduction-0000001053732605)

## Cloud Function Overview

Cloud Functions enables serverless computing. It provides the Function as a Service (FaaS) capabilities to
simplify app development and O&M by splitting service logic into functions and offers the Cloud Functions SDK that
works with Cloud DB and Cloud Storage so that your app functions can be implemented more easily. Cloud Functions
automatically scales in or out server resources for functions based on actual traffic, freeing you from server
resource management and reducing your O&M workload.

- [Cloud Function Introduction](https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-Guides/agc-cloudfunction-introduction-0000001059279544)

## Cloud DB Overview

Cloud DB is a device-cloud synergy database product that provides data synergy management capabilities, unified
data models, and various data management APIs. In addition to ensuring data availability, reliability,
consistency, and security, CloudDB enables seamless data synchronization between the device and cloud,
and supports offline application operations, helping developers quickly develop device-cloud and multi-device
synergy applications. As a part of the AppGallery Connect solution, Cloud DB builds the Mobile Backend as a Service
(MBaaS) capability for the AppGallery Connect platform. In this way, application developers can focus on
application services, greatly improving the production efficiency.

## Cloud Storage Overview

AppGallery Connect Cloud Storage allows you to store high volumes of data such as images, audio, videos, and other 
user-generated content securely and economically. This scalable and maintenance-free service can free you 
from development, deployment, O&M, and capacity expansion of storage servers, so you can focus on 
service capability building and operations with better user experience. The Cloud Storage SDK provided 
for various clients has the following advantages in file uploads and downloads.Strong security: 
Data is transmitted using HTTPS, and files are encrypted and stored on the cloud using secure 
encryption protocols. Resumable transfer, You can resume uploads or downloads from the breakpoint 
if there is a network failure or misoperation while the upload or download is underway.

- [Cloud Storage Introduction](https://developer.huawei.com/consumer/en/doc/development/AppGallery-connect-Guides/agc-cloudstorage-introduction-0000001054847259)

## Agconnect Installation

You can install the agconnect via PyPi

    pip install agconnect

After the installation takes place, you can import the SDKs as shown below:

    from agconnect.auth_server import AGCAuth
    from agconnect.cloud_function import AGConnectFunction
    from agconnect.database_server import AGConnectCloudDB
    from agconnect.cloud_storage import AGConnectCloudStorage

# Supported Environments

This project supports Python version 3.7 or higher

Also note that the Huawei AppGallery Connect Python Server SDK should only be used in server-side/back-end environments
controlled by the application developer.This includes most server and serverless platforms. Do not use the Python Server
SDK environment in the client.

## License

Huawei AppGallery Connect Python Server SDK for Auth is licensed under the "ISC".

## Keywords

[agconnect](https://pypi.org/search/?q=agconnect&o=)

[python](https://pypi.org/search/?q=python&o=)

[server sdk](https://pypi.org/search/?q=server+sdk&o=)

[authentication](https://pypi.org/search/?q=authentication&o=)
