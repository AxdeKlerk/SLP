## 9. Testing

All functionality was tested manually by working through user stories. Testing was carried out in Google Chrome, Edge, Brave and Firefox across desktop and mobile screen sizes. DevTools were used to check responsiveness and console errors. Forms and dynamic elements were tested for validation, correct behaviour, and feedback.

### 9.1 User Stories

#### 9.1.1 Ticket Oversell Guardrail

As a *fan* buying tickets I want *the checkout system to stop me from purchasing more tickets than the event’s available capacity*,  
so that I *cannot buy a ticket to an oversold event with a clear message so that I clearly understand why my order cannot proceed*.

**What Was Tested:**  
I tested that the checkout view prevented users from overselling tickets for an event. As a user, I wanted to see a clear error message if I tried to purchase more tickets than the event’s available capacity, so that I would know the purchase could not go through.

**Acceptance Criteria:**  
- [x] If the quantity of tickets in the basket exceeded the event’s effective capacity, the checkout view blocked the order.  
- [x] An error message was displayed on the basket page, positioned directly above the checkout button.  
- [x] The error message included the specific event name to avoid confusion when multiple events were in the basket.  
- [x] Normal checkout proceeded when the basket quantity was within capacity.  

**Tasks Completed:**  
- [x] Added `capacity` field to `Venue` and `ticket_capacity` field to `Event`.  
- [x] Implemented `effective_capacity()` method in `Event` to enforce venue and event limits.  
- [x] Moved the oversell guardrail check to the top of `checkout_view` so it runs before POST handling.  
- [x] Updated basket template to display error messages to the left of the checkout button.  
- [x] Verified error messages correctly identified the event that exceeded capacity.  

**Notes:**  
Initially, the oversell check did not run because it was inside the `if request.method == "POST":` block, and the *checkout button* triggered a `GET` request. Moving the *guardrail check* above the `POST` block fixed the issue. The error messages now displays correctly, styled in line with the project theme, and gives users immediate feedback before completing an order.

#### 9.2.1 Input Text Visibility Fix

As a *user signing up or logging in* I want *the text I type into input fields to be clearly visible in black* so that I *can easily read what I am entering without confusion*.

**What Was Tested:** 

I tested that the signup and login form input fields displayed black text when users typed into them. I verified that the CSS loaded correctly on *Heroko* and that text remained visible across all input types. As a user signing up or logging in, I wanted the text I typed into input fields to be clearly visible in black so that I could easily read what I was entering without confusion.

**Acceptance Criteria:** 

- [x] Input text in all signup and login fields displayed in black.  
- [x] Placeholder text remained a lighter gray (`#888`) and did not override typed text.  
- [x] CSS changes worked correctly in local development.  
- [x] CSS changes deployed correctly to *Heroku* after running `collectstatic`.  
- [x] No invisible or transparent input text remained.  

**Tasks Completed:** 

- [x] Updated CSS rules for `.page-item input`, `.page-item select`, and `.page-item textarea` with `color: #000000 !important;`.  
- [x] Added focus state overrides to ensure the text stayed black when active.  
- [x] Cleared stale static files from *Heroku*.  
- [x] Ran `python manage.py collectstatic` to regenerate a clean `staticfiles/` directory.  
- [x] Verified the changes by redeploying and testing live on *Heroku*.  

**Notes:** 

At first, the text wasn't invisible because old static files were being served with `color: #0000;` (transparent). This caused the input text to appear blank even though it was being typed. The fix required cleaning out *Heroku*’s cached static files, ensuring `STATIC_URL` was set correctly, and re-running `collectstatic` so the updated `style.css` was deployed. Once that pipeline was corrected, the black text styling worked consistently both locally and on *Heroku*.

## Validation Error – Ticket Capacity Message Errors

**User Story:**  
As a user, I want to be prevented from purchasing more tickets than are available for an event, so that I don’t end up buying tickets for an event that is already at the event's capacity and I want to receive a clear error messages before purchasing my ticket.

**What Was Tested:**

I tested the basket and checkout flow with events tied to venues with limited capacity. I verified that correct error messages were shown when attempting to buy more tickets than available, and that valid purchases went through when quantities matched capacity.

**Acceptance Criteria:**
 
