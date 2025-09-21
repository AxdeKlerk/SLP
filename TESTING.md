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
