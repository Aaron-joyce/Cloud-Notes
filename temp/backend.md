# Backend API Service

## 1. External Libraries/Packages Used

This node.js backend relies heavily on the following external dependencies (from `package.json`):
- **@aws-sdk/client-s3 & s3-request-presigner**: For uploading and retrieving profile images and signatures (S3/MinIO compatible storage).
- **@prisma/client & prisma**: The ORM framework for interacting with the PostgreSQL database.
- **bcrypt**: For securely hashing and verifying passwords from students and admins.
- **cookie-parser & cors**: Middleware to parse cookies (useful for JWT storage) and enable Cross-Origin Resource Sharing for student and admin frontends.
- **dotenv**: To parse environment variables like DB connections.
- **express**: The core web app framework handling API routing.
- **express-rate-limit**: To protect authentication and main routes from DDoS/Spamming.
- **express-validator**: Data validation for incoming requests.
- **helmet**: Secure HTTP headers for protecting against well-known web vulnerabilities.
- **json2csv**: Used to convert application data to CSV data tables for the admin dashboard.
- **jsonwebtoken**: For creating and verifying JWT access tokens.
- **nodemailer**: Used for configuring an SMTP client and sending status updates and OTPs via email.
- **otp-generator**: For generating 6-digit one-time passwords for onboarding user verification.
- **pg**: Pure JS driver for PostgreSQL interacting with Prisma/Drizzle.
- **swagger-jsdoc & swagger-ui-express**: Providing API documentation and testing capabilities to developers under `/api/docs`.
- **ws**: WebSocket framework used for real-time live events and notifications on the dashboards.

---

## 2. Each Function and its Working by File

The backend employs an MVC style structure focusing on Controllers processing business logic, and Services abstracting reusable elements.

### `app.js` & `server.js`
- **Working**: Setup the Express application, configures global middlewares (CORS, Morgan, Helmet), initiates Swagger Docs, configures API rate limiting, defines primary route prefixes (like `/api/auth`, `/api/student`, `/api/admin`, `/api/applications`, etc.), and starts the WebSocket server and CRON jobs.

### `controllers/admin.controller.js`
- **`listApplications`**: Fetches paginated applications belonging to students dynamically applying specific SQL-like filters.
- **`approveApplication`**: Approves pass generation and internally invokes certificate generation service and optional auto slot. Logs auditing details.
- **`rejectApplication`**: Marks pass request as rejected, attaching a rejection message, and logs standard audits.
- **`bulkActionApplications`**: Accepts multiple application ID's, applying bulk rejections or approvals transactionally.
- **`getAdminDashboard`**: Performs aggregated COUNT and GROUP BY queries on tables to feed statistics on the Admin UI.
- **`verifyStudentPayment`**: Changes verification tracking of standard fees manually using admin tools.

### `controllers/application.controller.js`
- **`applyForPass`**: Registers a new pass context. Ensures users do not have multiple active applications simultaneously or concurrent active passes. Uses `generateAppId()`.
- **`myApplications`**: Returns all applications correlated to the logged in student ID.
- **`getApplication`**: Fetches a single application using ID, protecting routes ensuring students only fetch their own properties.

### `controllers/auth.controller.js`
- **`studentLogin` & `adminLogin`**: Compares username/CRIDNs and plain passwords against `bcrypt` hashed variants. Issues and signs an HTTPOnly cookie embedded with JWT payload.
- **`studentRegister`**: Initiates registration but checks if CRIDN clashes, hashing passwords, logging them unverified.
- **`forgotPassword`, `sendResetPasswordLink`, `resetPassword`**: Emits a token for password resets wrapped over email.
- **`validateSession`**: Protects secure areas by validating token extraction from headers/cookies.

### `controllers/student.controller.js`
- **`getProfile`**: Serves deep relationships containing user's profile metadata and signed short-lived URLs to access their S3 image blobs securely.
- **`getAllStudents`**: Typically used by Admin, lists entire array of student profiles across all branches with presigned URLs.
- **`uploadProfileImage` / `uploadSignature`**: Ingests `multer` buffers into S3 blobs natively and links the S3 paths contextually inside Prisma.

### `controllers/slot.controller.js`
- **`createCollectionSlot` & `generateSlots`**: Admin tools to iteratively provision pickup window periods avoiding collisions.
- **`bookSlot` & `cancelSlot`**: Students can book exact `collectionSlot` if their `status=Approved`. Maintains constraints enforcing 3 concurrent attempts.
- **`markSlotCollected`**: Disables the slot denoting pass handed manually.

### `controllers/onboarding.controller.js`
- **`initiateOnboarding`**: Creates unique identifier (CRIDN) logic based on College classification, validating duplicity limits.
- **`verifyOnboarding`**: Authenticates users consuming single-shot OTP stored locally. Enforces fresh passwords after email validations.
- **`resendOTP`**: Generates new 6-digit identifier via `otp-generator` wrapped under `nodemailer`.

### `controllers/certificate.controller.js`
- **`createCertificate`**: Accepts approved passes mapping them explicitly to specific dates factoring in 1-month to 3-month durations dynamically updating SQL relations.

### `services/`
- Contains decoupled business logic. Includes:
  - `email.service.js`: Interfaces tightly with Nodemailer transporting SMTP data.
  - `audit.service.js`: Logs all IP and payload specific activities executed mainly by Administrators.
  - `s3.utils.js`: Core methods interfacing with the @aws-sdk object commands `PutObject`, `GetObject`.

---

## 3. Overall Working 

The backend acts as the standard RESTful hub, communicating bidirectionally with Postgres via Prisma ORM for queries, mutations, and constraints.  

**Input Origins:**
1. **Admin Frontend Request (Admin Portal)**: Passes bulk updates, slot provisionings, searches, dashboards queries via HTTP endpoints and payload bodies.
2. **User Frontend Request (Student Portal)**: Pushes credentials via POST logic, uploads binary Multipart imagery (for profiles/signatures), applies to railway concessions and manages personal profile modifications.

**Output Destinations:**
1. **To User (Student Frontend)**: Fetches presigned profile blobs from S3 infrastructure to render UI assets. Reads pass status pipelines tracking statuses asynchronously through Polling/Sockets. 
2. **To Admin (Admin Frontend)**: Exports aggregate analytics mapping all colleges and processing volumes. Emits lists of active slots contextually.
3. **To Email Services**: Utilizing asynchronous Nodemailer functions invoked as side-effects across the controllers emitting Welcome hooks, OTP codes, status mutations, and tracking identifiers seamlessly without slowing the internal HTTP requests significantly.
