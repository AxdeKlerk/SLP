## Security Bug

**Bug:**

Accidentally committed the *Django* SECRET_KEY to *GitHub* in the initial commit.

**Fix:**

Regenerated a new secure key using get_random_secret_key()

Stored it safely in a .env file (excluded via .gitignore)

Updated settings.py to load the key using python-decouple

Removed the entire *Git* history by deleting .git, reinitializing, and creating a fresh, secure initial commit

Force-pushed the cleaned repo to *GitHub*

**Lesson Learned:**

Even one leaked commit can expose sensitive data permanently. Using environment variables and .gitignore from the start prevents accidental leaks. Rewriting history should be done early if needed, before more commits make it harder.

## Deployment Issue

**Bug:**

After deploying to Heroku, the app crashed with an Application Error and later returned a 404 page instead of loading the homepage. The logs revealed that some environment variables were missing, and Django couldn’t find SECRET_KEY or `DATABASE_URL`. Even after fixing that, the app loaded but still returned a 404 error for all routes.

**Fix:**

Added missing environment variables to Heroku using:

    heroku config:set SECRET_KEY="your-secret-key"
    heroku config:set `DATABASE_URL`="your-database-url"

Added DISABLE_COLLECTSTATIC=1 to stop Heroku failing on missing static files during build.

The 404 error wasn’t caused by routing issues or template placement — the problem was that the templates were in the templates/ folder, but the view was trying to render core/home.html, which didn’t exist.

**Fix:**

Updated the views to match the actual template paths. Since the HTML files were directly inside templates/ (not in a core/ subfolder), we changed from:

    return render(request, 'core/home.html') to return render(request, 'home.html')

(Same for about.html and contact.html.)

**Lesson Learned:**

Heroku needs all environment variables your app depends on — even if it runs locally.

If Django throws a 404 after deployment but the URL paths look correct, double-check the template paths in your render() function.

Don't assume it's a folder problem — sometimes it's just the wrong string in the render() call.

## Database Configuration Error

### **Database Configuration Error**

**Bug:**  
The new *Heroku* app was still connected to the *PostgreSQL database* used in a previous project. This led to seeing old user data in the *Django* admin panel, even though the new app was supposed to be starting fresh. The problem occurred because the ``DATABASE_URL`` in *Heroku* was still pointing to the old *Heroku PostgreSQL* database from the previous project.

**Fix:**  
A brand-new *Supabase* database was created to replace the old *Heroku PostgreSQL* one. The *transaction pooler* connection string was copied from *Supabase* (under **Database > Connection Pooling**) and updated to include the actual password with special characters properly percent-encoded (e.g. `!` → `%21`). The connection string was set in *Heroku* and migrations were applied to initialise the new data base.

**Lesson Learned:**
When creating a new *Heroku* app, it may retain environment variables (like `DATABASE_URL`) from earlier linked services. If not explicitly changed, the app will connect to the previous database, even if the project is new. Always inspect and update `DATABASE_URL` after setting up a new deployment. Special characters in credentials must be percent-encoded to avoid connection errors.

### Offcanvas Navigation Error

**Bug:**  
The navigation links inside the mobile offcanvas menu would not redirect properly. Clicking them closed the menu but did not trigger navigation, even though the same links in the inline (desktop) menu worked fine.  

**Fix:**  
Removed the `data-bs-dismiss="offcanvas"` attribute from each `<a>` tag inside the offcanvas. This attribute was closing the drawer but also blocking the link’s natural navigation behaviour.  

**Lesson Learned:**  
If links inside a *Bootstrap* offcanvas are meant to load a new page (like *Django* `{% url %}` links), there is no need for `data-bs-dismiss`. The page reload will automatically hide the offcanvas, so adding dismissal attributes can actually break expected link behaviour.  

## Runtime Error

**Bug:**

*Cloudinary* image uploads failed in the *Django* admin panel. The error traceback ended with:
    `ValueError: Must supply api_key`
Even though the .env file included separate CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET variables, they were not being read correctly.

