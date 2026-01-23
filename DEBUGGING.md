## 4.1 DEBUGGING LOG
This document has been restructured from my original DEBUGGING.md which listed each bug fix in chronological order, as development progressed. The restructuring only grouped the relevant entries under the 7 headings listed in the table of contents for ease of reference. 


### 4.1 Table of Contents
- [4.1 DEBUGGING LOG](#41-debugging-log)
  - [4.1 Table of Contents](#41-table-of-contents)
  - [4.1.1 FRONTEND / UI](#411-frontend--ui)
    - [4.1.1.1 Offcanvas Navigation Error](#4111-offcanvas-navigation-error)
    - [4.1.1.2 Template Logic — Navbar active state (dropdown parent)](#4112-template-logic--navbar-active-state-dropdown-parent)
    - [4.1.1.3 Navigation Highlight Issue](#4113-navigation-highlight-issue)
    - [4.1.1.4 CSS Layout Bug](#4114-css-layout-bug)
    - [4.1.1.5 Template Logic Bug for Size Dropdown Menu items](#4115-template-logic-bug-for-size-dropdown-menu-items)
    - [4.1.1.6 Template/Context Error](#4116-templatecontext-error)
    - [4.1.1.7 Search Input Responsive Sizing (Mobile) Issue](#4117-search-input-responsive-sizing-mobile-issue)
    - [4.1.1.8 Merch Search Functionality Issue](#4118-merch-search-functionality-issue)
    - [4.1.1.9 Contact Form Email Confirmation and Redirect](#4119-contact-form-email-confirmation-and-redirect)
  - [4.1.2 BACKEND / LOGIC](#412-backend--logic)
    - [4.1.2.1 Logic Bug](#4121-logic-bug)
    - [4.1.2.2 Logic Error for Forgot Username View](#4122-logic-error-for-forgot-username-view)
    - [4.1.2.3 Logic Error](#4123-logic-error)
    - [4.1.2.4 Logic Error](#4124-logic-error)
  - [4.1.2.5 Email Logic Error](#4125-email-logic-error)
  - [4.1.3 DATABASE CONFIGURATION](#413-database-configuration)
    - [4.1.3.1 Database Configuration Error](#4131-database-configuration-error)
    - [4.1.3.2 Database Integrity and Square Order Sync](#4132-database-integrity-and-square-order-sync)
  - [4.1.4 SYSTEM / FRAMEWORKS](#414-system--frameworks)
    - [4.1.4.1 404 \& 500 Template Routing Error](#4141-404--500-template-routing-error)
    - [4.1.4.2 Admin Field and Payment Verification Errors](#4142-admin-field-and-payment-verification-errors)
  - [4.1.5 BASKET / CHECKOUT / PAYMENT LOGIC](#415-basket--checkout--payment-logic)
    - [4.1.5.1 Basket Data Handling Error](#4151-basket-data-handling-error)
    - [4.1.5.2 Basket Size Display Error](#4152-basket-size-display-error)
    - [4.1.5.3 Basket Event Details Error](#4153-basket-event-details-error)
    - [4.1.5.4 Basket Layout / Responsive Error](#4154-basket-layout--responsive-error)
    - [4.1.5.5 AttributeError](#4155-attributeerror)
    - [4.1.5.6 Quantity Clamping Error](#4156-quantity-clamping-error)
    - [4.1.5.7 Ticket Oversell Error Not Displaying](#4157-ticket-oversell-error-not-displaying)
    - [4.1.5.8 Validation Error – Ticket Capacity Message Errors](#4158-validation-error--ticket-capacity-message-errors)
    - [4.1.5.9 Routing Error (Payment Button)](#4159-routing-error-payment-button)
    - [4.1.5.10 Routing Error (Products Namespace)](#41510-routing-error-products-namespace)
    - [4.1.5.11 Calculation Error](#41511-calculation-error)
    - [4.1.5.12 Calculation Error (Checkout Totals)](#41512-calculation-error-checkout-totals)
    - [4.1.5.13 Runtime Error for Checkout and Payment Summary Totals](#41513-runtime-error-for-checkout-and-payment-summary-totals)
    - [4.1.5.14 Basket and Checkout Totals Calculation Runtime Error](#41514-basket-and-checkout-totals-calculation-runtime-error)
    - [4.1.5.15 Navigation Routing Error](#41515-navigation-routing-error)
    - [4.1.5.16 Redirect Loop for Continue Shopping Button](#41516-redirect-loop-for-continue-shopping-button)
    - [4.1.5.17 Continue Shopping Persistent Redirect Fallback Logic](#41517-continue-shopping-persistent-redirect-fallback-logic)
  - [4.1.6 WEBHOOKS \& SQUARE INTEGRATION](#416-webhooks--square-integration)
    - [4.1.6.1 Integration Errors (Square API with Django)](#4161-integration-errors-square-api-with-django)
    - [4.1.6.2 CSRF and Tokenisation Errors](#4162-csrf-and-tokenisation-errors)
    - [4.1.6.3 Invalid Application ID Error](#4163-invalid-application-id-error)
    - [4.1.6.4 Authentication Error](#4164-authentication-error)
    - [4.1.6.5 Webhook Integration Errors](#4165-webhook-integration-errors)
    - [4.1.6.6 Webhook Signature Verification Errors](#4166-webhook-signature-verification-errors)
    - [4.1.6.7 Webhook Authentication Error](#4167-webhook-authentication-error)
    - [4.1.6.8 Webhook Integration Error](#4168-webhook-integration-error)
    - [4.1.6.9 Webhook Validation Error](#4169-webhook-validation-error)
  - [4.1.7 SECURITY \& DEPLOYMENT](#417-security--deployment)
    - [4.1.7.1 Security Bug](#4171-security-bug)
    - [4.1.7.2 Deployment Issue](#4172-deployment-issue)
    - [4.1.7.3 Database Configuration Error (*Heroku*)](#4173-database-configuration-error-heroku)
    - [4.1.7.4 Configuration Error](#4174-configuration-error)
    - [4.1.7.5 Environment Variable Load Failure](#4175-environment-variable-load-failure)
    - [4.1.7.6 Deployment Errors](#4176-deployment-errors)
    - [4.1.7.7 Static Files Cache Error](#4177-static-files-cache-error)
    - [4.1.7.8 Deployment and Payment Integration](#4178-deployment-and-payment-integration)
    - [4.1.8 Project Failure - External Database Dependency Unavailable During Assessment](#418-project-failure---external-database-dependency-unavailable-during-assessment)
  - [4.1.9 Database Configuration and Migration from *Supabase* to *Neon*](#419-database-configuration-and-migration-from-supabase-to-neon)
    - [4.1.9.1 *Supabase* *Postgres* Pause Caused Production Failure](#4191-supabase-postgres-pause-caused-production-failure)
    - [4.1.9.2 *Neon* Schema-Only Migration Resulted in Missing Data](#4192-neon-schema-only-migration-resulted-in-missing-data)
    - [4.1.9.3 *Supabase* Network Inaccessibility Blocked Initial Export](#4193-supabase-network-inaccessibility-blocked-initial-export)
    - [4.1.9.4 *PowerShell* Line Continuation Caused Dump Output to STDOUT](#4194-powershell-line-continuation-caused-dump-output-to-stdout)
    - [4.1.9.5 *Supabase* Internal Schemas Triggered Restore Warnings](#4195-supabase-internal-schemas-triggered-restore-warnings)
    - [4.1.9.6 *Django* Migration State Out of Sync After Restore](#4196-django-migration-state-out-of-sync-after-restore)
    - [4.1.9.7 Explicit Schema Selection Required for *Neon*](#4197-explicit-schema-selection-required-for-neon)
    - [4.1.9.8 Data and *Cloudinary* Verification After Migration](#4198-data-and-cloudinary-verification-after-migration)
  - [4.1.10 Security \& Deployment](#4110-security--deployment)
    - [4.1.10.1 Assessment Failure Initially Misattributed to Code](#41101-assessment-failure-initially-misattributed-to-code)

---

### 4.1.1 FRONTEND / UI

#### 4.1.1.1 Offcanvas Navigation Error
**Bug:**  
The navigation links inside the mobile offcanvas menu would not redirect properly. Clicking them closed the menu but did not trigger navigation, even though the same links in the inline (desktop) menu worked fine.  

**Fix:**  
Removed the `data-bs-dismiss="offcanvas"` attribute from each `<a>` tag inside the offcanvas. This attribute was closing the drawer but also blocking the link’s natural navigation behaviour.  

**Lesson Learned:**  
If links inside a *Bootstrap* offcanvas are meant to load a new page (like *Django* `{% url %}` links), there is no need for `data-bs-dismiss`. The page reload will automatically hide the offcanvas, so adding dismissal attributes can actually break expected link behaviour.  

---

#### 4.1.1.2 Template Logic — Navbar active state (dropdown parent)
**Bug:**  
Initially the `Events` navbar item wasn't staying highlighted once one of the dropdown items were selected. I then hard coded the `Events` navbar item as `active` and realised that the issue was with the relationship between parent and child items.

**Fix:**  
I removed the hard-coded `active` from the parent toggle and marked the parent/children `active`:

`{% if url_name == 'events' or url_name == 'previous_events' %}active{% endif %}` based on the current view name with a request resolver above: `{% with url_name=request.resolver_match.url_name %}` and added the `active` status to *my* css to increase specifity.

**Lesson Learned:**  
Don’t hard-code active on nav items; compute it from the current route. For dropdowns, the parent’s state should reflect child activity (via request.resolver_match.url_name) and keep CSS specific but simple; Bootstrap’s defaults can override you unless your rules target the right elements.

---

#### 4.1.1.3 Navigation Highlight Issue
**Bug:**  
The *Search* navbar item did not stay highlighted when navigating to either the artist or venue detail page (`artist_detail`, `venue_detail`). The expected behavior was for the *Search* tab to be marked active when the user was on these pages, just like the *Events* tab behaves when on related event pages.

**Fix:**  
I identified that the condition checking the *Search* tab for `artist_search` and `venue_search` was incorrect because those were not the actual view names. Instead, the actual view names were `artist_detail` and `venue_detail`. I updated the navbar to use these correct names.

**Lesson Learned:**  
When using `url_name` for template conditions, it’s essential to ensure *I’m* checking against the correct view name. I learned to debug this by printing `url_name` in the template using:

`url_name = {{ request.resolver_match.url_name }}`

This helped *me* verify the actual names *Django* was using for each page. Always ensure the condition matches the exact value of `url_name` for the intended behavior.

---

#### 4.1.1.4 CSS Layout Bug
**Bug:**  
On screens between 576px and 767px, *my* event cards were not centred. The `.row` container was full width, but the `.standard-card` element stayed stuck to the left side. This only happened on small screens because the card had a `max-width` set, which prevented it from stretching to fill the column. Without centring rules, it always aligned left.

**Fix:**  
I discovered that the `.standard-card` CSS had `max-width: 300px;` but no horizontal centring. The card was narrower than its parent column and defaulted to the left. I fixed this by adding `margin-left: auto;` and `margin-right: auto;` to the `.standard-card` CSS so that it stayed centered inside its column.

**Lesson Learned:**  
When using `max-width` on a card inside a Bootstrap column, the card will not center itself automatically. Even if the column is full width, the child element needs `margin: auto` to align correctly. Always check custom CSS rules like `max-width` if a card or element looks offset at certain breakpoints. Although it’s quite basic syntax, panicking about it instead of pausing to think clearly was unhelpful — a good reminder to slow down.

---

#### 4.1.1.5 Template Logic Bug for Size Dropdown Menu items
**Bug:**  
The size dropdown was showing for all merch items, including flags, mugs, and caps. These products do not need size options, but the template always displayed the dropdown. *My* first attempt was to use `{% if merch.category == "flag" %}`, but this failed because the correct model field name was `product_category`. When I later tried to check multiple categories with `in ("flag", "mug", "cap")`, it caused a *Django* `TemplateSyntaxError` because template conditions do not support tuple syntax.

**Fix:**  
I solved the problem by chaining multiple conditions with `or` in the template. This allowed *me* to remove the dropdown for flags, mugs, and caps, while keeping it for t-shirts and hoodies using a conditional `if` statement.

`{% if merch.product_category == "flag" or merch.product_category == "mug" or merch.product_category == "cap" %}`

**Lesson Learned:**  
The *Django* template language does not support Python tuple syntax in `if` statements. To check multiple values, I must use `or` (or `and`) to chain conditions. It is important to reference the correct model field, in this case the (`product_category`), when testing values. Using the wrong field name will always fail, even if the condition looks correct.

---

#### 4.1.1.6 Template/Context Error
**Bug:**  
The size dropdown wasn’t showing any options in the merch detail page. Clicking the button made the dropdown appear, but it was empty. The issue was that I tried looping with `{% for s in size_choices %}` and using `{{ s }}`, but *my* model’s choices actually return two values `(key, label)`. Because of that, nothing was rendered in the `<ul>`.

**Fix:**  
I updated *my* `MerchDetailView` to pass size_choices into the context. Then in *my* template, I switched from using `{{ s }}` to the correct `{{ key }}` and `{{ label }}`. Finally, I matched the *Size JS* to the same pattern as the *Quantity JS*, so both dropdowns behave consistently.

**Lesson Learned:**  
I need to remember that *Django* model field choices always give back `(key, label)` pairs, not a single value. If I try to loop with the wrong variable, the template will silently fail and look like “nothing happened.” Next time, *I’ll* check what data type a loop is actually returning before writing the template logic, and *I’ll* keep dropdown JS patterns consistent across all fields.

---

#### 4.1.1.7 Search Input Responsive Sizing (Mobile) Issue
**Bug:**  
In mobile view, the search input fields inside the `offcanvas` were far too wide and pushed the layout beyond the screen width. They also expanded even when not active, causing alignment issues.

**Fix:**  
I added specific width constraints within a media query for screens under 768px and adjusted the offcanvas width so it “hugged” the search inputs. The `offcanvas` now expands only when the search is clicked. This ensures inputs stay within the viewport and aligned correctly.

**Lesson Learned:**  
Always test responsive elements both in collapsed and expanded states — *Bootstrap’s* `offcanvas` width doesn’t automatically scale with its contents, so manual sizing adjustments are sometimes necessary.

---

#### 4.1.1.8 Merch Search Functionality Issue
**Bug:**  
The merch search stopped working after introducing form-based searches for artists and venues. Pressing enter on the merch search field no longer redirected to results.

**Fix:**  
I replaced the static `<input>` with a proper form pointing to `{% url 'products:search_view' %}` and used `name="q"` consistently across all fields. Updated the JavaScript `handleMerchSearch()` to handle the same `id="merch-search"` (desktop) and `id="merch-search-mobile"` (mobile)` logic, matching the artist and venue setups. Adjusted `views.py` to detect merch queries and display either multiple results or a single merch item styled like the merch list.

**Lesson Learned:**  
Consistency between input names, form actions, and view logic is key. Even one mismatched `name` or `id` can break a working search feature.

---

#### 4.1.1.9 Contact Form Email Confirmation and Redirect

**Bug:**  
Originally, the contact form used *FormSubmit*, a third-party service that sent messages externally without backend control, from teh working version of *www.searchlightpromotions* website. This meant no confirmation email could be sent to users, and the redirect to the thank-you page was unreliable once switched to *Django* handling.  

**Fix:**  
Replaced the external `FormSubmit` action with a *Django*-based `ContactForm` and `contact_view`. The view now:
- Validates all form inputs using *Django*’s form system.  
- Sends two emails — one to the site owner with full message details, and one to the sender confirming receipt.  
- Redirects to the dedicated **thank-you page** after successful submission.  
Added inline field error handling with brand-styled validation messages using the `.invalid-feedback` class and the red colour `#E63946`.  

**Lesson Learned:**  
Always manage key user interactions like contact forms within *Django* itself to maintain full control over logic, validation, and user feedback. This not only improves reliability but also ensures consistent styling, secure data handling, and a smoother user experience.

--- 

### 4.1.2 BACKEND / LOGIC

#### 4.1.2.1 Logic Bug
**Bug:**  
I noticed that *my* Roxoff event cards were appearing on the Upcoming Gigs page. This wasn’t supposed to happen — Roxoff events should only be shown on their own dedicated template (roxoff.html), not mixed in with regular events.

**Fix:**  
I realised I needed a way to clearly separate Roxoff events from regular ones. So I added a new `event_type` field to the Event model with `regular` and `roxoff` choices. Then I updated the view for the Upcoming Gigs page (events_view) to exclude Roxoff events:

`events = Event.objects.filter(gig_date__gte=today).exclude(event_type='roxoff').order_by('gig_date')`

**Lesson Learned:**  
It’s better to explicitly separate types of events in the model using a dedicated field like `event_type`. That way, filtering them in views is more reliable and readable than trying to guess based on other values like `roxoff_day`. It also makes future development easier, especially if I need more event types later.

---

#### 4.1.2.2 Logic Error for Forgot Username View
**Bug:**  
The forgot username feature did not work. Submitting the form just reloaded the same page and never redirected to the done page. No email was sent to the terminal. After checking the `views.py`, I saw the condition was written as `if request.method == "Post":`. The browser always sends the HTTP method in uppercase (`"POST"`), so this condition never matched. As a result, the code inside never ran.

**Fix:**  
I corrected the case of the request method check to `"POST"`. With this fix, the form submission was processed, the email was printed to the terminal, and the redirect to the `password_reset_done` page worked as expected.

**Lesson Learned:**  
In *Django*, `request.method` is always uppercase. If I use lowercase or mixed case like `"Post"`, the condition will never be true. Always check against `"POST"` for form submissions and `"GET"` for page loads.

---

#### 4.1.2.3 Logic Error
**Bug:**  
When I added a *merch item* to the basket without choosing a size, the size field was saved as empty instead of defaulting to "L". This happened because the hidden input for `size` in `basket_button.html` had no value set, so unless the *JavaScript* updated it after a click, nothing was passed to the backend.

**Fix:**  
I updated the hidden input in `basket_button.html` to include a default value of `"L"`. This meant that if no size was chosen, the basket still received "L" automatically.

`<input type="hidden" name="size" id="selected-size" value="L">`

**Lesson Learned:**  
I learned that hidden inputs should always have a sensible default if they rely on *JavaScript* to change their values. Without the default, the backend will just get blanks when no interaction occurs. Keeping things simple with a fallback avoids unexpected empty data being saved.

---

#### 4.1.2.4 Logic Error
**Bug:**  
Delivery and booking fee charges were not being carried over to the order summary page after checkout. The basket correctly displayed both charges, but the checkout total remained unchanged, only reflecting raw item prices.

**Fix:**  
I rewrote the `basket_checkout` view to mirror the fee logic used in the basket. Added `Decimal`-based calculations for both booking and delivery fees inside the order creation loop:  
`subtotal += line_total + (booking_fee * item.quantity) + delivery_fee`  
This ensured both charges were included in `order.subtotal` and `order.total` before saving.

**Lesson Learned:**  
When performing multi-step calculations across views, always duplicate or abstract shared logic (e.g. into a helper function) so updates remain consistent. The basket and checkout must use identical fee logic to avoid mismatched totals.

---

### 4.1.2.5 Email Logic Error

**Bug:** 
During mentor testing, the payment page could not auto-populate the user’s email address because the sign-up process never required or stored one. Users were able to register without providing an email, which prevented receipts and e-tickets from being delivered after checkout.

**Fix:** 
I created a custom form called `CustomUserCreationForm` that extends *Django*’s default `UserCreationForm` and includes a required `email` field. The new form was imported into the `signup` view and replaced the default form reference. The `signup.html` template was then updated to include the email field between the username and password inputs. Validation messages were confirmed for blank, invalid, and valid entries. Once a user is registered, their email now saves correctly to `User.email` and automatically appears on the payment page using `{{ request.user.email }}`.

**Lesson Learned:**  
Even when using *Django*’s built-in authentication, the default `UserCreationForm` doesn’t collect email addresses by design. If email-based functionality (like receipts or password resets) is part of the workflow, a custom registration form is essential. Extending *Django*’s existing forms is the cleanest way to add required fields without disrupting authentication or introducing a custom user model.

### 4.1.3 DATABASE CONFIGURATION

#### 4.1.3.1 Database Configuration Error
**Bug:**  
The new *Heroku* app was still connected to the *PostgreSQL database* used in a previous project. This led to seeing old user data in the *Django* admin panel, even though the new app was supposed to be starting fresh. The problem occurred because the `DATABASE_URL` in *Heroku* was still pointing to the old *Heroku PostgreSQL* database from the previous project.

**Fix:**  
A brand-new *Supabase* database was created to replace the old *Heroku PostgreSQL* one. The *transaction pooler* connection string was copied from *Supabase* and updated to include the actual password with special characters properly percent-encoded. The connection string was set in *Heroku* and migrations were applied.

**Lesson Learned:**  
Always inspect and update `DATABASE_URL` after setting up a new deployment. Special characters in credentials must be percent-encoded to avoid connection errors.

---

#### 4.1.3.2 Database Integrity and Square Order Sync
**Bug:**  
When running the new *Square* checkout integration, *Django* raised an `IntegrityError` complaining about a `null value in column "order_type"` in the `checkout_order` table. The model no longer contained that field, but the database schema still required it. This caused the order creation process to fail before the *Square* API could be called.

**Fix:**  
I restored the missing `order_type` field to the `Order` model and gave it a default value of `"event"`. Then faked the migration:  
`python manage.py migrate checkout 0003 --fake`

**Lesson Learned:**  
If *Django* reports missing columns, the issue is usually a mismatch between model definitions and existing migrations. Adding a default value or faking the migration is safer than manually altering tables.

---

### 4.1.4 SYSTEM / FRAMEWORKS

#### 4.1.4.1 404 & 500 Template Routing Error
**Bug:**  
Custom error pages were not being displayed. Even though I had created `404.html` and `500.html` templates inside the `config/templates` directory, *Django* continued to serve its default error pages instead.

**Fix:**  
I added custom error handler functions in `config/views.py` for both `404` and `500` pages and then registered them inside `config/urls.py` as follows:  
`handler404 = "config.views.custom_404"`  
`handler500 = "config.views.custom_500"`  
This ensured *Django* used the project-specific templates instead of the defaults.

**Lesson Learned:**  
*Django* will only render custom error templates if global error handlers are defined in `urls.py`. Simply having the HTML files present is not enough; the handlers must explicitly point to their corresponding views.

---

#### 4.1.4.2 Admin Field and Payment Verification Errors
**Bug:**  
The *Django* admin panel blocked editing of *Square* payment IDs for existing orders, and these fields appeared blank during data inspection. This made verifying live payment data impossible.

**Fix:**  
I adjusted `readonly_fields` within the `OrderAdmin` class to temporarily allow editing and inspection of the payment-related fields. I also updated the `list_display` configuration to include `square_order_id` and `square_payment_id` for easier verification.

**Lesson Learned:**  
*Django* admin will not allow editing of `auto_now_add` or restricted fields by default. When debugging or verifying external API data, it’s sometimes necessary to temporarily relax these restrictions — but they should always be re-enabled once testing is complete.

### 4.1.5 BASKET / CHECKOUT / PAYMENT LOGIC

#### 4.1.5.1 Basket Data Handling Error
**Bug:**  
Quantities were not being carried over between basket and checkout pages, and item ordering appeared inconsistent.

**Fix:**  
I updated the logic to explicitly pull `quantity` from the POST data when creating order items and enforced `order_by("id")` on basket queries to maintain consistent ordering.

**Lesson Learned:**  
Explicitly retrieving form data avoids silent losses, and using `order_by()` ensures stable ordering when rendering or processing lists of related items.

---

#### 4.1.5.2 Basket Size Display Error
**Bug:**  
Product sizes were missing or displayed in lowercase within the basket summary.

**Fix:**  
I added the `size` field properly to the basket model and switched to using `get_size_display()` to return the human-readable version of the choice field.

**Lesson Learned:**  
When using model choice fields, always display them with `get_FIELD_display()` to ensure readable labels rather than raw keys.

---

#### 4.1.5.3 Basket Event Details Error
**Bug:**  
Event information was duplicated in the basket display because I was rendering the event both via its `__str__()` method and by referencing individual fields.

**Fix:**  
I simplified the template to render each event field separately (artist, venue, and date), ensuring no double rendering occurred.

**Lesson Learned:**  
Avoid mixing `__str__()` calls with explicit field references in the same context. Decide on one method to maintain consistent, predictable output.

---

#### 4.1.5.4 Basket Layout / Responsive Error
**Bug:**  
The basket layout was inconsistent across different screen sizes. On smaller devices, items stacked unevenly, and spacing broke under certain Bootstrap grid combinations.

**Fix:**  
I implemented a clearer responsive layout using *Bootstrap’s* grid breakpoints (`col-md-6`, `col-lg-4`) and wrapped elements inside `.row` containers to maintain alignment.

**Lesson Learned:**  
When designing for responsiveness, build for mobile first and then progressively enhance for larger screens. Bootstrap grids only align predictably when each child element is correctly nested within a `.row` structure.

---

#### 4.1.5.5 AttributeError
**Bug:**  
A runtime error occurred when calculating totals in the basket view:  
`AttributeError: 'BasketItem' object has no attribute 'price'`.  
This happened because the view attempted to directly access `price`, which is not a stored field.

**Fix:**  
I replaced the direct reference to `.price` with `.line_total`, which correctly computes totals through a property method.  

**Lesson Learned:**  
Avoid assuming attributes exist; rely on defined properties or helper methods. They provide controlled and consistent logic for derived values.

---

#### 4.1.5.6 Quantity Clamping Error
**Bug:**  
Users could manually adjust item quantities to zero, negative numbers, or values exceeding stock limits.

**Fix:**  
I added server-side validation to clamp quantity values between 1 and 9, preventing invalid input regardless of client-side manipulation.

**Lesson Learned:**  
Always enforce critical validation rules on the backend. Frontend checks can be bypassed easily, but backend validation guarantees data integrity.

---

#### 4.1.5.7 Ticket Oversell Error Not Displaying
**Bug:**  
Oversell prevention logic wasn’t working — tickets exceeding capacity did not trigger warnings. The validation was written after a GET request check, so it never executed during POST form submissions.

**Fix:**  
I moved the capacity validation logic above the request-type branching, ensuring the rule runs before any form submission processing.

**Lesson Learned:**  
Always run validation checks before branching by request method in *Django* views. Otherwise, POST requests can skip important validation entirely.

---

#### 4.1.5.8 Validation Error – Ticket Capacity Message Errors
**Bug:**  
The “fully booked” message appeared incorrectly for partially filled events. I had misused `@property` methods as if they were normal callable functions.

**Fix:**  
I corrected the property references and restructured the conditional logic to distinguish between “sold out” and “nearly full” statuses, ensuring accurate messages were shown.

**Lesson Learned:**  
Property decorators remove the need for parentheses when accessing computed fields. Always verify whether a model attribute is a property or method before calling it.

---

#### 4.1.5.9 Routing Error (Payment Button)
**Bug:**  
The “Proceed to Payment” button on the profile page raised a `NoReverseMatch` error. This happened because the URL pattern was namespaced, but I used `{% url 'process_payment' %}` without including the namespace.

**Fix:**  
I corrected the URL reference to `{% url 'payments:process_payment' %}` in the template.

**Lesson Learned:**  
When using namespaced URLs, always include the full namespace in `{% url %}` tags. Forgetting it is a common cause of `NoReverseMatch` errors.

---

#### 4.1.5.10 Routing Error (Products Namespace)
**Bug:**  
Venue search pages were returning 404 errors due to duplicate `include()` statements for the same app at both the root and nested levels of the project’s URL configuration.

**Fix:**  
I removed the redundant include from the root URL patterns and adjusted JavaScript redirect logic accordingly. This ensured only the correct namespace was used.

**Lesson Learned:**  
Keep URL namespaces consistent throughout the project. Duplicate `include()` statements can override expected routes and cause unexpected 404s.

---

#### 4.1.5.11 Calculation Error
**Bug:**  
The basket subtotal displayed correctly, but delivery fees were always charged as a flat £5 regardless of how many items were in the basket.

**Fix:**  
I adjusted the delivery fee logic to apply £5 for the first item and £2.50 for each additional one. This was calculated dynamically within the basket view before rendering totals.

**Lesson Learned:**  
Always multiply delivery or booking fees by quantity and differentiate between first-item and additional-item rates. Hardcoding flat fees can lead to over- or under-charging.

---

#### 4.1.5.12 Calculation Error (Checkout Totals)
**Bug:**  
Booking and delivery fees displayed correctly in the basket but not in the checkout totals. The view reused an older calculation function that ignored these values.

**Fix:**  
I updated the checkout fee calculation logic to use the same helper function as the basket, ensuring identical totals on both pages.

**Lesson Learned:**  
When reusing shared logic across views, centralise calculations into one helper function to prevent desynchronisation between pages.

---

#### 4.1.5.13 Runtime Error for Checkout and Payment Summary Totals
**Bug:**  
Per-item totals on the payment summary excluded booking and delivery fees. The queryset used in the template was being refetched from the database after totals were calculated, losing the attached attributes.

**Fix:**  
I converted the queryset into a list before adding calculated fields. This preserved the data for rendering in the template.

**Lesson Learned:**  
When attaching custom attributes to objects derived from querysets, convert them to lists first. Re-evaluating a queryset resets its objects.

---

#### 4.1.5.14 Basket and Checkout Totals Calculation Runtime Error
**Bug:**  
A `Decimal not callable` runtime error occurred due to parentheses being added after a `Decimal` instance, and the basket item model lacked a compatible `get_line_total()` method. This error occurred because `Decimal` instances cannot be called like functions (e.g. `Decimal()()`), so removing parentheses resolved the issue.

**Fix:**  
I corrected the syntax and ensured both the basket and order item models shared a consistent `get_line_total()` method.

**Lesson Learned:**  
Method naming consistency between models prevents subtle calculation errors. Avoid naming collisions with built-in classes like `Decimal`.

---

#### 4.1.5.15 Navigation Routing Error
**Bug:**  
After completing a payment, clicking “View Basket” redirected to an empty basket even though an order still existed.

**Fix:**  
I added a conditional link to redirect to a new `restore_basket` view that repopulates the basket from pending order data.

**Lesson Learned:**  
Once an order is finalised, basket data is cleared. Providing a “restore” route allows continuity for users wanting to recheck their previous items.

---

#### 4.1.5.16 Redirect Loop for Continue Shopping Button
**Bug:**  
The “Continue Shopping” button on the basket page caused a redirect loop, returning users to the same page instead of the product list.

**Fix:**  
I imported the correct view reference and implemented referrer validation logic, falling back to the product list when no valid HTTP referrer was available.

**Lesson Learned:**  
`HTTP_REFERER` values can point to the same page, causing infinite loops. Always include a safe fallback redirect.

---

#### 4.1.5.17 Continue Shopping Persistent Redirect Fallback Logic
**Bug:**  
After logging out and logging back in, session data was lost, and users were redirected incorrectly when continuing shopping from an incomplete basket.

**Fix:**  
I enhanced fallback logic to inspect basket contents before deciding where to redirect, ensuring behaviour remained consistent regardless of session state.

**Lesson Learned:**  
Session data can reset on logout, so persistent state should be inferred from database models when continuity is required.

### 4.1.6 WEBHOOKS & SQUARE INTEGRATION

#### 4.1.6.1 Integration Errors (Square API with Django)
**Bug:**  
The wrong *Square SDK* version was installed and used incorrectly, which caused method mismatches and invalid imports when processing payments.

**Fix:**  
I reinstalled the correct SDK version, verified the available classes using `dir()`, and replaced the broken imports. I then corrected usage of the `Square` class and the `list()` method while adjusting the response-handling logic to align with the updated SDK.

**Lesson Learned:**  
Always check which SDK version is installed before writing integration code. Method names and response structures often differ between releases, and outdated imports can silently break logic.

---

#### 4.1.6.2 CSRF and Tokenisation Errors
**Bug:**  
Card tokenisation repeatedly failed with console errors caused by an insecure context, incorrect route, and a missing CSRF token in the fetch request.

**Fix:**  
I switched to using `localhost` for local testing instead of an unsecured address, fixed the fetch URL path, and ensured the CSRF cookie was included with the request headers.

**Lesson Learned:**  
Successful tokenisation requires all three conditions: a secure context (HTTPS or localhost), a correct route, and a valid CSRF token. Missing any one of these will prevent payment form submission.

---

#### 4.1.6.3 Invalid Application ID Error
**Bug:**  
*Square* returned `InvalidApplicationIdError` because the `|escapejs` filter in the template corrupted the application ID by encoding characters incorrectly.

**Fix:**  
I replaced the `|escapejs` filter with `|escape` in all template data attributes to preserve the correct ID formatting.

**Lesson Learned:**  
Use `|escapejs` only when outputting values inside inline JavaScript. For HTML attributes, the correct filter is `|escape` to avoid encoding issues.

---

#### 4.1.6.4 Authentication Error
**Bug:**  
*Square* API calls failed with a `401 Unauthorized` error. At first, I assumed it was due to bad credentials, but after testing the same token through curl, I discovered the real issue was the payload format.

**Fix:**  
I switched from sending data under an `"order"` key to the correct `"quick_pay"` object structure as required by the current API documentation.

**Lesson Learned:**  
A `401` response doesn’t always mean invalid credentials; it can also mean the payload structure is wrong. Always verify that the request body matches the expected schema for the endpoint.

---

#### 4.1.6.5 Webhook Integration Errors
**Bug 1–5:**  
Webhook tests repeatedly failed due to several setup issues: incorrect callback URLs, inactive *ngrok* sessions, missing `.ngrok-free.dev` domains in `ALLOWED_HOSTS`, unimported `json`, and stopped *ngrok* tunnels.

**Fix:**  
I removed duplicate URL prefixes, confirmed that both *Django* and *ngrok* were running, added `.ngrok-free.dev` to `ALLOWED_HOSTS`, imported `json` in the webhook view, and restarted *ngrok* to re-establish the tunnel.

**Lesson Learned:**  
Webhook testing depends on the environment being synchronised. Always verify the URL prefix, required imports, and active tunnel before retesting. *Ngrok* sessions must remain open while webhook tests are running.

---

#### 4.1.6.6 Webhook Signature Verification Errors
**Bug:**  
*Square* rejected every webhook attempt with `Invalid signature` because I only hashed the request body, not the full URL plus body combination.

**Fix:**  
“I concatenated the full HTTPS notification URL with the request body before computing the HMAC signature, following Square’s official verification pattern.

**Lesson Learned:**  
*Square* signs the full HTTPS URL concatenated with the request body, not just the body. Verifying only the payload will always fail signature validation.

---

#### 4.1.6.7 Webhook Authentication Error
**Bug:**  
Signatures still failed to verify, and some headers were missing from the request when running locally.

**Fix:**  
I switched to retrieving headers directly from `request.META` and ensured that the signature verification used the full HTTPS URL. This fixed the authentication mismatch and made validation consistent between local and deployed environments.

**Lesson Learned:**  
Always access headers using `request.META` to guarantee compatibility across environments. Signature verification must include the HTTPS URL exactly as *Square* sent it.

---

#### 4.1.6.8 Webhook Integration Error
**Bug:**  
The webhook raised a `JSONDecodeError`, and events were missing `square_order_id` and `square_payment_id` fields, breaking data handling.

**Fix:**  
I corrected the JSON structure, added the missing fields to the model, ran migrations, and temporarily disabled signature checks to test the webhook manually with PowerShell curl commands.

**Lesson Learned:**  
Always validate JSON syntax before parsing, ensure that model fields exist for expected data, and use `--data-binary` in PowerShell curl requests to prevent unwanted character encoding.

---

#### 4.1.6.9 Webhook Validation Error
**Bug:**  
Signature mismatches and HTTP 500 errors continued during webhook validation tests. Some duplicate payment events were also being recorded in the database.

**Fix:**  
I rebuilt the `square_webhook()` view from scratch with proper HTTPS signature verification, structured error handling, and duplicate event protection. Orders are now only marked as paid when the payment status is `"COMPLETED"`.

**Lesson Learned:**  
Force HTTPS in signature verification and always guard against duplicate event processing. A well-structured webhook should verify signatures first, handle only completed payments, and safely ignore repeats.

### 4.1.7 SECURITY & DEPLOYMENT

#### 4.1.7.1 Security Bug
**Bug:**  
Accidentally committed the *Django* `SECRET_KEY` to *GitHub* in the initial commit.

**Fix:**  
I regenerated a new secure key using `get_random_secret_key()`, stored it safely in a `.env` file (excluded via `.gitignore`), updated `settings.py` to load it using *python-decouple*, removed the entire *Git* history by deleting `.git`, reinitialising, and creating a fresh secure commit, then force-pushed the cleaned repo to *GitHub*.

**Lesson Learned:**  
Even one leaked commit can expose sensitive data permanently. Using environment variables and `.gitignore` from the start prevents accidental leaks. Rewriting history should be done early, before more commits make it harder.

---

#### 4.1.7.2 Deployment Issue
**Bug:**  
After deploying to *Heroku*, the app crashed with an `Application Error` and later returned a `404 page` instead of loading the homepage. Logs showed missing environment variables, and *Django* couldn’t find `SECRET_KEY` or `DATABASE_URL`.

**Fix:**  
I added the missing environment variables in *Heroku* using:

    heroku config:set SECRET_KEY="your-secret-key"
    heroku config:set DATABASE_URL="your-database-url"

Added `DISABLE_COLLECTSTATIC=1` to stop build errors.  
The `404` issue was due to mismatched template paths, fixed by changing:

    return render(request, 'core/home.html')
to  
    return render(request, 'home.html')

**Lesson Learned:**  
*Heroku* needs all environment variables, even if the app runs locally.  
If *Django* throws a 404 after deployment, double-check template paths in `render()` before assuming a routing issue.

---

#### 4.1.7.3 Database Configuration Error (*Heroku*)
**Bug:**  
The new *Heroku* app connected to the old *PostgreSQL* database from a previous project, showing old user data in *Django* admin.

**Fix:**  
I created a new *Supabase* database, copied the transaction pooler connection string, updated it with percent-encoded credentials, and set it in *Heroku*. Migrations were then applied to initialise the new schema.

**Lesson Learned:**  
When creating a new *Heroku* app, always update `DATABASE_URL`. Old connections may persist. Credentials containing special characters must be percent-encoded to avoid connection errors.

---

#### 4.1.7.4 Configuration Error
**Bug:**  
After deploying to *Heroku*, uploaded images failed to display because the `cloud_name` was missing in *Cloudinary* configuration.

**Fix:**  
I added the missing `CLOUDINARY_URL` environment variable in *Heroku*:

    heroku config:set CLOUDINARY_URL="cloudinary://<api_key>:<api_secret>@<cloud_name>"

Then restarted dynos with:

    heroku ps:restart -a slp-upgrade

**Lesson Learned:**  
*Cloudinary* requires a full connection URL, including `cloud_name`. Without it, *Django* can’t render image URLs even if uploads succeed.

---

#### 4.1.7.5 Environment Variable Load Failure
**Bug:**  
The *Square* payment form wouldn’t render because environment variables were not loading, leaving `SQUARE_APPLICATION_ID` and `SQUARE_LOCATION_ID` empty in runtime.

**Fix:**  
I moved `load_dotenv(BASE_DIR / ".env")` to the top of `config/settings.py`, added `DJANGO_SETTINGS_MODULE=config.settings` to `.env`, restarted the server, and confirmed both variables loaded correctly.

**Lesson Learned:**  
Environment variables must load before *Django*’s settings initialise. Placement of `load_dotenv()` is critical; it must come before any variable references.

---

#### 4.1.7.6 Deployment Errors
**Bug 1:**  
The first *Heroku* deployment failed due to `ModuleNotFoundError: No module named 'square'`.

**Fix 1:**  
I installed the correct SDK with `pip install squareup`, updated `requirements.txt`, and redeployed.

**Lesson Learned 1:**  
If a dependency isn’t in `requirements.txt`, *Heroku* won’t install it.

**Bug 2:**  
After installing, the import still failed because the SDK version on *Heroku* didn’t match local imports.

**Fix 2:**  
I inspected `dir(square.client)` in *Heroku’s* Python shell to confirm the correct class names, then adjusted imports accordingly.

**Lesson Learned 2:**  
Always confirm available classes directly in *Heroku* when import errors persist.

**Bug 3:**  
Initialising the client with `access_token` caused a `TypeError`.

**Fix 3:**  
I removed `access_token` from the constructor and set it as an attribute after initialisation.

**Lesson Learned 3:**  
SDK versions differ — confirm constructor signatures before assuming examples apply.

**Bug 4:**  
Couldn’t run migrations on the Eco plan due to single dyno limitation.

**Fix 4:**  
Scaled web dyno down with `heroku ps:scale web=0`, ran migrations, then scaled it back up.

**Lesson Learned 4:**  
On the Eco plan, *Heroku* only allows one dyno at a time, meaning migration commands can’t run while the `web dyno` is active.

**Bug 5:**  
Forgot to scale web dyno back up, causing H14 errors.

**Fix 5:**  
Ran `heroku ps:scale web=1`.

**Lesson Learned 5:**  
If *Heroku* returns “No web processes running”, restart the dyno.

---

#### 4.1.7.7 Static Files Cache Error
**Bug:**  
The deployed site showed old CSS, making form text invisible.  
`heroku run "cat staticfiles/css/style.css | grep color"` showed outdated `color: #0000;` rules.

**Fix:**  
I deleted `staticfiles/`, forced a rebuild with an empty commit, re-ran `collectstatic`, and confirmed fresh CSS with a new grep check.

**Lesson Learned:**  
If old CSS persists, static files are cached. Clear `/app/staticfiles`, force a rebuild, and verify the deployed file content.

---

#### 4.1.7.8 Deployment and Payment Integration
**Bug:**  
The *Square* card field didn’t render after deployment. Console showed `Cannot read properties of null` and `InvalidApplicationIdError`.

**Fix:**  
I delayed script execution until `window.onload`, added correct credentials to *Heroku* Config Vars, and verified SSL via *SSL Labs*. After redeployment, the card form appeared correctly.

**Lesson Learned:**  
Ensure scripts run only after DOM load and that *Heroku* Config Vars are set. Always verify HTTPS is valid; *Chrome* warnings may persist temporarily but don’t always indicate real danger.

---

#### 4.1.8 Project Failure - External Database Dependency Unavailable During Assessment

The project failed at assessment due to a production database dependency being used across all environments without resilience or environment separation. When the external Postgres service became unavailable, the application could not establish a database connection, resulting in server errors across authentication, admin access, and primary navigation routes. This prevented the assessor from accessing or evaluating core functionality.

**Bug:**
I configured the project to rely on a single external *Postgres* database hosted on *Supabase* for all environments (local development, production, and assessment). The free tier database was automatically paused after a period of inactivity. When the assessor accessed the deployed application, *Django* failed to resolve the database host, causing startup failure and resulting in `500 errors` across signup, login, admin, and database-backed routes.

**Fix:**
I removed the *Supabase* dependency entirely and migrated the project to a stable managed *Postgres* database hosted on *Neon*. I corrected the *Django* database configuration to explicitly require a valid `DATABASE_URL` and ensured it was set correctly in both local development and production via environment variables. I applied all migrations to the new database and verified that authentication, admin access, and primary routes functioned correctly in both local and deployed environments on Heroku.

**Lesson Learned:**
Relying on a single external database service across all environments without resilience or separation introduces a critical single point of failure. Free-tier managed databases may pause or become unavailable during assessment windows, causing complete application failure. Production deployments must use stable database providers and environment-aware configuration to ensure the application can reliably boot and remain accessible for assessment.

---

### 4.1.9 Database Configuration and Migration from *Supabase* to *Neon*

#### 4.1.9.1 *Supabase* *Postgres* Pause Caused Production Failure

**Bug:**  
The deployed application returned `Internal Server Errors` and failed assessment checks because the *Supabase* *Postgres* free-tier database entered a paused state. This caused DNS resolution failures and prevented *Django* from establishing a database connection in production.

**Fix:**  
*Supabase* was identified as an unstable external dependency for assessment-critical deployment. I temporarily resumed the *Supabase* project solely to allow a full database export, then permanently removed *Supabase* from the project after migration to *Neon* *Postgres*.

**Lesson Learned:**  
Free-tier managed databases can pause without warning. External infrastructure must be auditable, resumable, and suitable for assessment and production contexts.


#### 4.1.9.2 *Neon* Schema-Only Migration Resulted in Missing Data

**Bug:**  
After repointing *Django* to *Neon* *Postgres* and applying migrations, the application loaded successfully but displayed no Events, Products, or admin-generated content.

**Fix:**  
Confirmed that *Django* migrations recreated schema only. I planned and executed a full *Postgres*-to-*Postgres* data migration using native tooling rather than *Django* ORM serialisation or manual admin recreation.

**Lesson Learned:**  
*Django* migrations do not migrate data. Schema and data are separate concerns and must be handled explicitly.


#### 4.1.9.3 *Supabase* Network Inaccessibility Blocked Initial Export

**Bug:**  
Attempts to run `pg_dump` failed with hostname resolution errors because the *Supabase* project was paused and unreachable at the network level.

**Fix:**  
The *Supabase* project was manually resumed. Network reachability was verified using `Test-NetConnection` on port `5432` instead of ICMP-based `ping`.

**Lesson Learned:**  
ICMP is often blocked by managed services. TCP port checks are the correct diagnostic method for database connectivity.


#### 4.1.9.4 *PowerShell* Line Continuation Caused Dump Output to STDOUT

**Bug:**  
Using *PowerShell* line continuations caused `pg_dump` to execute without creating a dump file, resulting in output being written to STDOUT instead of disk.

**Fix:**  
I re-ran the export using a single-line command with an explicit `--file=supabase.dump` argument and verified the file existed with a non-zero size.

**Lesson Learned:**  
Shell-specific behaviour can affect critical commands. Single-line execution reduces ambiguity during data migration.


#### 4.1.9.5 *Supabase* Internal Schemas Triggered Restore Warnings

**Bug:**  
During `pg_restore`, errors were reported for missing relations such as `vault.secrets`.

**Fix:**  
Confirmed that the `vault` schema is *Supabase*-internal and unused by the application. Warnings were safely ignored, and public application tables restored correctly.

**Lesson Learned:**  
Provider-specific internal schemas may appear in exports. Not all restore warnings indicate application-level data loss.


#### 4.1.9.6 *Django* Migration State Out of Sync After Restore

**Bug:**  
*Django* raised errors indicating missing tables (e.g. `products_event`) when querying restored data.

**Fix:**  
I ran `python manage.py migrate` to align *Django*’s migration state with the restored database schema.

**Lesson Learned:**  
After raw database restores, *Django* migrations may still need to be applied to reconcile schema expectations.


#### 4.1.9.7 Explicit Schema Selection Required for *Neon*

**Bug:**  
*Django* failed to create the `django_migrations` table with the error `no schema has been selected to create in`.

**Fix:**  
Updated `DATABASE_URL` to include `&options=-csearch_path=public`, ensuring *Django* consistently targeted the correct schema.

**Lesson Learned:**  
*Neon* does not always default to the `public` schema. Schema selection must be explicit for *Django* compatibility.


#### 4.1.9.8 Data and *Cloudinary* Verification After Migration

**Bug:**  
There was uncertainty whether restored data and *Cloudinary* image references would function correctly after migration.

**Fix:**  
Verified data presence via the *Django* shell (`Event.objects.count()` returned `16`). Confirmed `e.image.url` returned valid *Cloudinary* URLs without re-uploading assets.

**Lesson Learned:**  
*Cloudinary* assets are external to the database. Once rows are restored, media works automatically.


### 4.1.10 Security & Deployment

#### 4.1.10.1 Assessment Failure Initially Misattributed to Code

**Bug:**  
The project assessment failed due to production errors that appeared to be application-level issues.

**Fix:**  
I traced failures to third-party infrastructure instability and database unavailability. Migrated to *Neon*, restored data, stabilised *Heroku* configuration, and verified production parity.

**Lesson Learned:**  
Infrastructure failures can masquerade as application bugs. Database availability and deployment configuration must be verified before refactoring application code.