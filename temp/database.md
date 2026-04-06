# Database Architecture & Storage

This application utilizes **PostgreSQL** as its relational database. The Node.js backend interacts with this database using **Prisma ORM**.

## Schema Overview

### 1. `Student` Table
Stores all the details about the registered students and admins.
- **Columns:**
  - `id` (Integer, Primary Key)
  - `fullName` (String)
  - `crid` (String, Unique) - Custom registration ID
  - `password` (String) - Hashed password
  - `role` (Enum: `STUDENT`, `ADMIN`)
  - `collegeType` (Enum: `JUNIOR`, `SENIOR`)
  - `uidOrRoll` (String)
  - `class` (String)
  - `dob` (DateTime)
  - `address` (String)
  - `homeStation` (String)
  - `createdAt` (DateTime)
- **Relations:**
  - **1-to-Many (1:N) with `PassApplication`**: A single `Student` can have multiple `PassApplication` records (stored via the `applications` field).

### 2. `PassApplication` Table
Stores the details of a railway concession pass requested by a student.
- **Columns:**
  - `id` (Integer, Primary Key)
  - `studentId` (Integer, Foreign Key to `Student.id`)
  - `ageYears` (Integer)
  - `ageMonths` (Integer)
  - `passClass` (Enum: `FIRST`, `SECOND`)
  - `period` (Enum: `MONTHLY`, `QUARTERLY`)
  - `prevVoucherNo` (String, Optional)
  - `prevStartDate` (DateTime, Optional)
  - `prevEndDate` (DateTime, Optional)
  - `status` (Enum: `PENDING`, `APPROVED`, `REJECTED`)
  - `createdAt` (DateTime)
- **Relations:**
  - **Many-to-1 (N:1) with `Student`**: Multiple applications can belong to one `Student`.
  - **1-to-1 (1:1) with `Certificate`**: One application generates exactly one `Certificate`.
  - **1-to-1 (1:1) with `Slot`**: One application has exactly one pickup `Slot`.

### 3. `Certificate` Table
Stores the issued certificate details when a pass application is approved.
- **Columns:**
  - `id` (Integer, Primary Key)
  - `applicationId` (Integer, Unique, Foreign Key to `PassApplication.id`)
  - `certificateNo` (String, Unique)
  - `issuedAt` (DateTime)
- **Relations:**
  - **1-to-1 (1:1) with `PassApplication`**: This certificate belongs to exactly one `PassApplication`.

### 4. `Slot` Table
Stores the collection time slot details for handing over the physical pass.
- **Columns:**
  - `id` (Integer, Primary Key)
  - `applicationId` (Integer, Unique, Foreign Key to `PassApplication.id`)
  - `slotDate` (DateTime)
  - `slotTime` (String)
  - `collected` (Boolean) - Tracks whether the pass has been picked up
- **Relations:**
  - **1-to-1 (1:1) with `PassApplication`**: This slot is mapped to exactly one `PassApplication`.

### Summary of Relationships
- **Student ↔ PassApplication:** `1:Many` (One student can apply for many passes over time).
- **PassApplication ↔ Certificate:** `1:1` (Each application results in one unique certificate).
- **PassApplication ↔ Slot:** `1:1` (Each application booked into one physical collection slot).

*Note: User profile images and signatures are not stored directly in Postgres, but sent to an **S3-compatible blob storage** (e.g., MinIO). Dynamic presigned URLs serve them to the frontends.*

---

## Transaction Methodology: ACID vs BASE

The transactions in this application follow strict **ACID** properties, meaning it prioritizes strong data consistency over the eventual consistency models found in BASE (NoSQL) databases.

1. **Database Engine (PostgreSQL):** PostgreSQL is a traditional RDBMS and is strictly **ACID-compliant**, guaranteeing reliable transaction processing.
2. **ORM Layer (Prisma):** Prisma inherits and executes Postgres's transactional guarantees. Mutating multiple tables together (like approving an application and generating a certificate) utilizes `$transaction` to ensure atomic blocks.
3. **Application Logic:** Features like bulk approval/rejection (`bulkActionApplications`) execute transactionally within the backend controllers to avoid partial update failures.

### ACID Breakdown:
- **Atomicity:** When an application is approved and a certificate must be generated, both writes succeed completely, or both natively roll back.
- **Consistency:** Database schema constraints (like Foreign Keys and Enums) refuse invalid data relationships before they write.
- **Isolation:** Multiple concurrent admins approving data won't trigger overlapping race conditions — each transaction resolves securely.
- **Durability:** Once writes are committed inside Postgres, they are safely preserved to disk.