**Fix:**

Instead of using the dictionary-style CLOUDINARY_STORAGE = {...} config in settings.py, I used the unified CLOUDINARY_URL format in .env, like so:
    `CLOUDINARY_URL=cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>`
I also made sure to load this into the environment using *python-dotenv*, like this:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')

    CLOUDINARY_URL = os.getenv(`CLOUDINARY_URL`)
    if CLOUDINARY_URL:
    os.environ[CLOUDINARY_URL] = CLOUDINARY_URL
I then removed the old cloudinary.config() and CLOUDINARY_STORAGE = { ... } blocks to avoid conflicts with cloudinary_storage.

**Lesson Learned:**

*Cloudinary* prefers the all-in-one CLOUDINARY_URL format, and it must be present in os.environ before *Django* tries to use it. If you’re using *python-decouple*, it won’t export variables to os.environ automatically, which breaks *Cloudinary* unless you handle it manually. *python-dotenv* with *os.getenv()* works better in this case.

## Template Logic — Navbar active state (dropdown parent)

**Bug:**
Initially the `Events` navbar item wasn't staying highlighted once one of the dropdown items were selected. I then hard coded the `Events` navbar item as `active` and realised that the issue was with the relationship between parent and child items.

**Fix:**
I removed the hard-coded `active` from the parent toggle and marked the parent/children `active`:

`{% if url_name == 'events' or url_name == 'previous_events' %}active{% endif %}` based on the current view name with a request resolver above: `{% with url_name=request.resolver_match.url_name %}` and added the `active` status to my css to increase specifity.

**Lesson Learned:**

Don’t hard-code active on nav items; compute it from the current route. For dropdowns, the parent’s state should reflect child activity (via request.resolver_match.url_name) and keep CSS specific but simple; Bootstrap’s defaults can override you unless your rules target the right elements.

## Logic Bug

**Bug:**

I noticed that my Roxoff event cards were appearing on the Upcoming Gigs page. This wasn’t supposed to happen — Roxoff events should only be shown on their own dedicated template `(roxoff.html)`, not mixed in with regular events.

**Fix:**

I realised I needed a way to clearly separate Roxoff events from regular ones. So I added a new event_type field to the Event model with `regular` and `roxoff` choices. Then I updated the view for the Upcoming Gigs page `(events_view)` to exclude Roxoff events:

`events = Event.objects.filter(gig_date__gte=today).exclude(event_type='roxoff').order_by('gig_date')`

**Lesson Learned:**

It’s better to explicitly separate types of events in the model using a dedicated field like event_type. That way, filtering them in views is more reliable and readable than trying to guess based on other values like roxoff_day. It also makes future development easier, especially if I need more event types later.

## Routing Error

**Bug:**
The venue search was returning a 404 error after submitting a search term. The artist search worked perfectly, even though the structure for both was identical in urls.py, views.py, and JavaScript. Visiting a URL like /venue/2/ returned a 404, but /artist/5/ did not.

**Fix:**
The issue was caused by relying on both root-level and namespaced includes for the products app in config/urls.py. At one point, both of these were present:

`path('', include('apps.products.urls')),`
`path('products/', include('apps.products.urls', namespace='products')),`

This meant some views worked at /artist/5/ (because of the root include), while others like /venue/2/ failed (due to inconsistent includes or redirects).
Once the root-level include was removed for clarity and consistency, all routes required the /products/ prefix. The fix involved two changes:

Removed the root include:

`path('', include('apps.products.urls')),`  # removed

Updated JS redirects to include the /products/ prefix:

window.location.href = `/products/venue/${data.id}/`;
window.location.href = `/products/artist/${data.id}/`;

**Lesson Learned:**
When using app-level namespacing `(namespace='products')`, routes must consistently match the URL prefix (/products/...). Having both root-level and prefixed includes causes unpredictable routing. Always verify that JavaScript redirects match your configured URL patterns.

## Navigation Highlight Issue

**Bug:**

