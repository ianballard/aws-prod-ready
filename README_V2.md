# AWS Production-Ready Starter Template

A highly configurable starter template for quickly scaffolding production-ready systems on AWS. This project leverages 
serverless architecture, including AWS API Gateway, Lambda, and DynamoDB, as well as event-driven architecture. 
It focuses on security, incorporating best practices for audit logging with CloudTrail and resource management using AWS
services like AWS Config, GuardDuty, and Security Hub. The template also prioritizes business continuity plans for data 
redundancy and backups and can be configured to set resources in private subnets within a VPC if required.

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
- `backupRegion`: The secondary AWS region where replicas and backups will be stored.
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

Provide step-by-step instructions on how to install and set up the project.

1. Step 1 - Description of the first step
2. Step 2 - Description of the second step
3. Step 3 - Description of the third step

## Usage

Explain how to use the project, including any configuration options, command-line arguments, or examples of common use cases.

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