- [x] A user can add tickets up to the venue/event capacity without errors.  
- [x] A user receives an error if the basket quantity exceeds available tickets.  
- [x] Error message shows correct remaining tickets.  
- [x] The checkout is blocked when overselling tickets.  
- [x] The checkout proceeds when basket quantities exactly match remaining tickets.  

**Tasks Completed:**

- [x] Fixed `@property` usage for `tickets_sold` and `effective_capacity`.  
- [x] Added logic to calculate `remaining = capacity - sold`.  
- [x] Updated error message to display the correct number of tickets left.  
- [x] Removed redundant "event fully booked" block so exact capacity orders succeed.  
- [x] Confirmed messages only trigger when overselling occurs.  

**Notes:** 
 
During testing, I confirmed that the bug was not with template rendering but with the logic in `checkout_view`. The root cause was treating `@property` methods as callables and mis-handling the condition when basket quantities equaled capacity. After fixing, the flow correctly distinguishes between valid and invalid ticket requests.  

## Invalid Application ID Error

**User Story:**

As a **developer**, I wanted to **render the Square card input in my checkout page** so that I **could generate a token from a sandbox card and confirm the frontend to backend tokenisation flow worked correctly**.

**What Was Tested:**

I tested that the *Square* Web Payments SDK loaded correctly, that the application ID and location ID passed from *Django* to the frontend were in the right format, and that the card input rendered without errors. The user story was considered complete when a sandbox card could be entered, tokenised, and successfully posted to the backend.

**Acceptance Criteria:** 

- [x] The *Square* SDK script loaded with status 200.  
- [x] The application ID in the browser console displayed as `sandbox-sq0idb-...` without unicode escapes.  
- [x] The card input rendered inside the `#card-container` div.  
- [x] No `InvalidApplicationIdError` appeared in the console.  
- [x] Clicking the *Generate Token* button returned a token and updated the status message on screen.  
- [x] The *Django* backend logged the received token and amount.  

**Tasks Completed:**  

- [x] Removed the `|escapejs` filter from the template and replaced it with `|escape` in the `data-app-id` and `data-location-id` attributes.  
- [x] Reloaded the checkout page and checked that the IDs displayed correctly in console logs.  
- [x] Verified that the *Square* card input rendered correctly in the browser.  
- [x] Entered a *sandbox* test card and clicked the *Generate Token* button.  
- [x] Confirmed token and amount were posted to the backend and logged.  

**Notes:** 

The error occurred because `|escapejs` converted dashes (`-`) into unicode escapes (`\u002D`), which broke the application ID format expected by *Square*. By switching to `|escape`, the IDs were passed in raw format to the *HTML* attributes and the SDK accepted them. This proved the tokenisation flow worked correctly once the correct filter was used.

#### Basket Quantity Clamping

**User Story:**

As a **developer**, I want **the basket to only allow item quantities between 1 and 9** so that **the system is not broken by invalid or malicious inputs**.

**What Was Tested:** 

I tested the basket handlers to ensure that if a user tries to add or update an item with a quantity below 1 or above 9, the backend automatically corrects the value. This ensures the basket is safe from tampered form submissions or direct POST requests.

**Acceptance Criteria:**

- [x] If a user tries to set quantity to 0, it is corrected to 1.  
- [x] If a user tries to set quantity to a negative number, it is corrected to 1.  
- [x] If a user tries to set quantity to greater than 9, it is corrected to 9.  
- [x] Event items cannot exceed a quantity of 9, even if repeatedly added.  
- [x] Merch items cannot exceed a quantity of 9, regardless of form tampering.  
- [x] Basket totals calculate correctly after the clamping logic is applied.  

**Tasks Completed:** 

- [x] Added clamp logic (`if` statement) in `add_merch_to_basket`.  
- [x] Added clamp logic (`if` ststement) in `update_basket_item`.  
- [x] Updated `add_event_to_basket` so increments cannot exceed 9.  
- [x] Manually tested with valid and invalid inputs.  
- [x] Confirmed basket pages display corrected quantities.  

**Notes:**  

During testing I confirmed that invalid inputs (0, -5, 20, etc.) cannot be accepted. The basket automatically enforces a minimum of 1 and a maximum of 9 for all items. This prevents malicious or accidental misuse and ensures stable basket totals.