The *Search* navbar item did not stay highlighted when navigating to either the artist or venue detail page (`artist_detail`, `venue_detail`). The expected behavior was for the *Search* tab to be marked active when the user was on these pages, just like the *Events* tab behaves when on related event pages.

**Fix:**  
I identified that the condition checking the *Search* tab for `artist_search` and `venue_search` was incorrect because those were not the actual view names. Instead, the actual view names were `artist_detail` and `venue_detail`. I updated the navbar to use these correct names.

**Lesson Learned:**  
When using `url_name` for template conditions, it’s essential to ensure I’m checking against the correct view name. I learned to debug this by printing `url_name` in the template using:

<p style="color:red; font-size:12px">
  url_name = {{ request.resolver_match.url_name }}
</p>

This helped me verify the actual names *Django* was using for each page. Always ensure the condition matches the exact value of `url_name` for the intended behavior.

## Template/Context Error

**Bug:**

The size dropdown wasn’t showing any options in the merch detail page. Clicking the button made the dropdown appear, but it was empty. The issue was that I tried looping with `{% for s in size_choices %}` and using `{{ s }}`, but my model’s choices actually return two values `(key, label)`. Because of that, nothing was rendered in the `<ul>`.

**Fix:**

I updated my `MerchDetailVie`w to pass size_choices into the context. Then in my template, I switched from using `{{ s }}` to the correct `{{ key }} and {{ label }}`. Finally, I matched the *Size JS* to the same pattern as the *Quantity JS*, so both dropdowns behave consistently.

**Lesson Learned:**

I need to remember that *Django* model field choices always give back `(key, label)` pairs, not a single value. If I try to loop with the wrong variable, the template will silently fail and look like “nothing happened.” Next time, I’ll check what data type a loop is actually returning before writing the template logic, and I’ll keep dropdown JS patterns consistent across all fields.

## Configuration Error

**Bug:**  

After deploying to **Heroku**, images uploaded through the Django Admin did not display. In the **Heroku** *Python shell*, running `print(e.image.url)` raised:

    *ValueError: Must supply cloud_name in tag or in configuration*

The images had uploaded to **Cloudinary** (the `public_id` existed), but without the `cloud_name` in the configuration, **Django** could not generate valid URLs.

**Fix:**  

I added the missing `CLOUDINARY_URL` environment variable in **Heroku** using the value from the **Cloudinary** dashboard:

    **heroku** *config:set CLOUDINARY_URL="cloudinary://<api_key>:<api_secret>@<cloud_name>" -a slp-upgrade*

Then I restarted the dynos:

    *heroku ps:restart -a slp-upgrade*

After this, `{{ event.image.url }}` returned a proper **Cloudinary** URL such as `https://res.cloudinary.com/<cloud_name>/...`, and the images displayed correctly.

**Lesson Learned:**  

**Cloudinary** requires the `CLOUDINARY_URL` environment variable, which contains the `cloud_name`. Without it, images cannot be resolved even if they are uploaded. Always verify critical third-party environment variables are set in Heroku before deploying.

## Search Integration Bug

**Bug:**  

I added a "Merch" field to the navbar search dropdown, but it didn’t return results. "Artist" and "Venue" already worked by looking up the PK through small API endpoints and redirecting straight to their detail pages. "Merch" needed to search by `product_name` or `product_category` (both key and label) via the central search view, but nothing happened on Enter because the input wasn’t wired to the same flow and the view didn’t robustly handle category labels.

**Fix:**  

I kept Artist/Venue logic exactly as-is (PK lookup + redirect) and added a *minimal, isolated* merch path:

1) Confirmed a namespaced central search route so I can link to it reliably.
    
    File: `apps/products/urls.py`
    
        from django.urls import path
        from . import views
        
        app_name = "products"
        
        urlpatterns = [
            # ...existing routes...
            path("search/", views.search_view, name="search"),
        ]

