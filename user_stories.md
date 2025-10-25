### Extracted User Stories (in order)

### 4.2.1 Core Epic  

#### 4.2.1.1 Site Identification  
User Story:  
As a **user** I want to **land on the website and immediately recognise that it is for a rock and metal music promotion company** so that I **know I am in the right place**.  

#### 4.2.1.2 Navigation  
User Story:  
As a **user** I want to **be able to navigate between Home, About, Event, Merch, Contact Form and Basket** so that I **can reach any section quickly**.  

#### 4.2.1.3 Search  
User Story:  
As a **user** I want to **be able to search for artists, merch and venues** so that I **can navigate quickly to my selected choice**.  

#### 4.2.1.4 Contact Form  
User Story:  
As a **user** I want to **contact the promotions company** so that **my query reaches the right place**.  

#### 4.2.1.5 Footer  
User Story:  
As a **user** I want to **see a basic footer with copyright information** so that I **can know where the end of the page is by the consistent copyright protection displayed beneath**.  

#### 4.2.1.6 Base Template  
User Story:  
As a developer I want a reusable base.html template so that all pages share the same layout, styling, and design consistency.  

---

### 4.2.2 Products Epic  

#### 4.2.2.1 Event Listings  
User Story:  
As a **user** I want to **view all upcoming events** so that I **can decide which ones to attend**.  

#### 4.2.2.2 Event Detail Page — Ticket Oversell Guardrail  
User Story:  
As a **fan buying tickets** I want **the checkout system to stop me from purchasing more tickets than the event’s available capacity** so that I **cannot buy a ticket to an oversold event with a clear message so that I clearly understand why my order cannot proceed**.  

#### 4.2.2.3 Ticket Availability Tracking — Validation Error Message  
User Story:  
As a **user**, I want to **be prevented from purchasing more tickets than are available for an event**, so that I **don’t end up buying tickets for an event that is already at the event's capacity and I want to receive a clear error message before purchasing my ticket**.  

#### 4.2.2.4 Roxoff Page & Event Tickets  
User Story:  
As a **user**, I want to **access the Roxoff page** so that **I can easily view and purchase tickets for upcoming events promoted under the Roxoff brand**.  

---

### 4.2.3 Basket Epic  

#### 4.2.3.1 Add to Basket  
User Story:  
As a **user**, I want to **add event tickets or merchandise to my basket** so that **I can purchase them later**.  

#### 4.2.3.2 View Basket  
User Story:  
As a **user**, I want to **view my basket** so that I **can see the items I intend to purchase**.  

#### 4.2.3.3 Update Basket — Basket Quantity Clamping  
User Story:  
As a **developer**, I want **the basket to only allow item quantities between 1 and 6** so that **the system is not broken by invalid or malicious inputs**.  

#### 4.2.3.4 Remove from Basket  
User Story:  
As a **user**, I want **to delete items from my basket** so that I **don’t purchase items I no longer want**.  

#### 4.2.3.5 Basket Totals  
User Story:  
As a **user**, I want to **see my basket total** so that I **know the total cost before checkout**.  

---

### 4.2.4 User Epic  

#### 4.2.4.1 Add Required Email Field to Sign Up  
User Story:  
As a **new user**, I want to **provide my email address during registration** so that I **can receive receipts and e-tickets linked to my account**.  

#### 4.2.4.2 Sign Up — Input Text Visibility Fix  
User Story:  
As a **user signing up or logging in** I want **the text I type into input fields to be clearly visible in black** so that I **can easily read what I am entering without confusion**.  

#### 4.2.4.3 Log In  
User Story:  
As a **registered user**, I want to **log in** so that I **can access my account and complete purchases**.  

#### 4.2.4.4 Password Reset  
User Story:  
As a **registered user**, I want to **be able to reset my password if I forget it** so that I **can regain access to my account**.  

#### 4.2.4.5 Log Out  
User Story:  
As a **logged in user**, I want to **log out** so that **my account is secure when I leave the site**.  

#### 4.2.4.6 Profile — Delete Selected Orders  
User Story:  
As a **logged-in user**, I want to **be able to select one or more pending orders from my profile page and delete them**, so that I **can remove orders I no longer wish to keep**.  

#### 4.2.4.7 Email Confirmations (Backlog – Not MVP)  
User Story:  
As a **registered user**, I want to **receive email confirmations** so that I can **verify my account and trust the platform**.  

#### 2.4.4.8 Order Confirmation Page  