#### Proceed to Payment Button Routing

**User Story:**

As a **user**, I want the **Proceed to Payment button on my profile page to take me directly to the checkout page** so that I can **complete payment for my selected order**.

**What Was Tested:** 

I tested whether the *Proceed to Payment* button correctly redirected from the profile page to the checkout page. The expected outcome was that clicking the button would resolve the `payments:payment_checkout` URL and load the checkout view.

**Acceptance Criteria:** 

- [x] The *Proceed to Payment* button on the profile page uses the correct namespaced URL (`payments:payment_checkout`).  
- [x] Clicking the button redirects to `/payments/checkout/`.  
- [x] The checkout page loads without errors.  
- [x] No `NoReverseMatch` errors appear in the server logs.  

**Tasks Completed:**

- [x] Updated the template to use `{% url 'payments:payment_checkout' %}`.  
- [x] Restarted the server to ensure URL changes were picked up.  
- [x] Verified redirection worked by clicking the button in the browser.  
- [x] Checked server logs to confirm no routing errors occurred.  

**Notes:**

The error was caused by omitting the `payments:` namespace in the template. Once corrected, *Django* resolved the URL properly, and the button redirected to the checkout page as expected.

#### Delete Selected Orders

**User Story** 

As a **logged-in user**, I want to **be able to select one or more pending orders from my profile page and delete them**, so that I can **remove orders I no longer wish to keep**.

**What Was Tested**

- Confirmed that the profile page shows checkboxes next to each order in progress.  
- Verified that selecting one order and clicking *Delete Selected* removes only that order.  
- Verified that selecting multiple orders and clicking *Delete Selected* removes all selected orders.  
- Verified that clicking *Delete Selected* with no orders ticked shows the error message “No orders selected”.  
- Confirmed that the success and error messages only display on the profile page and not on the basket page.  

**Acceptance Criteria** 

- [x] Each order in progress has a checkbox.  
- [x] Only checked orders are deleted.  
- [x] Error message displays if no orders are selected.  
- [x] Success message displays with the number of orders deleted.  
- [x] Messages appear only on the profile page.  

**Tasks Completed** 

- [x] Replaced hidden inputs with checkboxes in the profile template.  
- [x] Wrapped all orders in a single form for bulk actions.  
- [x] Updated `bulk_order_action` view to filter only selected IDs.  
- [x] Added `extra_tags="orders"` so delete messages only appear on the profile page.  
- [x] Verified end-to-end flow manually in the browser.  

**Notes** 
 
Initially, all orders were being deleted because hidden inputs sent every order ID to the backend regardless of selection. This was fixed by switching to checkboxes and handling only checked values. Messages were also showing up incorrectly in the basket view, which was resolved by adding message tags (`extra_tags="orders"`) and filtering them in `profile.html`.

## Search Function Variation Testing

**User Story:**  
As a **user**, I wanted to **search for artists and venues by partial names or even single letters** so that I **could easily find all bands and venues matching my query** (for example, searching "black" or just the letter "b").

**What Was Tested:** 

I tested the updated search function to confirm that typing part of a name (like "black") or a single letter (like "b") returned all matching artists and venues instead of just one.

**Acceptance Criteria:** 

- [x] Searching "black" should return all artists with "black" in their name.  
- [x] Searching with a single letter (e.g., "b") should return all artists and venues containing that letter.  
- [x] Multiple results should display stacked correctly using the `_artist_detail_block.html` and `_venue_detail_block.html` template.  
- [x] Search results should be ordered alphabetically by name.  
- [x] If no matches exist, a clear "No artists found" message should appear.  

**Tasks Completed:** 

- [x] Updated `views.py` to use `.filter()` instead of `.first()`.  
- [x] Added `order_by("name")` to ensure results are ordered consistently.  
- [x] Modified `search_results.html` to loop over all matches with `{% for artist in artist_results %}` and `{% for venue in venue_results %}`.  
- [x] Verified partial matches and single-letter searches return the correct results.  
- [x] Confirmed no results message appears when there are no matches.  

**Notes:**
  
This test confirmed that the search now behaves like a real search engine, listing all valid results instead of just one. The change from `.first()` to `.filter()` fixed the issue and ensured a better user experience when searching by variations or letters.