2) I Added a *Enter-key handler* for the merch input only. This builds `?category=merch&q=...` and sends the browser to the central search page. Artist/Venue handlers remained unchanged.

    File: `static/js/script.js`
    
        document.addEventListener("DOMContentLoaded", function () {
          // --- MERCH: Enter -> central search ---
          (function () {
            const merchSearch = document.getElementById("merch-search");
            if (!merchSearch) return;
        
            // Prefer dynamic URL from <body data-search-url="...">; fallback to namespaced path
            const searchUrl = (document.body && document.body.dataset && document.body.dataset.searchUrl)
              ? document.body.dataset.searchUrl
              : "/products/search/";
        
            merchSearch.addEventListener("keydown", function (e) {
              if (e.key !== "Enter") return;
              e.preventDefault();
        
              const q = (this.value || "").trim();
              if (!q) return;
        
              window.location.href = `${searchUrl}?category=merch&q=${encodeURIComponent(q)}`;
            });
          })();
        
          // (Artist and Venue keydown handlers stayed exactly as they were.)
        });

3) I Made the central search view’s merch branch match on product name OR category key OR category label to cover queries like “hoodie” or “Hoodie”.

    File: `apps/products/views.py`
    
        from django.db.models import Q
        
        def search_view(request):
            category = (request.GET.get("category") or "").strip()
            q = (request.GET.get("q") or "").strip()
        
            ctx = {"category": category, "q": q}
        
            if not category or not q:
                return render(request, "search_results.html", ctx)
        
            if category == "artist":
                ctx["artist_results"] = Artist.objects.filter(
                    name__icontains=q
                ).order_by("name")
        
            elif category == "venue":
                ctx["venue_results"] = Venue.objects.filter(
                    name__icontains=q
                ).order_by("name")
        
            elif category == "merch":
                choices = Merch._meta.get_field("product_category").choices  # [(key, "Label"), ...]
                label_keys = [key for key, label in choices if q.lower() in str(label).lower()]
        
                ctx["merch_results"] = Merch.objects.filter(
                    Q(product_name__icontains=q) |
                    Q(product_category__icontains=q) |    # matches key like "hoodie"
                    Q(product_category__in=label_keys)     # matches label like "Hoodie"
                ).order_by("product_name", "product_category", "size")
        
            return render(request, "search_results.html", ctx)

**Lesson Learned:**

- Static JS cannot use `{% url %}`; expose **Django** URLs via `data-*` attributes in templates or hardcode a stable path.  
- Keep IDs unique; duplicate IDs silently break listeners.  
- Standardize query paramaters (`q` + `category`) so server-side logic stays simple.  
- When using `choices`, match both the stored key and the human readable label to make searches intuitive (“hoodie” should match, whether user types the key or the label).

## Basket Data Handling Error

**Bug:**

When adding merch items with a specific quantity (e.g., 2), the quantity was not carrying over into the basket. Additionally, when updating quantities of items already in the basket, the order of items would randomly change. This made it look like quantities were being applied inconsistently and the basket was shuffling unpredictably.

**Fix:**

For the missing quantity, I updated the `add_merch_to_basket` view to capture the `quantity` value from the form (`request.POST`) instead of defaulting to 1 every time. This allowed the chosen number from the merch detail dropdown to carry through to the basket correctly.

For the reordering, I added explicit ordering to the queryset with `basket.items.order_by("id")`. This stopped items from appearing in a different order after each update, since **Django** by default doesn’t guarantee order unless specified.

**Lesson Learned:**

Never assume form values are automatically passed through — always grab them explicitly from `request.POST`. And when showing lists of models, always add `order_by` if I want a predictable order; **Django** does not guarantee query ordering without it.

## Basket Size Display Error

**Bug:**

The merch size wasn’t showing up in the basket, even though it was being selected on the merch detail page. When it did appear, it sometimes showed as a lowercase letter (`l` instead of `L`). 

**Fix:**

I added a `size` field to the `BasketItem` model and ensured the selected size was stored in it when the merch was added to the basket. In the template, I displayed the size using `{{ item.get_size_display }}` instead of just `{{ item.size }}`, so it pulled the capitalised label defined in the model’s `choices`.