As a **user**, I want to **see an order confirmation page after completing my payment** so that I can **be sure my order has been successfully processed and view a summary of my purchase**.  

#### 2.4.4.9 Order History in Profile  

As a **logged-in user**, I want to **view my past orders in my profile page** so that I can **keep track of my purchase history and review order details at any time**.

---

### 4.2.5 Checkout & Payments Epic  

#### 4.2.5.1 Checkout Page — Proceed to Payment Button Routing  
User Story:  
As a **user**, I want the **""Proceed to Payment"" button on my profile page to take me directly to the checkout page** so that I **can complete payment for my selected order**.  

#### 4.2.5.2 Order Summary Event Display  
User Story:  
As a **user**, I want to **see clear and accurate details of my event orders in the checkout and payment summary** so I can **confirm I’m paying for the correct gig before completing my purchase**.  

#### 4.2.5.3 Delivery and Booking Fees Carry Over to Order Summary  
User Story:  
As a **user**, I want **delivery and booking fees shown in my basket to be accurately carried over to my checkout summary** so that I **always see the correct final total before payment**.  

#### 4.2.5.4 Checkout Summary Fee and Total Calculations  
User Story:  
As a **user**, I wanted the **checkout summary to clearly display item costs including booking and delivery fees**, so that I can **understand exactly how my total is calculated before payment**.  

#### 4.2.5.5 Checkout and Payment Summary Totals  
User Story:  
As a **user**, I wanted to **see accurate per-item totals that include all booking and delivery fees on both the checkout and payment summary pages** so that I can clearly understand the full cost before completing my order.  

#### 4.2.5.6 Basket and Checkout Totals Calculation  
User Story:  
As a **user**, I want the **basket and checkout totals to include the correct booking and delivery fees for each item** so that I can **see accurate costs before payment**.  

#### 4.2.5.7 Delivery Charge Message  
User Story:  
As a **user**, I want to **clearly see how delivery costs are calculated when buying multiple merch items** so that I **understand why my delivery fee changes at checkout**.  

#### 4.2.5.7 Payment Integration and Deployment Testing  
User Story:  
As a **user**, I want to **complete a secure checkout using the *Square* payment form** so that I can **confidently pay for my order online**.  

---

### 4.2.6 Webhooks & Integrations Epic  

#### 4.2.6.1 Invalid Application ID Error  
User Story:  
As a **developer**, I wanted to **render the *Square* card input in my checkout page** so that I **could generate a token from a sandbox card and confirm the frontend to backend tokenisation flow worked correctly**.  

#### 4.2.6.2 Payment Link API  
User Story:  
As a **user**, I wanted to **be redirected to a *Square* checkout page when I clicked “Proceed to Payment” from my profile**, so that I **could complete my order securely**.  

#### 4.2.6.3 Webhook Verification  
User Story:  
As a **developer**, I wanted to **confirm that my webhook endpoint correctly verified *Square*’s signature** so that **only legitimate events could trigger updates**.  

#### 4.2.6.4 Order Status Update via Square Webhook  
User Story:  
As a **user**, I want **my order status to automatically update to “paid” once my *Square* payment completes**, so that I **know my transaction has been confirmed**.  

#### 4.2.6.5 Square Webhook Integration  
User Story:  
As a **site owner**, I want **my *Django* application to securely receive and process payment webhooks from *Square***, so that **order statuses automatically update to “paid” when payments are completed**.  

#### 4.2.6.6 Square Payment Verification (Admin Action)  
User Story:  
As a **site owner**, I want to **verify payment statuses directly from *Django* Admin by checking *Square*’s records**, so that I can **confirm completed transactions even if a webhook fails**.  

#### 4.2.6.7 Square Sandbox Order Creation and Webhook Verification  
User Story:  
As a **site owner**, I want **my checkout process to automatically create *Square* orders and payments in the sandbox environment** so that I can **verify real-time payment updates before going live**.  

---

### 4.2.7 DevOps Epic  

User Story:  
As a **developer**, I want to **deploy the application to *Heroku*** so that **users can access the live site**.  

#### 4.2.7.2 400 Error Page  
User Story:  
As a **user**, I want to **see a friendly 400 error page when I make a bad request** so that **I am not shown a confusing error message**.  

#### 4.2.7.3 500 Error Page — Custom 404 and 500 Pages with Back Navigation  
User Story:  
As a **user**, I want to **see branded and consistent error pages when something goes wrong, with a back button that takes me to my previous page**, so I **don’t lose my place on the site**.  