# AWS Production-Ready Starter Template

A highly configurable starter template for quickly scaffolding production-ready systems on AWS. This project leverages 
serverless architecture, event-driven architecture, and it focuses on best practices for a well-architected framework at all levels.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Maintenance](#maintenance)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgements](#acknowledgements)

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
- `appId`: A unique identifier used for creating S3 bucket names.
- `dbTableName`: The name of the DynamoDB table.
- `stackType`: Determines whether the stack is a primary or secondary (replica) region.
- `enablePersistentStorage`: Enables or disables persistent storage (set to true for long-lived environments, false for ephemeral environments).
- `enableVPC`: Enables or disables the use of a Virtual Private Cloud (VPC).
- `enableOpenSearch`: Enables or disables the use of AWS OpenSearch Service.
- `enableS3Replication`: Enables or disables Amazon S3 bucket replication.
- `enableAWSAuth`: Enables or disables AWS authentication using Amazon Cognito.
- `enableBackup`: Enables or disables AWS Backup for creating and managing backups.
- `enableSecurity`: Enables or disables security features such as AWS Security Hub, GuardDuty, and Config.
- `enableApiCDN`: Enables or disables the use of a Content Delivery Network (CDN) for the API Gateway (this can be set to false for quicker ephemeral environment deployments).
- `corsAllowedOrigins`: Specifies the allowed origins for CORS (Cross-Origin Resource Sharing) headers.
- `emailDistributionSubscription`: Specifies the email distribution list for receiving alerts related to the project like error alarms.

## Features

In addition to the configurable options, this AWS Production-Ready Starter Template includes the following features to 
help you set up a robust and secure infrastructure:

### Serverless Architecture

The template is designed with a serverless architecture in mind, utilizing AWS API Gateway for creating, publishing, 
and managing APIs, AWS Lambda for running your code without provisioning or managing servers, and DynamoDB as a 
managed NoSQL database.

### Event-Driven Architecture

This project embraces an event-driven architecture, allowing you to build highly scalable and efficient applications by automatically triggering AWS Lambda functions based on events in DynamoDB and other AWS services. Some key aspects of the event-driven architecture in this template are:

#### DynamoDB Stream Events

The template is designed to consume, process, and send DynamoDB stream events to various destinations, such as:

- AWS OpenSearch Service, for indexing, searching, and analyzing large volumes of data.
- Amazon Kinesis Data Firehose, for reliably loading streaming data into data lakes, and analytics services.

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

### Business Continuity

The template emphasizes business continuity by providing:

- Data redundancy and backups using AWS Backup and cross-region replication for Amazon S3 buckets.
- The ability to configure resources in private subnets within a VPC, offering an additional layer of security.

### Highly Configurable

The AWS Production-Ready Starter Template utilizes a pattern of configurable nested stacks segmented by functionality, enabling you to conditionally create stacks based on the parameters you provide. This modular approach allows you to maintain a clean and organized infrastructure, while offering a high level of customization for each component of your system.

The primary stack is responsible for creating and managing the nested stacks, which are divided according to their specific functionality. Each nested stack is designed to be independently configurable through the use of parameters. By adjusting these parameters, you can choose whether to enable or disable certain features, as well as control the behavior and properties of individual resources within each stack.

For example, you can conditionally enable or disable the creation of a VPC, persistent storage, OpenSearch, S3 replication, AWS authentication, backups, security, and API CDN by adjusting their respective parameters in the primary stack. This flexibility allows you to tailor your infrastructure to your specific needs while maintaining a clear separation of concerns among various components.

The use of nested stacks also simplifies the management and deployment of your infrastructure, as updates to individual components can be performed independently, reducing the risk of unintended side effects. Additionally, this modular approach promotes reusability, as individual nested stacks can be easily shared and reused across multiple projects or environments.

### Monitoring and Alerting

The template includes monitoring and alerting capabilities to ensure the health and performance of your infrastructure. It integrates with Amazon CloudWatch for monitoring your resources and applications, as well as sending notifications to the specified email distribution list for any alerts or issues that may arise.

### Auto-Generated OpenAPI Specification

The template includes automatic generation of OpenAPI specifications from API Gateway definitions. These specifications are published to an Amazon CloudFront distribution, making it easy for developers to access and maintain up-to-date documentation for your API. This feature streamlines the process of keeping your API documentation in sync with your actual API implementation, ensuring that developers always have accurate and up-to-date information about your API's capabilities and usage.

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
     conda create --name my_env python=3.9
     ```

   - Activate the new Conda environment:

     - On Windows, run:

       ```
       conda activate my_env
       ```

     - On macOS and Linux, run:

       ```
       source activate my_env
       ```

7. **Install the project dependencies**: Navigate to the project's root directory, where the `requirements.txt` file is located. Install the dependencies in your Conda environment by running the following command:

   ```
   pip install -r requirements.txt
   ```

   This command installs the required packages and libraries specified in the `requirements.txt` file into your Conda environment.

8. **Run the requirements_to_local_layers script**: After installing the dependencies, run the `requirements_to_local_layer.sh` script located in the `./scripts` directory. This script helps you manage your project's dependencies and ensures that your AWS Lambda functions have access to the necessary libraries. Run the following command:

   ```
   ./scripts/requirements_to_local_layer.sh
   ```

   This command will process the installed dependencies and generate the required local layers for your AWS Lambda functions.

By completing these prerequisites, you will have a properly configured development environment to work with the AWS Production-Ready Starter Template.

## Usage

### Setting Parameters


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
* **Parameter enableS3Replication**: Enable S3 replication (true or false).
* **Parameter enableAWSAuth**: Enable AWS authentication with Amazon Cognito (true or false).
* **Parameter enableBackup**: Enable AWS Backup support (true or false).
* **Parameter enableSecurity**: Enable security features (true or false).
* **Parameter enableApiCDN**: Enable API Gateway CloudFront distribution (true or false).
* **Parameter corsAllowedOrigins**: Allowed CORS origins for your API (e.g., * for all origins, or a specific domain).
* **Parameter emailDistributionSubscription**: Email address for receiving alerts and notifications (e.g., your-email@gmail.com).

During the guided deployment process, you will be prompted to enter values for each of these parameters. After entering the required information, you can confirm the changes and proceed with the deployment.

* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Save arguments to samconfig.<primary|secondary>.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
sam local start-api
curl http://localhost:3000/
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

### Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
sam logs -n HelloWorldFunction --stack-name sam-app --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## #Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
pip install -r tests/requirements.txt --user
# unit test
python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

### Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name sam-app
```

### Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)


----

## New Env Deploy Process:

- update values in samconfig files for regions and app ids other parameter overrides
- deploy main stack with replication disabled
- deploy second stack with replication enabled
- redeploy main stack with replication enabled

### Configuration

If applicable, describe any configuration files or options and how to customize them.

### Examples

Provide examples of how to use the project, including code snippets or command-line examples.

## Maintenance

Explain how to maintain the project, including how to update dependencies, apply patches, or perform any other required maintenance tasks.

## Contributing

Outline the process for contributing to the project, including any guidelines, code of conduct, or specific steps that contributors should follow.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeatureName`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeatureName`)
5. Create a new Pull Request

## License

Include the project's license information, such as the type of license and a link to the full license text.

This project is licensed under the [LICENSE NAME] License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

List any individuals, organizations, or resources that were instrumental in the creation or development of the project.