**Lesson Learned:**

If a field uses choices in **Django**, always use `get_FIELD_display` to render the user-friendly label instead of the raw database value. That avoids problems like lowercase codes or cryptic letters showing in the UI.

## Basket Event Details Error

**Bug:**

I originally used `{{ item.event }}` to show event details in the basket, but this included the event name, venue, and date all in one line (because of the model’s `__str__` method). When I tried to split them, the venue ended up being repeated, making the basket confusing.

**Fix:**

I updated the basket template to display the individual attributes separately:
- `{{ item.event.title }}` for the event name,
- `{{ item.event.venue }}` for the venue,
- `{{ item.event.date }}` for the date.

This stopped duplication and gave me full control of where each piece of information appeared.

**Lesson Learned:**

Don’t rely on `__str__` when you need fine control over display. It’s better to pull the exact fields needed, especially when showing multiple attributes in different places.

## Basket Layout/Responsive Error

**Bug:**

The basket layout was inconsistent across screen sizes. On larger screens, the qty dropdown, delete button, and price weren’t lining up properly with the description. On smaller screens (<768px), the layout collapsed in unexpected ways: the description wrapped awkwardly, the qty dropdown wasn’t aligned with the text, and the venue/date sometimes appeared in the wrong place.

**Fix:**

I restructured the template using Bootstrap’s grid system:
- For ≥768px screens, I kept the original layout with three columns: thumbnail, details, and price aligned with description text. Qty dropdown and delete button sat below in a second row.
  
- For <768px screens, I stacked the layout into clearer rows: thumbnail in the first column, event/merch details in the second, and price + delete aligned in the third. I also adjusted the delete button size using `btn-sm` for mobiles and tightened spacing with Bootstrap utility classes.

**Lesson Learned:**

When debugging responsive layouts, design separately for mobile and desktop first, then merge. Bootstrap’s `d-none`, `d-md-block`, and breakpoint classes are essential for tailoring layouts. Never assume one structure will look right on both small and large screens without breakpoint adjustments.

## AttributeError

**Bug:**

When I tried to place an order at `/checkout/`, I got the error:  
`AttributeError: 'BasketItem' object has no attribute 'price'`.  
This happened because in `checkout_view` I was trying to use `item.price`, but my `BasketItem` model did not have a `price` field. Instead, it only had `event` or `merch`, each of which has its own price.

**Fix:**

I already had a `line_total` property in `BasketItem` that handled both event and merch correctly. I updated the `checkout_view` to use `item.line_total` instead of `item.price`. For the `OrderItem` snapshot, I stored the unit price by dividing `line_total` by `item.quantity`.

`line_total = item.line_total
subtotal += line_total`

`OrderItem.objects.create(
    order=order,
    product_name=str(item),
    quantity=item.quantity,
    price=(line_total / item.quantity) if item.quantity else 0,
)`

**Lesson Learned:**

I should not assume fields exist on a model without checking. If I’ve already written helper methods or properties like line_total, I should reuse them instead of duplicating logic. This keeps the code consistent and avoids errors like calling item.price when no such field exists.

## CSS Layout Bug

**Bug:**  

On screens between 576px and 767px, my event cards were not centered. The `.row` container was full width, but the `.standard-card` element stayed stuck to the left side. This only happened on small screens because the card had a `max-width` set, which prevented it from stretching to fill the column. Without centering rules, it always aligned left.

**Fix:** 

I discovered that the `.standard-card` CSS had `max-width: 300px;` but no horizontal centering. The card was narrower than its parent column and defaulted to the left. I fixed this by adding `margin-left: auto;` and `margin-right: auto;` to the `.standard-card` CSS so that it stayed centered inside its column.

**Lesson Learned:**  