## Payment Link API

**User Story:** 

As a **user**, I wanted to **be redirected to a Square checkout page when I clicked “Proceed to Payment” from my profile**, so that I **could complete my order securely**.

**What Was Tested:**

I tested the new *Square* payment integration flow, ensuring that pressing “Proceed to Payment” from the profile page generated a *Square*-hosted checkout link and redirected me correctly. This confirmed that the API call was working with the sandbox environment.  

**Acceptance Criteria:**  

- [x] Clicking “Proceed to Payment” from the profile page sends a request to *Square*.  
- [x] *Square* responds with `200 OK` and returns a valid `payment_link.url`.  
- [x] *Django* redirects the user to the *Square* sandbox checkout page.  
- [x] The local `Order` record saves the `square_order_id` for `webhook mapping`.  
- [x] No `401 Unauthorized` errors occur once the payload uses `quick_pay`.  

**Tasks Completed:** 

- [x] Added `square_order_id` field to `Order` model and migrated.  
- [x] Updated `bulk_order_action` to save the *Square* `order_id`.  
- [x] Replaced invalid `"order": {...}` payload with `"quick_pay": {...}` payload.  
- [x] Verified sandbox checkout flow works end-to-end with debug logs.  

**Notes:** 

At first, *Square* returned `401 Unauthorized` because the payload was structured incorrectly with `"order"`. Switching to `"quick_pay"` unlocked the API and returned the correct payment link. With the new mapping field added, orders can now be linked back to their *Square* order IDs. 

## Webhook Verification

**User Story:** 

As a **developer**, I wanted to **confirm that my webhook endpoint correctly verified *Square*’s signature** so that **only legitimate events from *Square* could trigger order updates**.

**What Was Tested:**

I tested the `webhook endpoint` by sending test `webhook` events from the *Square Sandbox* dashboard and observing how *Django* verified the signature, handled the event, and responded to Square.  

**Acceptance Criteria:** 

- [x] `Webhook` receives `POST` requests from *Square*.  
- [x] Header `x-square-hmacsha256-signature` is read correctly using `request.META`.  
- [x] Signature verification includes the `HTTPS URL` and request body.  
- [x] Matching signatures return `200 OK`.  
- [x] Mismatched signatures return `400 Bad Request`.  

**Tasks Completed:** 

- [x] Replaced `request.headers` with `request.META` for signature retrieval.  
- [x] Adjusted URL signing to use `https://` instead of `http://`.  
- [x] Added debug print statements for verification output.  
- [x] Successfully verified signature match with a `200 OK` response.  

**Notes:** 

At first, every `webhook` attempt failed with `Signature mismatch`. I confirmed the correct `SQUARE_SIGNATURE_KEY` was loaded but found that *Square* signs the `HTTPS URL` + body, not just the body. After adjusting the URL and signature retrieval, the `webhook` validated correctly, confirming a secure link between *Square* and *Django*.

#### 10.1.8 Order Status Update via Square Webhook

**User Story:**

As a **user**, I want **my order status to automatically update to “paid” once my *Square* payment completes**, so that I **know my transaction has been confirmed**.

**What Was Tested:** 

The `webhook` connection between *Square* and *Django* was tested to confirm that completed *Square* payments trigger a corresponding status update in the *Order* model.

**Acceptance Criteria:**

[x] `Webhook` endpoint correctly receives `payment.created` event  
[x] *JSON* payload is parsed successfully without errors  
[x] *Order* model includes both `square_order_id` and `square_payment_id` fields  
[x] Matching order is found and updated to `"paid"` when payment status is `"COMPLETED"`  
[x] Duplicate `webhook` events are safely ignored  
[x] Successful `200 OK` response returned from `webhook` endpoint  

**Tasks Completed:**

[x] Added `square_payment_id` and `square_order_id` to the *Order* model  
[x] Migrated database to include new fields  
[x] Modified `webhook` logic to update `order status` based on *Square* payload  
[x] Created valid *JSON* test file `test_payment.json`  
[x] Tested `webhook` locally using `curl.exe` and confirmed database updates  
[x] Verified `order.status` changed to `"paid"` and `square_payment_id` stored correctly  

**Notes:**

