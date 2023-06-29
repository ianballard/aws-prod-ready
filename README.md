# AWS Production-Ready Starter Template

A highly configurable starter template for quickly scaffolding production-ready systems on AWS. This project leverages 
serverless architecture, event-driven architecture, and it focuses on best practices for a well-architected framework at all levels.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Trouble-Shooting](#trouble-shooting)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The AWS Production-Ready Starter Template is designed to help you quickly create a fully production-ready set of infrastructure on AWS. This project leverages the following features:

- Serverless architecture using AWS API Gateway, Lambda, and DynamoDB
- Event-driven architecture
- Security-focused design, with best practices for audit logging using CloudTrail and resource management using AWS Config, GuardDuty, and Security Hub
- Business continuity planning for data redundancy and backups
- Configurable resources in private subnets within a VPC if required

The full list of configurations for this project and their descriptions are as follows:

- `stage`: The environment stage (e.g., dev, staging, prod, or test-1, test-2, etc. for ephemeral environments).
- `replicaRegion`: The secondary AWS region where replicas and backups will be stored.
- `appId`: A unique identifier used for creating S3 bucket names. It should not contain any special characters and should be in all lowercase. NOTE: You will also want to set this in your GitHub secrets as APP_ID for GitHub actions.
- `dbTableName`: The name of the DynamoDB table. Defaults to "DBTable" if not specified.
- `stackType`: Determines whether the stack is a primary or secondary (replica) region. The allowed values are 'primary' and 'secondary'. Defaults to 'primary' if not specified.
- `enablePersistentStorage`: Enables or disables persistent storage. Set to 'true' for long-lived environments such as dev, release, and prod, and 'false' for ephemeral environments. Defaults to 'true' if not specified.
- `enableVPC`: Enables or disables the use of a Virtual Private Cloud (VPC). The allowed values are 'true', 'false', and 'null'. Defaults to 'false' if not specified.
- `enableOpenSearch`: Enables or disables the use of AWS OpenSearch Service. The allowed values are 'true' and 'false'. Defaults to 'false' if not specified.
- `enableSearchApi`: Enables or disables the Search API. This allows a stack to have the Search API to be deployed and re-use the existing search cluster. The allowed values are 'true' and 'false'. Defaults to 'false' if not specified. This should only ever be true if enableOpenSearch is enabled in the long-lived stack. Useful for ephemerals.
- `enableS3Replication`: Enables or disables Amazon S3 bucket replication. Please note that buckets must exist (deploy stacks once with this disabled before enabling). The allowed values are 'true' and 'false'. Defaults to 'false' if not specified.
- `enableAWSAuth`: Enables or disables AWS authentication using Amazon Cognito. The allowed values are 'true' and 'false'. Defaults to 'true' if not specified.
- `enableBackup`: Enables or disables AWS Backup for creating and managing backups. The allowed values are 'true' and 'false'. Defaults to 'true' if not specified.
- `enableSecurity`: Enables or disables security features such as AWS Security Hub, GuardDuty, and Config. The allowed values are 'true' and 'false'. Defaults to 'true' if not specified.
- `corsAllowedOrigins`: Specifies the allowed origins for CORS (Cross-Origin Resource Sharing) headers. Defaults to empty if not specified.
- `emailDistributionSubscription`: Specifies the email distribution list for receiving alerts related to the project like error alarms.
- `enableDNS`: Enables or disables the use of AWS Route53 DNS. The allowed values are 'true' and 'false'. Defaults to 'false' if not specified.
- `hostedZoneName`: Specifies the DNS Hosted Zone. Defaults to empty if not specified.
- `hostedZoneId`: Specifies the DNS Hosted Id. Defaults to empty if not specified.

*NOTE:* Be mindful that some parameters and associated functionality may have dependencies. For example, by setting enableDNS to true, hostedZoneName and hostedZoneId need to be set. 
Or, in order to take advantage of some of the management event handling like when a new log group is created, enableSecurity must be set to true (CloudTrail emits the event that is then consumed).

## Features

In addition to the configurable options, this AWS Production-Ready Starter Template includes the following features to 
help you set up a robust and secure infrastructure:

### Serverless Architecture

The template is designed with a serverless architecture in mind, utilizing AWS API Gateway for creating, publishing, 
and managing APIs, AWS Lambda for running your code without provisioning or managing servers, and DynamoDB as a 
managed NoSQL database.

### Latency-based Multi-region and Fail-over Support with DNS Health Checks

The template provides a robust mechanism to ensure optimal user experience and high availability by utilizing AWS Route53 for latency-based routing and DNS health checks. 

This feature is designed to deliver your application with minimal latency and enhanced reliability. By hosting your application in multiple AWS regions, latency-based routing allows Route53 to direct user requests to the region that provides the lowest latency, ensuring faster load times for your users.

Alongside latency-based routing, DNS health checks are used to monitor the health and performance of your application's endpoints. If an endpoint becomes unhealthy - for instance, in case of a regional outage or an issue with your application - Route53's failover mechanism is triggered. 

The failover routing policy automatically redirects the traffic to a healthy region, thereby ensuring uninterrupted availability of your application. This feature makes it possible to provide reliable service to your users, even in the face of unforeseen outages or performance issues.

This combination of latency-based routing and DNS health checks provides an efficient multi-region strategy, enhancing the resilience and performance of your infrastructure.


### Event-Driven Architecture

This project embraces an event-driven architecture, allowing you to build highly scalable and efficient applications by automatically triggering AWS Lambda functions based on events in DynamoDB and other AWS services. Some key aspects of the event-driven architecture in this template are:

#### DynamoDB Stream Events

The template is designed to consume, process, and send DynamoDB stream events to various destinations, such as:

- AWS OpenSearch Service, for indexing, searching, and analyzing large volumes of data.
- Amazon Kinesis Data Firehose, for reliably loading streaming data into data lakes, and analytics services.

**NOTE: If the DB Event Stack is deployed and the events are not being processed, there was likely a problem with the Custom Resource execution that is supposed to enable the lambda's trigger. Please Refer to the Custom Resource Trouble Shooting section for more details.** 

#### Multi-Region AWS Cognito Service

The template replicates authentication events to replica regions, creating a multi-region AWS Cognito service. This ensures that your authentication service is highly available and fault-tolerant, providing consistent performance and reliability for your users.

#### Centralized Logging

The template centralizes application error and access logs for easier maintenance, tracing, and alerting. It uses AWS EventBridge to associate subscription filters for individual Lambda log groups, enabling you to put log events to central logging Lambdas whenever a new log group is created. This centralization of logs simplifies the process of monitoring and managing log data across your infrastructure, helping you identify and resolve issues more efficiently.

### Security Focus

The template is built with a strong focus on security, incorporating the following:

- Audit logging with AWS CloudTrail for monitoring, compliance, and operational auditing.
- Resource management using AWS Config, which provides a detailed view of the configuration of your AWS resources and evaluates them against best practices.
- Threat detection and continuous security monitoring with Amazon GuardDuty.
- Aggregated security findings and insights with AWS Security Hub.
- The ability to configure resources in private subnets within a VPC, offering an additional layer of security.
- User access logging to easily trace user sessions

### Business Continuity

The template emphasizes business continuity by providing:

- Data redundancy and backups using AWS Backup and cross-region replication for Amazon S3 buckets.

### Highly Configurable

The AWS Production-Ready Starter Template utilizes a pattern of configurable nested stacks segmented by functionality, enabling you to conditionally create stacks based on the parameters you provide. This modular approach allows you to maintain a clean and organized infrastructure, while offering a high level of customization for each component of your system.

The primary stack is responsible for creating and managing the nested stacks, which are divided according to their specific functionality. Each nested stack is designed to be independently configurable through the use of parameters. By adjusting these parameters, you can choose whether to enable or disable certain features, as well as control the behavior and properties of individual resources within each stack.

For example, you can conditionally enable or disable the creation of a VPC, persistent storage, OpenSearch, S3 replication, AWS authentication, backups, security, and API CDN by adjusting their respective parameters in the primary stack. This flexibility allows you to tailor your infrastructure to your specific needs while maintaining a clear separation of concerns among various components.

The use of nested stacks also simplifies the management and deployment of your infrastructure, as updates to individual components can be performed independently, reducing the risk of unintended side effects. Additionally, this modular approach promotes reusability, as individual nested stacks can be easily shared and reused across multiple projects or environments.

### Monitoring and Alerting

The template includes monitoring and alerting capabilities to ensure the health and performance of your infrastructure. It integrates with Amazon CloudWatch for monitoring your resources and applications, as well as sending notifications to the specified email distribution list for any alerts or issues that may arise.

### APIs

The AWS Production-Ready Starter Template also includes several pre-built APIs to help you get started with common functionality in your application:

1. **Auth API**: This API provides three endpoints for user authentication:
   * Sign Up: Allows users to register for an account.
   * Confirm Sign Up: Confirms the user's registration with a verification code.
   * Authenticate: Authenticates the user and provides an access token for further API requests.

2. **User Management API**: This API includes five endpoints to manage users and their relationships:
   * Associate Users: Allows users to establish associations with other users (e.g., "following" in a social media platform).
   * Query Associated Users: Retrieves a list of users associated with the current user.
   * Get User Profile: Retrieves the profile information for a specific user.
   * Update User: Allows users to update their own profile information.
   * Delete User: Enables users to delete their own account.

3. **Search API** (available if OpenSearch is enabled): This API allows you to search for users based on various attributes, such as username, email, first name, or last name. It provides a single endpoint for submitting search queries.

**NOTE: If the Open Search Stack is deployed and the search operations are not working or documents are not being posted, there was likely a problem with the Custom Resource executions that are supposed to update the cluster permissions, index creation, and logging settings. Please Refer to the Custom Resource Trouble Shooting section for more details.**

Each endpoint in the User Management and Search APIs is equipped with authorization models to determine if the principal user can access the requested resources. This ensures that your application enforces appropriate access controls and maintains user privacy.

These pre-built APIs can significantly accelerate the development process by providing a solid foundation for common functionality in your application.

### Auto-Generated OpenAPI Specification

The template includes automatic generation of OpenAPI specifications from API Gateway definitions. These specifications are published to an Amazon CloudFront distribution, making it easy for developers to access and maintain up-to-date documentation for your API. This feature streamlines the process of keeping your API documentation in sync with your actual API implementation, ensuring that developers always have accurate and up-to-date information about your API's capabilities and usage. Assuming the API stacks have been deployed, follow these steps to view the api definitions with a SwaggerUI:

1. Set the CloudFront distribution: After deploying the stack, locate the CloudFront distribution URL that serves the API definitions. This should be an output of the API Stack. Update the client/api-docs/.env file with the appropriate distribution URL.

2. Install dependencies: Navigate to the client/api-docs directory and run npm install to install the required dependencies for the API documentation viewer.

3. Start the documentation viewer: From the client/api-docs directory, run npm start to start the documentation viewer. This will open a local development server in your default web browser, allowing you to interact with the auto-generated API documentation.

**NOTE: If the API Stack is deployed and the API specs are not generated or out of date, there was likely a problem with the Custom Resource executions that are supposed to create/update the OpenAPI specifications. Please Refer to the Custom Resource Trouble Shooting section for more details.**

### GitHub Actions Workflows

The AWS Production-Ready Starter Template includes GitHub Actions workflows to automate various aspects of the development process. These workflows are divided into two categories:

#### 1. Automatic Workflows

These workflows run automatically on each push to the repository, ensuring that your code is consistently tested and adheres to best practices:

* **Run Unit Tests**: Tests your application logic using the Pytest framework.
* **Run Linting**: Checks your code for compliance with Python best practices, such as PEP 8, using the Flake8 linting tool.
* **Run Security Static Code Analysis**: Performs static code analysis to identify potential security vulnerabilities in your code using the Bandit security linter.

#### 2. Manual Workflows

These workflows are manually triggered and designed to assist with specific development tasks:

* **Create Ephemeral Env CI/CD**: This workflow allows you to create ephemeral environments for non-persistent resources, such as API Gateway and AWS Lambda functions. To run this workflow, you need to provide the source branch and a stage name for the new environment. This enables you to easily test and review changes in an isolated environment before merging them into your main branch.

By incorporating these GitHub Actions workflows into your development process, you can maintain high-quality, secure code and streamline various tasks related to testing and deploying your application.

## Prerequisites

Before you start using the AWS Production-Ready Starter Template, it is essential to set up your AWS account correctly and ensure that you follow AWS best practices. The following prerequisites will help you set up a secure and efficient AWS account:

### AWS Account Setup

1. **Create an AWS account**: If you do not already have an AWS account, you can sign up for one at https://aws.amazon.com/. This will give you access to AWS services and a Free Tier to help you get started with minimal costs.

2. **Configure IAM (Identity and Access Management)**: Set up proper IAM policies, roles, and users to manage access control for your AWS resources. For more information on IAM best practices, refer to the AWS documentation: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html. Consider using Service Control Policies (SCPs) ti allow you to set fine-grained permissions and restrictions for your AWS accounts within an organization. By using SCPs, you can enforce MFA and implement other typical IAM rules across all accounts in your organization. To learn how to create and use SCPs, refer to the AWS documentation: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scp.html.

3. **Enable Multi-Factor Authentication (MFA)**: Secure your AWS account by enabling MFA for your root user and all IAM users. This adds an extra layer of security to help protect your account from unauthorized access. For instructions on setting up MFA, refer to the AWS documentation: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable.html

4. **Using an External Identity Provider for User Authentication**: To enhance security and simplify user management, consider using an external identity provider (IdP) for user authentication, such as Azure Active Directory (Azure AD). By integrating your AWS account with an external IdP, you can leverage existing user directories, apply consistent access policies across your organization, and benefit from single sign-on (SSO) capabilities.

   AWS supports integration with a variety of IdPs, including Azure AD, Okta, Google Workspace, and more. To configure an external IdP with AWS, you can use AWS Single Sign-On (SSO) or configure a SAML 2.0 trust relationship between your IdP and AWS. For more information on integrating AWS with external IdPs, refer to the following resources:

   - AWS Single Sign-On: https://aws.amazon.com/single-sign-on/
   - Configuring SAML 2.0 trust relationship: https://aws.amazon.com/premiumsupport/knowledge-center/saml-adfs-azure-setup/

   By following these recommendations and integrating an external identity provider, your AWS account will benefit from improved security and streamlined user authentication processes.
5. **Set up Cost Detection and Budgets**: Monitor your AWS usage and costs by setting up AWS Cost Explorer, AWS Budgets, and cost allocation tags. This will help you track and manage your spending, as well as identify opportunities to optimize your resources and reduce costs. For more information on cost management best practices, refer to the AWS documentation: https://aws.amazon.com/aws-cost-management/aws-cost-management-best-practices/

6. **Follow AWS Account Best Practices**: Adhere to AWS account best practices, such as using AWS Organizations to manage multiple accounts, setting up AWS Control Tower for governance, and implementing AWS Well-Architected Framework principles. For more information on AWS account best practices, refer to the following resources:

   - AWS Organizations: https://aws.amazon.com/organizations/
   - AWS Control Tower: https://aws.amazon.com/controltower/
   - AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/

By completing these prerequisites, you will have a secure and well-organized AWS account, allowing you to fully leverage the AWS Production-Ready Starter Template and its features.

## Installation

### Development Environment Setup

Before working with the AWS Production-Ready Starter Template, make sure you have the necessary tools and libraries installed on your local development environment. The following prerequisites are required:

1. **AWS CLI**: Install the AWS Command Line Interface (CLI), which enables you to manage your AWS services from the command line. You can find the installation instructions for your operating system in the AWS documentation: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

2. **AWS SAM**: Install the AWS Serverless Application Model (SAM) CLI, a tool for building, testing, and deploying serverless applications. You can find the installation instructions for your operating system in the AWS documentation: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

3. **Docker**: Install Docker. Docker is a platform that enables developers to build, share, and run applications in containers. It is required for certain tasks, such as running AWS SAM CLI for local testing and development of your AWS Lambda functions. [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

4. **Python 3.9**: Install Python 3.9, which is the recommended Python version for this project. You can download Python 3.9 from the official Python website: https://www.python.org/downloads/

5. **Conda**: Install Conda, an open-source package management system and environment management system for installing multiple versions of software packages and their dependencies. You can find the installation instructions for your operating system in the Conda documentation: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

6. **Create a Virtual Environment for Python 3.9**: After installing Conda, create a virtual environment for Python 3.9 to isolate the project dependencies from your system-wide Python environment. Follow these steps to create and activate the virtual environment:

   - Open a terminal or command prompt and run the following command to create a new Conda environment with Python 3.9:

     ```
     conda create --name aws-prod-ready python=3.9
     ```

   - Activate the new Conda environment:

     - On Windows, run:

       ```
       conda activate aws-prod-ready
       ```

     - On macOS and Linux, run:

       ```
       source activate aws-prod-ready
       ```

7. **Install the project dependencies**: Navigate to the project's root directory, where the `requirements.txt` file is located. Install the dependencies in your Conda environment by running the following command:

   ```
   pip install -r requirements.txt
   ```

   This command installs the required packages and libraries specified in the `requirements.txt` file into your Conda environment.

By completing these prerequisites, you will have a properly configured development environment to work with the AWS Production-Ready Starter Template.

## Usage

### Use as a Template
In the GitHub repository page, click the **Use this template** button to create a new repository.

Follow GitHub protection standards for the repo including adding branch protection rules and adding code owners.

### Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --config-file samconfig.primary.toml
sam deploy --guided --config-file samconfig.primary.toml

sam build --config-file samconfig.secondary.toml
sam deploy --guided --config-file samconfig.secondary.toml
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Parameter stage**: The stage of your application (e.g., development, production, staging).
* **Parameter replicaRegion**: The AWS region for the replica environment.
* **Parameter appId**: A unique identifier for your app (e.g., app-1234567890).
* **Parameter dbTableName**: The name of the DynamoDB table.
* **Parameter stackType**: The type of the stack (e.g., primary, secondary).
* **Parameter enablePersistentStorage**: Enable persistent storage (true or false).
* **Parameter enableVPC**: Enable VPC support (true or false).
* **Parameter enableOpenSearch**: Enable OpenSearch support (true or false).
* **Parameter enableSearchApi**: Enable Search API (true or false). Only set to true if enableOpenSearch is set to true in the long-lived stack.
* **Parameter enableS3Replication**: Enable S3 replication (true or false). **NOTE:** This NEEDS to be false for a first time deploy, otherwise the stack will fail due to the destination bucket not yet existing in the replica region. 
* **Parameter enableAWSAuth**: Enable AWS authentication with Amazon Cognito (true or false).
* **Parameter enableBackup**: Enable AWS Backup support (true or false).
* **Parameter enableSecurity**: Enable security features (true or false).
* **Parameter corsAllowedOrigins**: Allowed CORS origins for your API (e.g., * for all origins, or a specific domain).
* **Parameter emailDistributionSubscription**: Email address for receiving alerts and notifications (e.g., your-email@gmail.com).
* **Parameter enableDNS**: Enables or disables the use of AWS Route53 DNS. The allowed values are 'true' and 'false'. Defaults to 'false' if not specified.
* **Parameter hostedZoneName**: Specifies the DNS Hosted Zone. Defaults to empty if not specified.
* **Parameter hostedZoneId**: Specifies the DNS Hosted Id. Defaults to empty if not specified.

During the guided deployment process, you will be prompted to enter values for each of these parameters. After entering the required information, you can confirm the changes and proceed with the deployment.

* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Save arguments to samconfig.<primary|secondary>.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

### Setting Repository Variables
After deploying the first time, update the repository **Action secrets and variables** under the **Settings** tab.

In order for ephemeral environments to work properly, the following secrets need to be added:

1. AWS_ACCESS_KEY_ID
2. AWS_SECRET_ACCESS_KEY
3. PRIMARY_SAM_BUCKET (primary region stack)
4. SECONDARY_SAM_BUCKET (replica region stack)

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
sam build --use-container --template-file template.local.yaml 
```

The template.local.yaml is not a complete set of app resources, for our purposes it is meant to test individual lambdas and endpoints, not the entire stack in its entirety. Please add or remove functions and api events to your own liking.

For each AWS::Serverless::Function defined in the template file, the SAM CLI installs dependencies defined in it's `requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.


The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 2999. 
There is a script to help with this in the `scripts` directory: `start-local.sh`.

```bash
./scripts/start-local.sh
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

### Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.


### Debugging
#### Debugging AWS SAM Local API in PyCharm

The instructions include creating a remote debug configuration, specifying your Docker host on your local machine, setting up the IDE host and port, adding the required package to the Lambda's `requirements.txt` file, and setting up a trace.

#### Prerequisites
- PyCharm Professional Edition

#### Steps


1. **Find the Docker network IP range**:

    First, find the Docker network your containers are running on. You can use the `docker network ls` command to list the available networks:

    ```
    docker network ls
    ```

    Identify the network that your container is using. By default, it might be the `bridge` network.

2. **Inspect the Docker network**:

    Run the `docker network inspect` command to get detailed information about the selected network:

    ```
    docker network inspect bridge
    ```

    Look for the "Gateway" field under the "IPAM" section in the output. The "Gateway" field contains the IP address of the Docker host. For example:

    ```
    "Gateway": "172.17.0.1"
    ```

    Use this IP address for your debugging setup.

3. **Create a remote debug configuration in PyCharm**:

    - Go to `Run` > `Edit Configurations...`
    - Click the `+` button and select `Python Debug Server`
    - Set the `Name` to "SAM Debug"
    - Set the `Host` to your Docker host IP address (e.g., `172.17.0.1`)
    - Set the `Port` to `5858`
    - Save the configuration by clicking `OK`

4. **Add the `pydevd-pycharm` package to your Lambda's `requirements.txt` file**:

    ```
    pydevd-pycharm==<pydevd-pycharm version suggested>
    ```

    *Note: Replace the version number with the one corresponding to your PyCharm version.*

5. **Add the import and trace setup in your Lambda function**:

    At the beginning of your Lambda function, add the following lines:

    ```python
    import pydevd_pycharm
    pydevd_pycharm.settrace('172.17.0.1', port=5858, stdoutToServer=True, stderrToServer=True)
    ```

    Replace `'172.17.0.1'` with your Docker host IP address.

6. **Build the AWS SAM application**:

7. **Start the AWS SAM local API**

8. **Start the remote debug configuration in PyCharm**:

    - In PyCharm, go to `Run` > `Debug` > `SAM Debug`
    - Wait for the debug server to start and show the message "Waiting for process connection..."

9. **Send requests to your local API**:

    Send requests to your local API using a tool like `curl` or Postman. The breakpoints set in your Lambda function should be hit, and the debugging session should start in PyCharm.


### Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
# unit test
python -m pytest tests/unit -v
```

### Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

### Examples

#### Auth API

1. Sign Up
   ```bash
   curl -X POST 'https://<auth-api-host>/Prod/v1.0/signup' \
   -H 'Content-Type: application/json' \
   -d '{
     "username": "johndoe",
     "password": "your_password",
     "email": "johndoe@example.com",
     "first_name": "John",
     "last_name": "Doe"
   }'

   ```

2. Confirm Sign Up
   ```bash
   curl -X GET 'https://<auth-api-host>/Prod/v1.0/confirm_sign_up?username=johndoe&code=123456'
   ```
   
3. Authenticate
   ```bash
   curl -X POST 'https://<auth-api-host>/Prod/v1.0/auth' \
   -H 'Content-Type: application/json' \
   -d '{
     "username": "johndoe",
     "password": "your_password"
   }'

   ```

#### Search API

1. Search Users
   ```bash
   curl -X POST 'https://<search-api-host>/Prod/v1.0/search/user' \
   -H 'Content-Type: application/json' \
   -d '{
     "search_str": "johndoe"
   }'
   ```

#### User API

1. Associate user:
   ```bash
   curl -X PUT 'https://<user-api-host>/Prod/v1.0/user/{id}/associate' \
   -H 'Content-Type: application/json'
   ```
   Replace `{id}` with the user's ID.

2. Query associated users:
   ```bash
   curl -X GET 'https://<user-api-host>/Prod/v1.0/user' \
   -H 'Content-Type: application/json'
   ```

3. Get user:
   ```bash
   curl -X GET 'https://<user-api-host>/Prod/v1.0/user/{id}' \
   -H 'Content-Type: application/json'
   ```
   Replace `{id}` with the user's ID.

4. Update user:
   ```bash
   curl -X PATCH 'https://<user-api-host>/Prod/v1.0/user/{id}' \
   -H 'Content-Type: application/json' \
   -d '{"entity_status": "example_status"}'
   ```
   Replace `{id}` with the user's ID and `example_status` with the desired status (ACTIVE or INACTIVE).

5. Delete user:
   ```bash
   curl -X DELETE 'https://<user-api-host>/Prod/v1.0/user/{id}' \
   -H 'Content-Type: application/json'
   ```
   Replace `{id}` with the user's ID.

## Trouble-Shooting

### Custom Resource Trouble Shooting

If a Custom Resource did not execute as expected. Simply check it's expected properties in its parent cloudformation 
template, and execute the underlying lambda function manually with these defined in a ResourceProperties object. 
Additionally, check the lambda code to see what RequestType (Create, Update, Delete) should be set to. An example input 
might look like this:

```json
{
  "RequestType": "Create",
   "ResourceProperties": {
      "foo": "bar"
   }
}
```

The list of Custom Resources are:

- ExecuteManageAuthApiExportsFunction
- ExecuteManageUserApiExportsFunction
- ExecuteManageSearchApiExportsFunction
- ExecuteCreateDBStreamEventTriggerFunction
- ExecuteSearchAdminAssignWriteAccessFunction
- ExecuteSearchAdminEnableLoggingFunction
- ExecuteSearchAdminCreateUserIndexFunction

## Contributing

Pull requests are welcome for bugfixes and new features. Please only create pull requests targeting the develop branch and use gitflow naming conventions. 
- New Features: feature/YourFeatureName
- Fixes: bugfix/FixName


## License

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)