When using `max-width` on a card inside a Bootstrap column, the card will not center itself automatically. Even if the column is full width, the child element needs `margin: auto` to align correctly. Always check custom CSS rules like `max-width` if a card or element looks offset at certain breakpoints. Although, it is quite basic syntax and something I should have known, going off into a panic about it when it is not working is not helpful, and most certainly a pause moment to step-back and think clearly without doubting myself.

## Template Logic Bug for Size Dropdown Menu items for Flags, Mugs and Caps

**Bug:** 

The size dropdown was showing for all merch items, including flags, mugs, and caps. These products do not need size options, but the template always displayed the dropdown. My first attempt was to use `{% if merch.category == "flag" %}`, but this failed because the correct model field name was `product_category`. When I later tried to check multiple categories with `in ("flag", "mug", "cap")`, it caused a *Django* `TemplateSyntaxError` because template conditions do not support tuple syntax.

**Fix:**  

I solved the problem by chaining multiple conditions with `or` in the template. This allowed me to remove the dropdown for flags, mugs, and caps, while keeping it for t-shirts and hoodies using a conditional `if` statement.

    {% if merch.product_category == "flag" or merch.product_category == "mug" or merch.product_category == "cap" %}

**Lesson Learned:**  

The *Django* template language does not support Python tuple syntax in `if` statements. To check multiple values, I must use `or` (or `and`) to chain conditions. It is important to reference the correct model field, in this case the (`product_category`), when testing values. Using the wrong field name will always fail, even `if` the condition looks correct.

## Logic Error for Forgot Username View

**Bug:** 

The forgot username feature did not work. Submitting the form just reloaded the same page and never redirected to the done page. No email was sent to the terminal. After checking the `views.py`, I saw the condition was written as `if request.method == "Post":`. The browser always sends the HTTP method in uppercase (`"POST"`), so this condition never matched. As a result, the code inside never ran.

**Fix:**  
I corrected the case of the request method check to `"POST"`. With this fix, the form submission was processed, the email was printed to the terminal, and the redirect to the `password_reset_done` page worked as expected.


**Lesson Learned:**  

In *Django*, `request.method` is always uppercase. If I use lowercase or mixed case like `"Post"`, the condition will never be true. Always check against `"POST"` for form submissions and `"GET"` for page loads.

## Ticket Oversell Error Not Displaying

**Bug:** 

When I set the `capacity` of a venue to 3 and added 4 tickets for the event in the basket, the checkout did not show the error message. The basket page loaded normally without any oversell warning.  

**Fix:**

I discovered that the ticket guardrail check was placed inside the `if request.method == "POST":` block in `checkout_view`. Since the checkout button in the basket template was a simple link (`<a href="...">`), it triggered a `GET` request, not a `POST`. This meant the oversell check never ran.  

To fix it, I moved the `oversell check` above the `POST` block so it always executes.  

**Lesson Learned:**

Placing validation logic only inside a `POST` block means it never runs when checkout is accessed with a `GET` request. For guardrails like ticket limits, the check should be at the top of the view so it always runs before proceeding. I also confirmed that my *BasketItem model* correctly linked to events, and that the `effective_capacity() method` in the *Event model* was being used. This ensured that overselling tickets could be caught and displayed with a clear error message.

## Static Files Cache Error

**Bug:** 

When I deployed to *Heroku*, the input fields on the login and signup pages did not show any text. Locally the text was black after updating my CSS, but in production it was invisible. Checking the deployed CSS with `heroku run "cat staticfiles/css/style.css | grep color"` showed that `color: #0000;` was present. This confirmed that old CSS was being served by *Heroku*, even though I had already fixed it in my local project.

**Fix:**  

I discovered that the problem was caused by old files inside the `staticfiles/` directory. This folder is generated by `collectstatic`, but older copies had slipped into *Heroku*’s cache.

Steps I followed to fix it:

- I removed the existing collected static files on *Heroku*:

- I forced a clean rebuild on *Heroku* to make sure no old files were cached:

    git commit --allow-empty -m "Force clean rebuild on Heroku"
    git push heroku main