During initial tests, `PowerShell` altered *JSON* formatting, causing `JSONDecodeErrors`. Switching to `--data-binary` preserved the *JSON* structure. After model updates and correct test data setup, `webhook` responses returned `“OK”`, and order status updated successfully. This completed the full payment confirmation loop between *Square* and *Django*.

#### 10.1.8 Order Status Update via Square Webhook

**User Story:**

As a **user**, I want **my order status to automatically update to “paid” once my *Square* payment completes**, so that I **know my transaction has been confirmed**.

**What Was Tested:**

The *Square* `webhook` was tested to confirm that payment events successfully update the associated *Order* in the database and that duplicate `webhook` events are ignored.

**Acceptance Criteria:**

[x] `Webhook` receives and logs incoming *Square* events  
[x] *JSON* payload parses without error  
[x] Matching order found using `square_order_id`  
[x] Order status updates to `"paid"` when payment status is `"COMPLETED"`  
[x] Duplicate `webhook` events are ignored  
[x] `200 OK` response returned successfully  

**Tasks Completed:**

[x] Added `square_order_id` and `square_payment_id` fields to *Order* model  
[x] Created valid `test_payment.json` payload  
[x] Disabled signature verification for local testing  
[x] Sent test payload using `curl.exe`  
[x] Verified `Order.status` changed to `"paid"` and `square_payment_id` recorded  
[x] Re-tested `webhook` and confirmed duplicate event correctly ignored  

**Notes:** 

Testing confirmed the `webhook` processes live payment events correctly and ignores repeated notifications. The only remaining step before production deployment is to re-enable signature verification to validate real *Square* `webhook` requests once running on *Heroku*.

#### Square Webhook Integration

**User Story:** 

As a **site owner**, I want **my *Django* application to securely receive and process payment webhooks from *Square***, so that **order statuses automatically update to “paid” when payments are completed**.

**What Was Tested:** 

I tested the end-to-end `webhook integration` between *Square* and *Django*. This included verifying that the `webhook endpoint` accepts real `POST` requests, validates the *Square* signature correctly, parses the payload safely, updates orders to “paid” only when payment status is `"COMPLETED"`, and ignores duplicates or unmatched order IDs.  

**Acceptance Criteria:** 

[x] The `webhook endpoint` accepts `POST` requests from *Square* via HTTPS.  
[x] Signature verification correctly matches the *Square* `HMAC-SHA256` value.  
[x] `Webhook` events with invalid signatures return a `400 Bad Request`.  
[x] Payment events with `status: COMPLETED` update the matching order to “paid.”  
[x] Duplicate payment events are safely ignored with a `200 response`.  
[x] Non-matching order IDs are logged and ignored without breaking the endpoint.  
[x] Unknown event types return `{"status": "ignored"}` with `200 OK`.  
[x] No `500 errors` occur during `webhook` testing.  

**Tasks Completed:**

[x] Added imports for `JsonResponse` and `HttpResponseBadRequest`.  
[x] Implemented `@csrf_exempt` and `@require_POST` decorators.  
[x] Re-enabled signature verification using `HMAC-SHA256`.  
[x] Forced HTTPS URL reconstruction for accurate signature comparison.  
[x] Added detailed console logging for event type, order ID, and payment ID.  
[x] Implemented logic to update order status to “paid” on `COMPLETED` events.  
[x] Added duplicate event protection.  
[x] Tested successfully using both `curl` and real *Square* test events through *ngrok*.  

**Notes:** 

During testing, *Square* returned a “payment.created” event with status `"APPROVED"`, which did not yet trigger an order update (correct behaviour). When the same event reached `"COMPLETED"`, the order was marked as “paid” and duplicate `webhook` calls were ignored. This confirms that *Django* and *Square* are fully synchronised, the` webhook` verification is secure, and the system is production-ready.

#### Square Payment Verification (Admin Action)

**User Story:**

As a **site owner**, I want to **verify payment statuses directly from *Django Admin* by checking *Square’s* records**, so that I can **confirm completed transactions even if a webhook fails**.

**What Was Tested:** 

