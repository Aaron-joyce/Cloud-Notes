# User (Student) Frontend

## 1. External Libraries/Packages Used

This Next.js 14+ (App Router) based student frontend uses several interactive dependencies (from `package.json`):
- **axios**: Used to wrap RESTful HTTP communications with the backend services.
- **html2canvas & jspdf**: Critical for transforming structurally nested React components like `.tsx` Slips/Tickets into downloadable PDF binaries directly inside the browser.
- **js-cookie**: Handles persistent secure token management matching backend HTTP-only states implicitly.
- **lucide-react**: Clean, consistent icon pack utilized across dashboards and form buttons.
- **react-hot-toast**: Triggers clean popup assertions during form submissions like apply, register, slot book.
- **reactflow**: A specialized library to draw node-based maps or diagrams, primarily utilized in `RailwayLineMap.tsx` helping students dynamically visualize and pick start/end stations iteratively.
- **next, react, react-dom**: Core rendering and file-system App Router infrastructure.
---

## 2. Each Function and its Working by File

Functions map heavily to Next.js page components and specific UI interactables.

### `app/page.tsx` & `app/layout.tsx`
- **Working**: Base entry points wrapping Context providers (`AuthContext`, `ConcessionContext`). Routes unauthenticated users towards `/login` and authenticated straight to `/dashboard`.

### `app/login/page.tsx` & `components/login/`
- **Working**: Encapsulates multiple states of entry. `LoginCard.tsx` switches dynamically between `LoginForm.tsx`, `ForgotPasswordForm.tsx`, and invokes backend validators. Sets session cookies natively upon validations.

### `app/onboarding/page.tsx` & `app/verify-email/page.tsx`
- **Working**: Captures complex structured data (like UID, GR Number, Address). Offloads registration rules to `initiateOnboarding` in backend. Routes to the verification challenge that consumes a mailed OTP.

### `app/reset-password/page.tsx`
- **Working**: Retrieves reset-tokens via parameterized URLs overriding forgotten credentials securely.

### `app/dashboard/page.tsx` & `components/StudentDashboard.tsx`
- **Working**: Consolidates active and past metrics. Re-renders `StatCard` configurations to communicate "Total Applications" versus "Approved". 

### `app/profile/page.tsx`
- **Working**: Invokes `getProfile()` locally updating user datasets. Allows users to attach multipart images via `uploadProfileImage()` altering their S3 blobs conditionally.

### `app/application/page.tsx` & `app/applications/[id]/page.tsx`
- **Working**: Employs rigorous Form controls capturing user data parameters against constraints. Fetches `RailwayLineMap.tsx` utilizing `reactflow` dynamically allowing precise endpoint tracing. Pushes `applyForPass()` structures to backend and reads explicitly isolated properties via ID.

### `app/slots/page.tsx`
- **Working**: Polls backend for `getSlots()`. Presents interactive, real-time filtered calendars enabling users to invoke `bookSlot()` matching against `capacity` constraints globally mapped for certificates collections.

### `components/ConcessionCard.tsx` & `components/*RailwayConcessionSlip.tsx`
- **Working**: Static UI configurations reflecting deep layout nuances separating *Junior* formatting structures from *Senior*. Utilizes `jspdf` internally parsing the wrapper DOM converting it immediately into a standardized, printer-friendly exported PDF block.

---

## 3. Overall Working 

The Student frontend functions as a rich, data-driven Client-Side interface optimizing heavily for accessibility and structured form completions guiding students cleanly through the railway concession bureaucracy.

**Working Details:**
1. **Inputs (User Origins):** Students perform heavy data ingestion. They initiate their journey through stringent registration validations (`OnboardingForm`), submit comprehensive personal application forms capturing images, signature blobs, addresses, and pinpoint stations across visual interactive maps (`reactflow`). They also book and cancel calendar slots mapped to existing DB allocations.
2. **Operations:** Components dispatch `axios` payload requests mapping 1:1 against the backend logic. Heavy reliance upon localized Context (`ConcessionContext`) reduces jitter preventing repetitive network calls on cached states (like Profile identities).
3. **Outputs (User Destinations):** Success mutations reflect instantly causing route pushes mapping newly formed application data cleanly. Visual ticket generations occur entirely local utilizing `html2canvas` abstracting away backend payload computations for PDF creations directly allowing "Download Pass" interactions locally on the User's device context window. Backend emails arrive natively resolving Out-Of-Band constraints like OTP codes seamlessly.