I re-ran collectstatic to regenerate fresh static files from my updated CSS:

    *python manage.py collectstatic*

Finally, I verified the fix by checking the CSS again:

    heroku run "cat staticfiles/css/style.css | grep color"

This time `color: #0000;` was gone and only `color: #000000;` remained.

**Lesson Learned:**  

If old rules show up in production, it usually means stale static files are being cached on *Heroku*. The correct fix is to wipe `/app/staticfiles`, force a rebuild, and regenerate clean static files. Always confirm with a `grep` check to make sure the deployed CSS matches local changes.

## Validation Error – Ticket Capacity Message Errors

**Bug:**

When testing ticket sales against venue and event capacities, three issues appeared:  
1. I was calling `tickets_sold()` and `effective_capacity()` with parentheses, but they were `@property` methods. This caused `TypeError: 'int' object is not callable`.  
2. The "Event is now fully booked" message triggered incorrectly even when the basket quantity exactly matched the event capacity. This blocked valid orders.  
3. Error messages always displayed "0 tickets left" because I wasn’t calculating `remaining` correctly when basket quantities were less than or equal to capacity.

**Fix:**  

I updated the validation logic inside `checkout_view` so that only overselling tickets triggers an error. I corrected `@property` usage by removing parentheses. I also dropped the redundant "event fully booked" branch to allow valid purchases when the basket exactly matched the remaining tickets.

Final working validation:

    for item in basket_items:
        if item.event and item.event not in checked_events:
            checked_events.add(item.event)

            sold = item.event.tickets_sold
            requested_quantity = sum(i.quantity for i in basket_items if i.event == item.event)
            capacity = item.event.effective_capacity

            remaining = capacity - sold

            if requested_quantity > remaining:
                ticket_word = "ticket" if remaining == 1 else "tickets"
                messages.error(
                    request,
                    f"Not enough tickets available! Try adjusting quantity! "
                    f"Only {remaining} {ticket_word} left for {item.event}!"
                )
                return redirect("basket:basket_view")

**Lesson Learned:** 

I learned that `@property` methods in *Django* models should not be called with parentheses. I also learned to distinguish between overselling (invalid) and exactly filling capacity (valid) when checking basket quantities. Removing redundant validation branches made the logic simpler and correct. Finally, calculating `remaining` before raising errors is essential to prevent misleading messages like "0 tickets left."  

## Integration Errors (*Square* API with Django)

**Bug:** 

When I first tried to install the *Square* Python SDK, I mistakenly installed `squareapp` and then ran into import errors. Even after installing `squareup`, I still saw `ImportError: cannot import name 'Client' from 'square.client'`. Later attempts with `SquareClient` also failed. The installed SDK version defined a `*Square*` class instead, and its constructor did not accept `access_token`. Calling `list_locations()` raised `AttributeError` because the method name had changed. Finally, trying to check `result.is_success()` failed because the response object was a Pydantic model without that helper method.

**Fix:**  

I uninstalled the incorrect `square` package and reinstalled the official SDK with `pip install squareup`. I then checked the installed file `.venv/Lib/site-packages/square/client.py` to confirm the class name and constructor signature. For my version, the correct setup was:

    import os
    from square.client import *Square*, SquareEnvironment

    client = *Square*(
        token=os.getenv("SQUARE_ACCESS_TOKEN"),
        environment=SquareEnvironment.SANDBOX
    )

Next, instead of `client.locations.list_locations()`, the right call was `client.locations.list()`. Finally, since the response was a Pydantic model, I accessed its `.locations` attribute directly and converted each item to a dict for JSON.

    def test_square_connection(request):
        result = client.locations.list()
        if hasattr(result, "errors") and result.errors:
            return JsonResponse({"errors": [e.detail for e in result.errors]})
        locations = [loc.dict() for loc in result.locations] if result.locations else []
        return JsonResponse({"locations": locations})

**Lesson Learned:**