I tested the new *Verify with Square* admin action to ensure it updates each order’s `payment_status` and `verified_on` fields correctly.  
A mock mode was used for local testing, simulating *Square* responses such as `APPROVED`, `COMPLETED`, and `CANCELED`.  
I also confirmed that manual entry of fake payment IDs in the admin form saved properly and displayed in the Orders list view.

**Acceptance Criteria:** 

[x] Orders with a `square_payment_id` can be selected and verified through an admin action.  
[x] The action updates `payment_status` and `verified_on` without errors.  
[x] Orders without a `square_payment_id` are safely skipped with an admin message.  
[x] Admin messages confirm each order’s verification result.  
[x] The action works in mock mode for local testing.  
[x] The admin form allows editing of `square_payment_id` when `readonly_fields` are adjusted for testing.  
[x] No `500` or `FieldError` exceptions occur during saving.  
[x] Verified data appears in `list_display` columns in the Orders table.

**Tasks Completed:**  

[x] Added `payment_status` and `verified_on` fields to the *Order* model.  
[x] Updated *OrderAdmin* with new columns, filters, and admin action.  
[x] Added the `verify_with_square()` admin action function using the *Square* Payments API endpoint.  
[x] Implemented mock mode using *Python*’s `random` module for local testing.  
[x] Fixed admin field editability by removing `square_payment_id` from `readonly_fields`.  
[x] Verified success messages and database updates in *Django* Admin.

**Notes:** 

The verification action successfully updated `payment_status` and `verified_on`, while the order’s local `status` remained “pending” (expected behaviour).In production, *Square’s* `webhook`will update `status` automatically when a `payment.completed` event is received, keeping both systems synchronized.

#### Square Sandbox Order Creation and Webhook Verification

**User Story:** 

As a **site owner**, I want **my checkout process to automatically create *Square* orders and payments in the sandbox environment** so that I can **verify real-time payment updates before going live**.

**What Was Tested:**

I tested the full end-to-end workflow in the *Square Sandbox*:
1. A user completes checkout in *Django*.
2. *Django* creates a matching *Square* order and payment via the `/v2/orders` and `/v2/payments` endpoints.
3. *Square* sends `payment.created` and `payment.updated` webhook events.
4. *Django* receives the `webhooks`, verifies signatures, and updates the local order status to `"paid"`.

**Acceptance Criteria:** 

[x] Local order successfully created without IntegrityError.  
[x] *Square* order and payment created in sandbox.  
[x] `Webhooks` received for both `payment.created` and `payment.updated`.  
[x] `Webhook` verification passes signature check.  
[x] *Django* updates local order `status` to `"paid"` when `COMPLETED`.  
[x] `square_order_id` and `square_payment_id` saved correctly.  
[x] Logs confirm successful synchronization end-to-end.

**Tasks Completed:**

[x] Restored `order_type` field with default `"event"`.  
[x] Faked the duplicate migration to sync schema.  
[x] Added *Square* API calls to `basket_checkout()` for order and payment creation.  
[x] Verified `webhook` processing updates order status correctly.  
[x] Confirmed Square IDs display in *Django* Admin.  

**Notes:**

This test confirmed full sandbox functionality: order creation, payment simulation, and `webhook` synchronization. The integration is now production-ready, requiring only a credential switch to live keys on *Heroku*.

#### Order Summary Event Display

**User Story:**

As a **user**, I want to **see clear and accurate details of my event orders in the checkout and payment summary**, so I can **confirm I’m paying for the correct gig before completing my purchase**.

**What Was Tested:**

The order summary section on the checkout and payment pages was reviewed to ensure event names display correctly. The summary should no longer show “None” for events when the optional `title` field is blank.

**Acceptance Criteria:** 

[x] Event orders display the full event string (artist, venue, and date).  
[x] Merch items continue to display correctly.  
[x] No “None” or blank text appears in the summary.  
[x] The output format matches the `__str__()` of the Event model.

**Tasks Completed:** 

[x] Identified that the template referenced `item.event.title`, which can be `None`.  
[x] Replaced it with `item.event` to use the Event model’s `__str__()` output.  
[x] Verified rendering shows correct event name and details.  
[x] Committed fix to repository.

**Notes:** 
 
This fix ensures future event listings remain consistent even if the optional `title` field isn’t used.  
Django’s automatic call to the model’s `__str__()` provides a safe fallback for display logic.
