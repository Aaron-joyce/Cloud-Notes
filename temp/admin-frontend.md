# Admin Frontend

## 1. External Libraries/Packages Used

This Next.js 14+ (App Router) admin frontend relies on the following major dependencies (from `package.json`):
- **axios**: Used in frontend service handlers (e.g., `admin.service.ts`) to communicate with the REST API backend.
- **clsx & tailwind-merge**: Utilities for constructing and conditionally merging Tailwind CSS class strings cleanly.
- **framer-motion**: Utilized for rich UI animations, page transitions, and smooth interactive behaviors.
- **helmet**: Secure HTTP headers integration on the client/frontend proxy level.
- **js-cookie**: Handles JWT and session state storing client-side to persist logins across page refreshes.
- **lucide-react**: Lightweight icon library provisioning UI icons (e.g., `<Users>`, `<FileText>`, `<CheckCircle>`).
- **react-hot-toast**: For rendering push notifications and feedback toasts upon operations like application approvals.
- **next, react, react-dom**: Core foundation rendering Server and Client components via Next JS.

---

## 2. Each Function and its Working by File

The frontend leverages a component-based structure relying on Next JS's file-system routing. Functions here relate to the functional React components orchestrating views.

### `app/page.tsx` & `app/layout.tsx`
- **Working**: Acts as the root routing redirector usually aiming towards `/login` or `/dashboard` based on authentication context. `layout.tsx` injects global providers (`AuthContext`, `SocketProvider`) encapsulating children components.

### `app/login/page.tsx`
- **Working**: Authenticates admins capturing usernames and passwords. Submits payload via axios `adminLogin()` service. Upon successful response, saves cookie/token state and routes admin natively to `/dashboard`.

### `app/dashboard/page.tsx`
- **Working**: Client Component that fetches aggregation data (`stats`, `distribution`, `recentApplications`) via `getAdminDashboard()`. Re-renders metrics within `DistributionCard` and animated statistic cards (`Users`, `Pending`, `Certificates`, `Slots`).

### `app/applications/page.tsx`
- **Working**: The core workflow manager. Employs `ApplicationsList` mapping internal arrays via the `ApplicationItem` abstraction. Facilitates Approve, Reject, and Bulk actions sending respective IDs to the mutation endpoints.

### `app/certificates/page.tsx`
- **Working**: Iterates over approved application structures rendering `CertificateCard`s. Contains modal overlays providing "Preview" behaviors of railway slips.

### `app/slots/page.tsx`
- **Working**: Handles administrative assignment/generation capabilities. Captures time periods parsing them into `generateSlots()` pushing mass availability schedules to the Postgres DB logic.

### `app/students/page.tsx`
- **Working**: Renders `StudentTable` wrapping rows in `StudentRow`, facilitating complex search and sorting functionalities over users using `StudentSearch`.

### `app/audit-logs/page.tsx`
- **Working**: Provides historical trace tables logging all significant mutative operations performed under the identity of specific administrators.

### `context/AuthContext.tsx`
- **Working**: Provides React global Context wrapper caching user identity tokens, propagating `isAuthenticated` states seamlessly through the DOM tree.

### `components/applications/`
- **Working**: Decoupled rendering elements.
  - `ApplicationItem.tsx`: Maps individual properties into DOM table rows cleanly.
  - `ConcessionCard.tsx` / `RailwayConcessionSlip.tsx`: Render highly stylized UI tickets simulating physical print-outs utilizing static structural templates.

---

## 3. Overall Working 

The Admin Frontend functions as a standard Single Page Application conceptually driven via the Next.js App Router (focusing largely on CSR via `"use client"` blocks). 

**Working Details:**
1. **Inputs:** Admins access the interface locally or over explicit domains. Forms and tables present inputs capable of accepting approvals, bulk updates, pass cancellations, and slot modifications. Search bars accept granular query modifications.
2. **Operations:** Clicking buttons (`Approve`, `Generate`, `Reject`) invokes specific `services/*.ts` Axios methods wrapping endpoints. Once the promise resolves:
   - A success state fires a `react-hot-toast` rendering success notifications.
   - Component states are mutated triggering a re-render to reflect the changed arrays (like dropping an app from `Pending` tabs).
3. **Outputs:** Information streams directly from the backend into the interfaces. `framer-motion` dictates layout shifts aesthetically, displaying analytics distribution via dynamic graphs, and populating tables containing `student` meta entities cleanly and efficiently. Websockets push real-time table syncs natively without explicit poll mechanisms.