Different versions of the *Square* SDK have different client class names, constructors, and method patterns. In my version, the correct class was `*Square*` instead of `Client`, and I had to pass `token` and `SquareEnvironment.SANDBOX` instead of `access_token`. API methods like `list_locations()` may be renamed to `list()`, and response handling moved to Pydantic models without helpers like `.is_success()`. Always confirm the installed SDK version and inspect its client class directly when debugging integration errors with external APIs in *Django*.

## CSRF and Tokenisation Errors

**Bug:** 

When setting up the *Square* Web Payments SDK for tokenisation, I encountered multiple problems that prevented the token from being generated and successfully posted to the *Django* backend. Specifically, there were three main issues:  
1. The *Square* SDK refused to render the card element because the site was not served over a secure context.  
2. The token `POST` request was failing with a `404 error` because the `fetch UR`L did not match the configured *Django* route.  
3. Even after fixing the URL, the request returned a `403 Forbidden error` due to a missing `CSRF cookie`, which meant *Django* blocked the request.

**Fix:**  

1. For the secure context error, I stopped using `127.0.0.1` and switched to `http://localhost:8000/payments/checkout/`, which *Square* treats as a valid sandbox context. This allowed the SDK to initialise and render the card element.  
2. For the routing error, I corrected the `fetch URL` in the *JavaScript* file. Originally it was pointing to `"/apps/payments/process-payment/"`, but my *Django* configuration exposed the route at `"/payments/process-payment/"`. After updating the `fetch call`, the request reached the correct view. 
 
   Example of the corrected fetch call:  
       const resp = await fetch("/payments/process-payment/", {
           method: "POST",
           headers: {
               "Content-Type": "application/json",
               "X-CSRFToken": csrftoken,
           },
           body: JSON.stringify({ token, amount }),
       });

3. For the `CSRF error`, I ensured the `CSRF cookie` was being set and included in the request header. Adding `{% csrf_token %}` to the template and confirming that `csrftoken` was present in the browser cookies fixed the `403 Forbidden` problem. With the `CSRF token` included, *Django* accepted the `POST` and the backend logged the *Square* token.

**Lesson Learned:** 

Tokenisation only works when all three conditions are satisfied: the SDK must be served in a secure context (`localhost` or HTTPS), the `fetch` URL must exactly match the route defined in *Django*, and the `CSRF cookie` must be present and sent with the `POST request`. Missing any of these steps caused errors that blocked the flow. By carefully checking console logs, *Django* terminal output, and *Dev Tools* network responses, I was able to isolate and resolve each issue in turn.

## Invalid Application ID Error

**Bug:**

When testing the *Square* Web Payments SDK, the card input would not render and the console showed `InvalidApplicationIdError: The Payment 'applicationId' option is not in the correct format.` In the logs, the `appId` value appeared as `sandbox\u002Dsq0idb\u002DSGiFCV2Wy5dWVMk2w_OJIQ` instead of `sandbox-sq0idb-SGiFCV2Wy5dWVMk2w_OJIQ`. The issue was caused by the `|escapejs` filter in the template, which converted dashes (`-`) into unicode escapes (`\u002D`). This broke the SDK because *Square* expected the raw application ID string.

**Fix:** 

I updated the template to stop escaping the IDs with `|escapejs` when using them in *HTML* attributes. The corrected code used `|escape` instead, which safely outputs the string without turning dashes into unicode escapes.

    <div id="square-config"
         data-app-id="{{ SQUARE_APPLICATION_ID|escape }}"
         data-location-id="{{ SQUARE_LOCATION_ID|escape }}">
    </div>

After this change, the `appId` printed correctly as `sandbox-sq0idb-...`, and the *Square* card input rendered as expected.

**Lesson Learned:**

The `|escapejs` filter in *Django* templates is only for values inserted into inline *JavaScript* blocks. When passing values into *HTML* `data-` attributes, using `|escapejs` will incorrectly encode special characters and break *API*s that expect raw values. The right approach is to use `|escape` or no filter at all for safe IDs. This ensured the *Square* SDK received the correct `applicationId` and allowed tokenisation to work.



