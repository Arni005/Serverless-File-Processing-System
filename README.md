---

# 📁 Serverless File Upload & Processing System

A fully **serverless, event-driven application** built using AWS that automatically processes uploaded files, extracts metadata, stores details in **DynamoDB**, and sends **real-time notifications** via SNS.

---

## 🚀 Overview

This project demonstrates how to build a **scalable serverless architecture** using **AWS Lambda**, **S3**, **DynamoDB**, and **SNS** — a common workflow used in cloud automation, enterprise data ingestion, and serverless backends.

Whenever a file is uploaded to an S3 bucket, a Lambda function is triggered that:

1. Extracts file metadata (name, size, timestamp)
2. Stores the metadata in DynamoDB
3. Publishes a notification via Amazon SNS to alert about the new file upload

---

## 🧩 Architecture Diagram

![Alt text](images/Gemini_Generated_Image_a0t2cha0t2cha0t2.png)


---

## ⚙️ AWS Services Used

| Service               | Purpose                    |
| --------------------- | -------------------------- |
| **Amazon S3**         | Stores uploaded files      |
| **AWS Lambda**        | Processes S3 upload events |
| **Amazon DynamoDB**   | Stores file metadata       |
| **Amazon SNS**        | Sends email notifications  |
| **Amazon CloudWatch** | Monitors logs and metrics  |

---

## 🛠️ Project Setup

### 1️⃣ Create an S3 Bucket

* Go to **Amazon S3 Console**
* Create a bucket (e.g., `serverless-file-processing-project`)
* Under **Properties → Event Notifications**, create a new event:

  * **Event type**: `all object create event`
  * **Destination**: Lambda function (created later)

---

### 2️⃣ Create a DynamoDB Table

* Table name: `FileUploads`
* Primary key: `file_name` (String)

---

### 3️⃣ Create an SNS Topic

* Topic name: `FileUploadNotifications`
* Subscribe your email (check inbox to confirm)
* Copy the **Topic ARN** (you’ll use it in Lambda)

---

### 4️⃣ Create a Lambda Function

* Function name: `FileProcessorLambda`
* Runtime: `Python 3.9` or later
* Add environment variables:

  ```
  DYNAMODB_TABLE = FileUploads
  SNS_TOPIC_ARN = arn:aws:sns:REGION:ACCOUNT_ID:FileUploadNotifications
  ```
* Attach an **IAM Role** with permissions for:

  * `s3:GetObject`
  * `dynamodb:PutItem`
  * `sns:Publish`
  * 
---

## 🧪 Testing

1. Upload a file to your S3 bucket (any image, PDF, or text file).
2. Check **DynamoDB → FileUploads** → you should see a new record.
3. Check your **email inbox** → you’ll receive a notification.
4. Check **CloudWatch Logs** if something fails.

---

## 📊 Example DynamoDB Record

```json
{
  "file_name": "invoice.pdf",
  "bucket": "serverless-file-processing-project",
  "file_size": 45213,
  "upload_time": "2025-10-17T12:45:00Z"
}
```

---

## 🧰 Optional Add-ons

| Feature                    | Description                                |
| -------------------------- | ------------------------------------------ |
| **CloudFront + S3 Web UI** | Create a simple frontend to upload files   |
| **API Gateway**            | Add REST API for querying uploaded files   |
| **SES instead of SNS**     | Send rich HTML emails                      |
| **Cost Monitoring**        | Add CloudWatch metrics for uploads per day |

---

## 🧼 Cleanup (to avoid charges)

When finished:

1. Delete S3 bucket (after removing files)
2. Delete Lambda function
3. Delete SNS topic
4. Delete DynamoDB table

---

## Author

**Arni Johry**

---
