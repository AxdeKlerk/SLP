Chronological Debugging and Testing entries

### Table of Contents
- [Debugging](##debugging)
- [Testing](##testing)


## Debugging

## Security Bug

**Bug:**
Accidentally committed the *Django* `SECRET_KEY` to *GitHub* in the initial commit.

**Fix:**
Regenerated a new secure key using `get_random_secret_key()`

Stored it safely in a `.env` file (excluded via `.gitignore`)

Updated settings.py to load the key using *python*-decouple

Removed the entire *Git* history by deleting .git, reinitializing, and creating a fresh, secure initial commit

Force-pushed the cleaned repo to *GitHub*

**Lesson Learned:**
Even one leaked commit can expose sensitive data permanently. Using environment variables and `.gitignore` from the start prevents accidental leaks. Rewriting history should be done early if needed, before more commits make it harder.

## Deployment Issue

**Bug:**
After deploying to *Heroku*, the app crashed with an    `Application Error` and later returned a `404 page` instead of loading the homepage. The logs revealed that some environment variables were missing, and *Django* couldn’t find     SECRET_KEY   or `DATABASE_URL`. Even after fixing that, the app loaded but still returned a `404 error` for all routes.

**Fix:**
Added missing environment variables to *Heroku* using:

    heroku config:set SECRET_KEY="your-secret-key"
    heroku config:set `DATABASE_URL`="your-database-url"

Added `DISABLE_COLLECTSTATIC=1` to stop *Heroku* failing on missing static files during build.

The `404 error` wasn’t caused by routing issues or template placement — the problem was that the templates were in the templates/ folder, but the view was trying to render core/home.html, which didn’t exist.

**Fix:**
Updated the views to match the actual template paths. Since the HTML files were directly inside templates/ (not in a core/ subfolder), we changed from:

    return render(request, 'core/home.html') to return render(request, 'home.html')

(Same for about.html and contact.html.)

**Lesson Learned:**
*Heroku* needs all environment variables your app depends on — even if it runs locally.

If *Django* throws a 404 after deployment but the URL paths look correct, double-check the template paths in your render() function.

Don't assume it's a folder problem — sometimes it's just the wrong string in the render() call.

## Database Configuration Error

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
After deploying to *Heroku*, images uploaded through the Django Admin did not display. In the *Heroku* *Python shell*, running `print(e.image.url)` raised:

    *ValueError: Must supply cloud_name in tag or in configuration*

The images had uploaded to *Cloudinary* (the `public_id` existed), but without the `cloud_name` in the configuration, *Django* could not generate valid URLs.

**Fix:**  
I added the missing `CLOUDINARY_URL` environment variable in *Heroku* using the value from the *Cloudinary* dashboard:

    **heroku** *config:set CLOUDINARY_URL="cloudinary://<api_key>:<api_secret>@<cloud_name>" -a slp-upgrade*

Then I restarted the dynos:

    *heroku ps:restart -a slp-upgrade*

After this, `{{ event.image.url }}` returned a proper *Cloudinary* URL such as `https://res.cloudinary.com/<cloud_name>/...`, and the images displayed correctly.

**Lesson Learned:**  
*Cloudinary* requires the `CLOUDINARY_URL` environment variable, which contains the `cloud_name`. Without it, images cannot be resolved even if they are uploaded. Always verify critical third-party environment variables are set in Heroku before deploying.

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

## Integration Errors (*Square* API with *Django*)

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

## Quantity Clamping Error

**Bug:** 
I realised that the basket handlers did not limit item quantities. This meant a malicious user could tamper with the form or send a direct POST request to set `quantity` to 0, a negative number, or something excessive like 99. This caused broken basket totals and risked over-selling tickets or merch items.

**Fix:** 
I added clamping logic in the basket views to enforce valid ranges. Specifically:
- In `add_merch_to_basket`, I wrapped the POSTed quantity with a check so anything below 1 defaults to 1, and anything above 9 defaults to 9.
- In `update_basket_item`, I replaced the old conditional with the same clamp logic to ensure updates cannot bypass the rule.
- In `add_event_to_basket`, I updated the increment logic so that repeated additions cannot push the quantity above 9.  

Example adjustment in `add_merch_to_basket`:  

    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1:
        quantity = 1
    elif quantity > 9:
        quantity = 9

**Lesson Learned:**  
Always enforce business rules on the backend, not just the frontend. Even if the form uses a `<select>` limited to 1–9, users can still tamper with `POST` data. By clamping the quantity inside the *Django* `views`, the basket remains safe against malicious inputs and ensures stable order totals.

## Routing Error

**Bug:**
When I clicked the *Proceed to Payment* button on the profile page, *Django* raised a `NoReverseMatch` error:  
`Reverse for 'payment_checkout' not found. 'payment_checkout' is not a valid view function or pattern name.`  

This happened because in `profile.html` I used `{% url 'payment_checkout' %}` without the correct namespace. Since the `payments` app was included in `config/urls.py` with `namespace="payments"`, *Django* could not resolve the route without the prefix.

**Fix:**
I updated the template to include the `namespace` so the URL matched the registered name:

    {% url 'payments:payment_checkout' %}

After this change and restarting the server, the button correctly resolved to `/payments/checkout/` and redirected as expected.

**Lesson Learned:**
When including an app’s URLs in `config/urls.py` with a `namespace`, all reverse lookups using `{% url %}` or `reverse()` must include that namespace. Forgetting the namespace will always result in a `NoReverseMatch` error, even if the route is defined correctly.

## Template Logic Error

**Bug:**
On the profile page, orders in progress were being displayed twice: once as styled cards and again in a table below. This duplication made the UI confusing and cluttered.

**Fix:**  
Removed the second loop that rendered orders in a table. Integrated `checkboxes` for *bulk delete* directly into the card layout so that only one rendering of the orders is shown. Updated the `bulk delete form` to wrap around the card loop, eliminating the need for a duplicate list.

**Lesson Learned:**
Always ensure each dataset is only rendered once in a template. If a new feature (like `bulk delete`) needs to interact with the same data, integrate it into the existing layout rather than creating a second loop. This keeps the UI consistent and avoids confusing duplication.

## Logic Error

**Bug:** 
When I added a *merch item* to the basket without choosing a size, the size field was saved as empty instead of defaulting to "L". This happened because the hidden input for `size` in `basket_button.html` had no value set, so unless the *JavaScript* updated it after a click, nothing was passed to the backend.

**Fix:**
I updated the hidden input in `basket_button.html` to include a default value of `"L"`. This meant that if no size was chosen, the basket still received "L" automatically.

    <input type="hidden" name="size" id="selected-size" value="L">

**Lesson Learned:** 
I learned that hidden inputs should always have a sensible default if they rely on *JavaScript* to change their values. Without the default, the backend will just get blanks when no interaction occurs. Keeping things simple with a fallback avoids unexpected empty data being saved.

## Search Function Variation Error

**Bug:**
When I searched for variations such as "black" or even a single letter like "b", the search only returned a single artist. This happened because the search function in my *Django* view was using `.first()`, which only grabs the first match, instead of pulling all relevant results.

**Fix:**  
I updated the `search_view` function to query all matches instead of just one. Specifically, I replaced the use of `.first()` with a queryset and ordered the results. This allowed multiple matches (e.g., "Black Sabbath" and "Black Keys") or all artists starting with "b" to appear.  

Updated section of `views.py`:

    if category == "artist":
        ctx["artist_results"] = Artist.objects.filter(
            name__icontains=q
        ).order_by("name")

I then adjusted the template `search_results.html` to loop through `artist_results` instead of only displaying one:

    {% if artist_results %}
        {% for artist in artist_results %}
            {% include "_artist_detail_block.html" with artist=artist %}
        {% endfor %}
    {% else %}
        <p>No artists found for "{{ q }}".</p>
    {% endif %}

This way, entering "black" lists all artists with "black" in their name, and entering a single letter like "b" lists all artists whose name contains that letter.

**Lesson Learned:**  
Using `.first()` in a queryset is only for grabbing one record, which is useful for lookups but not for listing results. For search functionality, I needed to query all matching objects with `.filter()` and then loop through them in the template. This ensures all variations and partial matches are displayed properly to the user.

## Deployment Errors

**Bug 1:** 
When I first deployed my project to *Heroku*, the site crashed with an `Internal Server Error`. The logs showed `ModuleNotFoundError: No module named 'square'`. This meant the *Square SDK* was not installed in production, even though it worked locally.

**Fix 1:** 
I installed the correct package locally with `pip install squareup`, then updated `requirements.txt` using `pip freeze > requirements.txt`, committed the change, and redeployed to *Heroku*. This ensured *Heroku* installed the *Square SDK* during build.

**Lesson Learned 1:**
If a package is not listed in `requirements.txt`, *Heroku* will not install it, even if it works locally.

**Bug 2:** 
After installing `squareup`, the import still failed. My code used `from square.client import Square, SquareEnvironment` and later `from square.client import Client`. The SDK version on *Heroku* did not match these imports.

**Fix 2:** 
I ran `heroku run python` and inspected `dir(square.client)`. This showed which classes were actually available. In my version, the correct class was `Square` and `SquareEnvironment`, not `Client`. I updated `apps/payments/utils.py` to import the right objects.

**Lesson Learned 2:** 
The *Python Square SDK* has changed across versions. Always confirm available classes with `dir()` on *Heroku* to avoid chasing outdated documentation.

**Bug 3:** 
When I attempted to initialise the `client` with:

    square = Square(
        access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
        environment=SquareEnvironment.SANDBOX
    )

the logs showed `TypeError: Square.__init__() got an unexpected keyword argument 'access_token'`.

**Fix 3:** 
I learned that in my SDK build, `Square` does not accept `access_token` in the constructor. I adjusted the code in `apps/payments/utils.py` to create the `client` with only `environment` and then attach the `token` later:

    import os
    from square.client import Square, SquareEnvironment

    square = Square(
        environment=SquareEnvironment.SANDBOX
    )

    square.access_token = os.getenv("SQUARE_ACCESS_TOKEN")
    payments_api = square.payments

**Lesson Learned 3:** 
Different builds of the *Square SDK* use different initialisation patterns. Never assume the examples in docs match the installed version. 

**Bug 4:** 
On the *Heroku* Eco plan, I could not run `heroku run python manage.py migrate`. The logs returned `Error: Cannot run more than 1 Eco size dynos.`

**Fix 4:** 
The Eco plan only allows one dyno. I solved this by scaling the web dyno down, running migrations, then scaling it back up:

    heroku ps:scale web=0
    heroku run python manage.py migrate
    heroku ps:scale web=1

**Lesson Learned 4:** 
On the *Heroku* Eco plan, I cannot run one-off commands while the web dyno is active. I need to scale down before running management commands or upgrade to the Hobby tier.

**Bug 5:** 
After scaling down with `heroku ps:scale web=0` and forgetting to scale back up, the app failed with `code=H14 desc="No web processes running"`.

**Fix 5:** 
I restarted the web dyno with `heroku ps:scale web=1`.

**Lesson Learned 5:** 
If I see *H14 errors*, it usually means I forgot to restart the web dyno after scaling it down.

## Webhook Integration Errors

**Bug 1:** 
I initially received `404 Not Found` responses from *Square* when sending test events. The issue was that my *Django* `urls.py` was misconfigured. I had duplicated `checkout/` in both `config/urls.py` and `apps/checkout/urls.py`, which created the path `/checkout/checkout/webhooks/square/`. Square was sending to `/checkout/webhooks/square/`, so *Django* could not find the route.

**Fix 1:** 
I removed the extra `checkout/` from `apps/checkout/urls.py` and left only:
    path("webhooks/square/", views.square_webhook, name="square_webhook")
This ensured the final URL was `/checkout/webhooks/square/`.

**Lesson Learned 1:** 
Always check how path prefixes combine in *Django* between the project’s `urls.py` and app-level `urls.py`. One extra prefix will create mismatches and cause 404 errors.

**Bug 2:** 
After fixing the URL, *Square* requests returned a `502 Bad Gateway` in *ngrok*. The cause was that I had *ngrok* running, but my *Django* server was not running in another terminal, so *ngrok* had nothing to forward to on `localhost:8000`.

**Fix 2:** 
I ensured `python manage.py runserver` was running in one terminal, and in a second terminal I ran `ngrok http 8000`.

**Lesson Learned 2:** 
Both the *Django* server and *ngrok* must be running at the same time. *Ngrok* forwards requests, but if *Django* is down, *ngrok* cannot deliver them.

**Bug 3:** 
Once Square reached *Django*, I still received `400 Bad Request`. The traceback showed:
    django.core.exceptions.DisallowedHost: Invalid HTTP_HOST header: 'conceptual-stridently-sadie.ngrok-free.dev'
This meant the *ngrok* domain was not in `ALLOWED_HOSTS`.

**Fix 3:** 
I updated `settings.py` to use a wildcard for all *ngrok* domains:
    ALLOWED_HOSTS = os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost,.ngrok-free.dev"
    ).split(",")

I also added a debug print:
    `print("ALLOWED_HOSTS:", ALLOWED_HOSTS)` to confirm `.ngrok-free.dev` was included at startup. I then updated my `.env` file to include `.ngrok-free.dev`:
    `ALLOWED_HOSTS=127.0.0.1,localhost,.herokuapp.com,.ngrok-free.dev`

**Lesson Learned 3:** 
Always include `.ngrok-free.dev` with a leading dot in `ALLOWED_HOSTS` so any random *ngrok* subdomain will be accepted. Also check for `.env` overrides, as they take priority over defaults in `settings.py`.


**Bug 4:** 
After fixing `ALLOWED_HOSTS`, my view still returned `400` with the error:
    `Webhook error: name 'json' is not defined`. This was because I tried to use `json.loads` without importing the `json` module.

**Fix 4:** At the top of `checkout/views.py`, I added: `import json`

**Lesson Learned 4:** 
Always check that required modules are imported before using them. Even simple oversights can break webhook handling.

**Bug 5:** 
I forgot to keep *ngrok* running, which caused *Square* to return `404 Not Found` again. When *ngrok* is stopped, the forwarding URL immediately becomes invalid.

**Fix 5:** 
I made a checklist:  
1. Start *Django* with `python manage.py runserver`.  
2. Start *ngrok* with `ngrok http 8000`.  
3. Copy the current HTTPS forwarding URL.  
4. Update the *Square* Notification URL to `https://<random>.ngrok-free.dev/checkout/webhooks/square/`. 

**Lesson Learned 5:** 
*Ngrok* subdomains change every run. If *ngrok* closes, the URL dies instantly. Always restart *ngrok* and update *Square*’s Notification URL before sending test events.

## Webhook Signature Verification Errors

**Bug:** After wiring up the *webhook endpoint*, I received `400 Bad Request` errors with the log message `Invalid signature`. The `SQUARE_SIGNATURE_KEY` was loading correctly, and the request body was being hashed with `HMAC-SHA256`, but the computed signature did not match the header sent by *Square*.

**Fix:** I first confirmed the correct header was being used (`X-Square-Hmacsha256-Signature`) and added debug prints for both the header signature and the computed value. The mismatch was due to *Square*’s signing process requiring the *concatenation of the notification URL and the request body*, not just the body alone. Updating the code to build the `string-to-sign` with:
    notification_url = f"https://{request.get_host()}{request.path}"
    string_to_sign = notification_url + request.body.decode("utf-8")
and then computing the `HMAC-SHA256` over that string produced a matching signature. After this correction, *Square* responded with `200 OK`.

**Lesson Learned:** *Square* webhook signature verification requires hashing the *full notification URL + raw body* string, not just the body. Always check *Square*’s official docs for the string-to-sign format. Using `request.get_host()` and `request.path` avoids hardcoding *ngrok* domains and ensures the `notification URL` matches exactly what *Square* uses. Adding debug prints for header and computed signatures side by side is essential for troubleshooting mismatches.

## Authentication Error

**Bug:** When I attempted to create a *Square* payment link from the profile page, the API consistently returned a `401 Unauthorized` error. I confirmed that my *Django* settings were loading the correct `sandbox token`, `base URL`, and `location ID`. The request headers logged as `Authorization: Bearer EAAA...`, and the debug output showed that the token, base URL, and location ID were aligned with sandbox mode. Despite this, *Square* still rejected the request. The problem was not with credentials but with the request payload format. I was incorrectly sending an `"order": {...}` object, which is not supported by the `CreatePaymentLink` endpoint in this context.

**Fix:** I updated the `payload` to use the `"quick_pay"` object instead of `"order"`. This matched the structure expected by the *Square* API and allowed the request to succeed. The corrected `payload` looked like this:

    payload = {
        "idempotency_key": str(uuid.uuid4()),
        "quick_pay": {
            "name": f"Order #{order.id}",
            "price_money": {
                "amount": int(order.total * 100),
                "currency": "GBP"
            },
            "location_id": settings.SQUARE_LOCATION_ID
        }
    }

After switching to `"quick_pay"`, *Square* returned a `200 OK` response along with a valid `payment_link.url`, and *Django* successfully redirected to the *Square* Sandbox Checkout page.

**Lesson Learned:** A `401 Unauthorized` error from *Square* does not always mean the token or location is wrong. If the credentials are correct but the payload is invalid for the endpoint, *Square* may still return `401`. Always cross-check the request body against the official *Square* API docs. For the `CreatePaymentLink` endpoint, `"quick_pay"` is the minimal, valid object for sandbox testing. Using `"order"` directly caused the error.

## Webhook Authentication Error

**Bug:** When I triggered a test `webhook` from the *Square Sandbox* dashboard, the request kept returning `400 Bad Request` with the message `Signature mismatch`. This meant *Django* was rejecting the webhook because the locally computed HMAC signature did not match the signature Square sent in the header. At first, I was using `request.headers.get("x-square-hmacsha256-signature")` to read the header, and only signing the raw body. Both of these caused issues: the header key wasn’t always read correctly, and Square signs the full HTTPS URL plus body, not just the body.

**Fix:** I switched to accessing the header from `request.META` for reliability:

    signature = request.META.get("HTTP_X_SQUARE_HMACSHA256_SIGNATURE", "")

Then I updated the signature computation to include the `HTTPS URL` (since *Square* always signs the `HTTPS` version, even when using *Ngrok*):

    webhook_url = request.build_absolute_uri().replace("http://", "https://")
    string_to_sign = webhook_url + body

After making these changes, the computed HMAC matched *Square*’s signature perfectly and the endpoint returned `200 OK`.

**Lesson Learned:** `Webhook` signature mismatches often come from subtle URL or header mismatches, not incorrect keys. *Square*’s webhook signatures always use the `HTTPS` version of the full URL plus the raw request body. Using `request.META` instead of `request.headers` ensures *Django* correctly retrieves the signature header, and replacing `http://` with `https://` aligns the signed string exactly with what Square expects.

## Webhook Integration Error

**Bug:** When testing the *Square* `webhook`, the `payload` caused a `JSONDecodeError` due to invalid *JSON* formatting. Even after correction, the `webhook` raised a `FieldError` because the Order model lacked the expected `square_order_id` field.  

**Fix:** 

1. Corrected `test_payment.json` by ensuring all keys and string values were enclosed in double quotes.  
2. Added `square_payment_id` and `square_order_id` fields to the *Order* model.  
3. Ran `makemigrations` and `migrate` to update the database schema.  
4. Set a test `square_order_id` value in the *Django* shell to match the test payload.  
5. Updated the `webhook` logic to locate the order using `square_order_id` and set the status to `"paid"` when *Square* returns `"COMPLETED"`.  
6. Used `curl.exe` with `--data-binary` to prevent `PowerShell` from altering *JSON* formatting.  
7. Temporarily commented out signature verification for local testing.  
8. Confirmed successful response (`OK`) and verified the order’s status and payment ID in the database.  

**Lesson Learned:** `PowerShell` often mangles *JSON* when using `-d` with multi-line or quoted content, so `--data-binary` or `Invoke-WebRequest` is safer for `webhook` testing. Always ensure model fields match the data you’re referencing in the `webhook` logic. Valid *JSON* must use double quotes for both keys and string values. Once verified locally, always re-enable the *Square* signature validation before pushing to *Heroku* for production security.

## Webhook Integration Error

**Bug:** When testing the *Square* `webhook` locally, *Django* returned multiple errors including `JSONDecodeError` (due to invalid *JSON*), `FieldError` (missing `square_order_id` field in the *Order* model), and `NameError` (missing `JsonResponse` import). The `webhook` also rejected local test payloads because of signature mismatch.

**Fix:** 

1. Corrected `test_payment.json` to use valid *JSON* with double quotes.  
2. Added `square_order_id` and `square_payment_id` fields to the *Order* model and migrated the database.  
3. Temporarily disabled signature verification for local testing.  
4. Created a test order in the *Order* table using the *Django* shell and linked it to `"ORDER123456"`.  
5. Added missing import line:  
       `from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse`  
6. Verified full request flow using `curl.exe` with `--data-binary` to prevent `PowerShell` from altering *JSON* structure.  
7. Confirmed `Order.status` successfully updated to `"paid"` and `square_payment_id` saved.  
8. Re-tested duplicate webhook to confirm graceful `"Duplicate event"` handling.

**Lesson Learned:** `PowerShell` requires the `--data-binary` flag to send *JSON* exactly as written. *Django*’s `JsonResponse` must be explicitly imported even when `HttpResponse` is already present. Always validate *JSON* syntax before parsing and temporarily disable signature verification when testing webhooks locally. Once deployed to *Heroku*, re-enable verification to secure production webhooks.

## Webhook Validation Error

**Bug:** When testing the *Square* `webhook` locally, I initially received signature mismatches and `500 errors` when using the `payment.created` event. The server either rejected requests with “Invalid signature” or failed to match incoming payment data to existing orders. This made it impossible to verify whether the `webhook endpoint` was actually functioning correctly.

**Fix:** I restructured the `square_webhook()` view in the *checkout* app to properly handle both signature verification and event parsing.  
Key changes included:

- Imported `JsonResponse` and `HttpResponseBadRequest` from `django.http` to handle responses cleanly.  
- Used `@csrf_exempt` and `@require_POST` decorators to allow external `POST` requests from *Square*.  
- Ensured that `request.build_absolute_uri()` was forced to HTTPS using  
      `webhook_url = request.build_absolute_uri().replace("http://", "https://")`  
  so that the computed signature matched the format used by *Square*’s `HTTPS webhooks`.  
- Implemented signature verification with  
      `hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha256)`  
  and base64-encoded the digest.  
- Wrapped all logic in defensive try/except blocks to safely handle malformed payloads and missing fields.  
- Added handling for `payment.created` and `payment.updated` events, including logic to mark matching orders as “paid” only when the payment status equals `"COMPLETED"`.  
- Implemented duplicate `webhook protection` to avoid redundant updates.

After testing with both `curl` and real *Square* test events through *ngrok*, the `webhook` now logs all events, correctly updates orders, and ignores duplicate or unmatched events with a `200 OK` response.

**Lesson Learned:** *Square*’s` webhook signature` must be generated using the *exact HTTPS URL* registered in the Developer Dashboard. When testing locally, *Django* builds `webhook URL`s with `http://`, which breaks signature verification unless replaced with `https://`.  
I also learned that *Square* sends several event types (`APPROVED`, `COMPLETED`, etc.), and my `webhook` should only mark orders as “paid” once the payment reaches `"COMPLETED"`. 
 
With signature verification now re-enabled and event parsing stable, the integration between *Django* and *Square* is fully secure and production-ready.

## Admin Field and Payment Verification Errors

**Bug:** While testing the *Square* verification feature, I was unable to manually enter a *Square* Payment ID in the *Django* Admin panel. The admin form either rejected changes, displayed “created_at cannot be specified,” or ignored the new value. In addition, saving fake IDs did not display correctly in the Orders table.

**Fix:** I reviewed the *OrderAdmin* configuration in *admin.py* and identified two issues:

1. `readonly_fields` included `square_payment_id` and `created_at`, which prevented editing non-editable fields.  
2. The `created_at` field triggered a `FieldError` because it was marked as `auto_now_add=True` in the model but still being rendered as editable.

To fix this:  
- I removed `square_payment_id` from `readonly_fields` during testing so manual IDs could be entered.  
- I set `readonly_fields = ("created_at", "verified_on")` to prevent *Django* from treating those fields as editable.  
- I confirmed the `square_payment_id` appeared correctly in the list view by adding it to `list_display`.

After the fix, I successfully added fake payment IDs, saved them, and confirmed they persisted correctly in the Orders table.

**Lesson Learned:** *Django* will raise a `FieldError` if an admin form tries to edit any model field marked as non-editable (e.g., `auto_now_add=True`).  

For testing, temporarily removing fields from `readonly_fields` is fine, but they should be restored later for data integrity. This debugging process also reinforced the difference between `square_order_id` (*Square*’s internal reference) and `square_payment_id` (used by *Square*'s* Payments API). Entering a fake ID in the wrong field initially caused confusion but clarified how both fields serve distinct roles.

## Database Integrity and Square Order Sync

**Bug:** When running the new *Square* checkout integration, *Django* raised an `IntegrityError` complaining about a `null value in column "order_type"` in the `checkout_order` table. The model no longer contained that field, but the database schema still required it. This caused the order creation process to fail before the Square API could be called.

**Fix:** I restored the missing `order_type` field to the `Order` model and gave it a default value of `"event"`. This ensured every order had a valid type and allowed *Django* and the database schema to match. Because the column already existed in the database, the subsequent migration was safely faked using:

    python manage.py migrate checkout 0003 --fake

After that, the checkout flow successfully created local orders and sent requests to the *Square Sandbox API* to generate external orders and payments. The *Square* webhooks returned `payment.created` and `payment.updated`, and the order was automatically marked as paid.

**Lesson Learned:** If *Django* reports missing or duplicate columns, the issue is usually a mismatch between model definitions and existing migrations. Adding a default value or faking the migration is safer than manually altering tables. Always ensure migrations and schema stay in sync before testing API integrations.

### Template Display Error

**Bug:** The order summary on the checkout and payment pages showed “None” for event items instead of displaying the correct event name and details. This happened because the template referenced `{{ item.event.title }}`, but the `title` field in the *Event* model is optional and often left blank.

**Fix:** Replaced `{{ item.event.title }}` with `{{ item.event }}` in the order summary loop.  
*Django* automatically calls the *Event* model’s `__str__()` method, which returns the correct readable format:  
`"{artist} @ {venue} | {gig_date}"`.  
This ensures event details display correctly even when the optional `title` field is empty.

**Lesson Learned:** When displaying model data in templates, always consider whether the referenced field can be blank.  
If the model has a meaningful `__str__()` method, using `{{ object }}` is a safer and cleaner approach than referencing a nullable field directly.

### Logic Error

**Bug:** Delivery and booking fee charges were not being carried over to the order summary page after checkout. The basket correctly displayed both charges, but the checkout total remained unchanged, only reflecting raw item prices.

**Fix:** Rewrote the `basket_checkout` view to mirror the fee logic used in the basket. Added `Decimal`-based calculations for both booking and delivery fees inside the order creation loop:
    subtotal += line_total + (booking_fee * item.quantity) + delivery_fee
This ensured both charges were included in `order.subtotal` and `order.total` before saving.

**Lesson Learned:** When performing multi-step calculations across views, always duplicate or abstract shared logic (e.g. into a helper function) so updates remain consistent. The basket and checkout must use identical fee logic to avoid mismatched totals.

### Template Logic Error

**Bug:** Messages confirming deleted pending orders `(“4 order(s) deleted)”)` appeared in the basket view instead of the “Orders in Progress” section. This caused confusion since the message was unrelated to basket actions.

**Fix:** Tagged order deletion messages in the user view with `extra_tags="orders"` and filtered message display in templates.  
In the basket template, I excluded messages containing `"orders"` from the flash message loop. In the user profile template, I added a dedicated message block under “Orders in Progress” to display messages with the `"orders"` tag only.

**Lesson Learned:** When using *Django*’s messages framework across multiple views, tagging messages is essential for controlling where they appear. Filtering messages by tags keeps unrelated alerts confined to the correct page context.

### Search Input Responsive Sizing (Mobile) Issue

**Bug:** In mobile view, the search input fields inside the `offcanvas` were far too wide and pushed the layout beyond the screen width. They also expanded even when not active, causing alignment issues.

**Fix:** I added specific width constraints within a media query for screens under 768px and adjusted the offcanvas width so it “hugged” the search inputs. The `offcanvas` now expands only when the search is clicked. This ensures inputs stay within the viewport and aligned correctly.

**Lesson Learned:** Always test responsive elements both in collapsed and expanded states — *Bootstrap*’s `offcanvas` width doesn’t automatically scale with its contents, so manual sizing adjustments are sometimes necessary.

### Merch Search Functionality Issue

**Bug:** The merch search stopped working after introducing form-based searches for artists and venues. Pressing enter on the merch search field no longer redirected to results.

**Fix:** I replaced the static `<input>` with a proper form pointing to `{% url 'products:search_view' %}` and used `name="q"` consistently across all fields. Updated the JavaScript `handleMerchSearch()` to handle the same `id="merch-search"` (desktop) and `id="merch-search-mobile"` (mobile)` logic, matching the artist and venue setups. Adjusted `views.py` to detect merch queries and display either multiple results or a single merch item styled like the merch list.

**Lesson Learned:** Consistency between input names, form actions, and view logic is key. Even one mismatched `name` or `id` can break a working search feature.

## Redirect Loop for Continue Shopping Button

**Bug:** When I added the `Continue Shopping` button to the basket template, clicking it did nothing. The button rendered fine, but nothing happened when I clicked it. There was no console output and no redirect. When I visited `/basket/continue-shopping/` directly in the browser, it worked and redirected properly, but clicking the button on the basket page just reloaded the basket instead of returning to the merch list.

**Fix:** I found that I hadn’t imported the `continue_shopping` view at the top of `urls.py`. After adding the import, the button finally triggered the view, but it still redirected back to the basket instead of the merch page. The issue turned out to be that the `HTTP_REFERER` header pointed to the basket page itself, creating a redirect loop. I fixed this by adding a conditional check to compare the referrer URL with the basket URL. If they matched, I forced the redirect to the merch list page instead. My final view looked like this:

    def continue_shopping(request):
        previous_page = request.META.get('HTTP_REFERER')
        basket_url = request.build_absolute_uri(reverse('basket:basket_view'))
        merch_url = reverse('products:merch_list')

        if not previous_page or previous_page == basket_url:
            previous_page = merch_url

        return HttpResponseRedirect(previous_page)

**Lesson Learned:** If a button doesn’t work, the issue is usually a missing import or a redirect loop. The `HTTP_REFERER` header can point to the same page, so it’s not always safe to rely on it without a fallback. I learned to always confirm a new view works by testing its URL directly before assuming there’s a *CSS* or *JavaScript* problem. I also learned to use clear conditional logic to prevent looping redirects when handling referrer-based navigation in *Django*.

## Continue Shopping Persistent Redirect Fallback Logic

**Bug:** After I added the *Continue Shopping* button to the basket, it initially redirected correctly while logged in, but after logging out and back in, it always went to the merch page even if my basket contained an event ticket. The issue occurred because logging out cleared the session, which meant the `last_shop_type` value used for redirection was lost. Without session data, the fallback always defaulted to merch.

**Fix:** I modified the `continue_shopping` view to include a third fallback option that inspects the contents of the user’s basket when the session data is missing. This allowed *Django* to determine whether the basket contained an event or merch item and redirect accordingly, even after logout.  

The final working view now looks like this:

    def continue_shopping(request):
        """
        Acts like the standard back button:
        - Uses a valid referrer if one exists.
        - Falls back to remembered shop type (session).
        - If session was cleared (after logout), inspects basket contents.
        """
        previous_page = request.META.get('HTTP_REFERER')
        basket_url = request.build_absolute_uri(reverse('basket:basket_view'))

        merch_url = reverse('products:merch_list')
        events_url = reverse('products:events')

        # Step 1: Use the referrer if it's valid
        if previous_page and previous_page != basket_url:
            return HttpResponseRedirect(previous_page)

        # Step 2: Try the session
        last_shop_type = request.session.get('last_shop_type')
        if last_shop_type == 'events':
            return HttpResponseRedirect(events_url)
        elif last_shop_type == 'merch':
            return HttpResponseRedirect(merch_url)

        # Step 3: Session missing — inspect basket contents
        if request.user.is_authenticated:
            basket, created = Basket.objects.get_or_create(user=request.user)
            if basket.items.filter(event__isnull=False).exists():
                return HttpResponseRedirect(events_url)
            elif basket.items.filter(merch__isnull=False).exists():
                return HttpResponseRedirect(merch_url)

        # Step 4: Fallback
        return HttpResponseRedirect(merch_url)

**Lesson Learned:** Sessions are wiped on logout, so anything stored in them must have a backup plan. I learned that basket-based logic is the most reliable fallback when persistent behaviour is required across sessions. Adding this third check made the *Continue Shopping* button consistent across all user states — logged in, logged out, and freshly returned to the site. It also reinforced how important clear redirect logic is when combining referrers, sessions, and model data in *Django*.

## Calculation Error

**Bug:** When testing the checkout summary, I noticed that the total on the right-hand side of each item was not including the associated booking or delivery fees. Additionally, the booking fee for multiple tickets only showed £1.00 for six tickets, which was incorrect. The logic used in the `checkout_view` was not multiplying the booking fee properly per quantity, and the total_with_fees field was not being updated to reflect the final cost.

**Fix:** I updated the fee calculation logic inside the `checkout_view` function to multiply the event booking fee correctly and ensure that the total for each item (including delivery or booking) was added to the right-hand column. The corrected section now ensures that event and merch items each calculate and display accurate totals. The updated code used this logic:  

    for item in order.items.all():
        item.line_total = item.price * item.quantity

        if item.event:
            item.booking_fee = (item.event.price * Decimal('0.10')) * item.quantity
            item.total_with_fees = item.line_total + item.booking_fee

        elif item.merch:
            base_fee = Decimal('5.00')
            extra_fee = (base_fee * Decimal('0.50')) * (item.quantity - 1)
            item.delivery_fee = base_fee + extra_fee if item.quantity > 1 else base_fee
            item.total_with_fees = item.line_total + item.delivery_fee

After this fix, the checkout summary displayed:
- “Cost: X × £Y ea” for each item  
- Correct 10% booking fee for ticket totals  
- Properly calculated delivery charge for merch items  
- Accurate right-hand totals including all charges  

**Lesson Learned:** I learned that reusing shared logic from other views like `basket_view` requires careful attention to how quantities and related fields are calculated. Even a small oversight, like not multiplying a percentage fee per quantity, can lead to visible errors in totals. Ensuring consistent fee calculations across both *Django* views avoids mismatched totals between basket and checkout summaries.

## Runtime Error for Checkout and Payment Summary Totals

**Bug:** The totals on the right-hand side of both the checkout and payment summary templates only showed the base item cost (`price × quantity`). The per-item booking and delivery fees were missing, even though they were correctly calculated in the `calculate_fees()` function. The grand total at the bottom was correct, but each item’s total on the right-hand side did not include the added fees.

**Fix:** I confirmed through debug prints that the per-item attributes (`booking_fee`, `delivery_fee`, and `total_with_fees`) were being correctly attached to each item inside `calculate_fees()`. However, the template still showed old totals because *Django* was re-fetching the `QuerySet` when rendering the page, losing those in-memory attributes.

The fix was to convert the queryset into a list before passing it to `calculate_fees()` so that the modified objects would be preserved and sent to the template. I also updated the template to reference the correct variable `item.total_with_fees` instead of `item.line_total`.

    def prepare_order_context(order):
        """Recalculate fees and return a consistent context for checkout/payment views."""
        items = list(order.items.all())  # convert queryset to list to preserve attached attributes
        order_items, subtotal, delivery_charge, basket_total = calculate_fees(items)

        context = {
            "order": order,
            "order_items": order_items,
            "subtotal": subtotal,
            "delivery_charge": delivery_charge,
            "basket_total": basket_total,
        }

        return context, subtotal, basket_total

**Lesson Learned:** When attaching calculated attributes to *Django* model instances (like per-item totals with fees), the queryset must be converted into a list before rendering. If I pass a `QuerySet` directly, *Django* re-queries the database during template rendering and drops any in-memory attributes. Always verify the data reaching the template with debug prints to confirm that calculated fields persist through the context.

## Basket and Checkout Totals Calculation Runtime Error

**Bug:** When loading the basket or checkout pages, I repeatedly hit a `TypeError: 'decimal.Decimal' object is not callable` or `AttributeError: 'BasketItem' object has no attribute 'get_line_total'`. The issue started after introducing the new `calculate_fees()` logic, where the code called `item.line_total()` to get totals for each basket or order item. In some cases, `line_total` was being overwritten with a `Decimal` value, and later we renamed the method to `get_line_total()` to prevent this conflict — but only in the `OrderItem` model. The `BasketItem` model did not have that method, which caused the final error when the basket page loaded.

**Fix:** I synchronized both models so they shared the same structure. 

In `OrderItem`, I kept:
    
    def get_line_total(self):
        return self.quantity * self.price

    @property
    def line_total(self):
        return self.get_line_total()

Then I added the same structure to `BasketItem`:

    def get_line_total(self):
        if self.event:
            return (self.event.price or 0) * self.quantity
        if self.merch:
            return (self.merch.price or 0) * self.quantity
        return 0

    @property
    def line_total(self):
        return self.get_line_total()

Finally, I updated all references inside `calculate_fees()` to use `item.get_line_total()` instead of `item.line_total()`. After restarting the server, both basket and checkout pages loaded without error, and the totals rendered correctly.

**Lesson Learned:** Method and property naming collisions can quietly break *Django* logic, especially when reusing calculation functions across multiple models. A method like `line_total()` should never be reassigned a numeric value. Using a uniquely named method like `get_line_total()` plus a property for templates keeps backend logic clean and avoids callability errors. It also helps to ensure that related models (like `BasketItem` and `OrderItem`) stay synchronized when shared logic depends on them.

## Environment Variable Load Failure

**Bug:** When I tried to render the *Square* payment form, the credit card section stayed blank and the browser console repeatedly showed the message `Square app or location ID missing from dataset.` Even though my `.env` file had the correct Square credentials, the values for `settings.SQUARE_APPLICATION_ID` and `settings.SQUARE_LOCATION_ID` were empty inside *Django*’s runtime. I confirmed this by running `python manage.py shell` and printing the settings, which returned nothing.  

**Fix:** I discovered that *Django* was loading its settings module before reading the `.env` file, meaning the Square credentials were never actually available when the app started. To fix it, I did the following:

1. Moved the `load_dotenv(BASE_DIR / ".env")` line to the very top of `config/settings.py` so the environment variables were loaded before any other imports.
2. Added `DJANGO_SETTINGS_MODULE=config.settings` to the `.env` file to make sure *Django* used the correct settings module.
3. Restarted the server and confirmed that `python manage.py diffsettings | findstr SQUARE` now showed the correct values.
4. Verified that `DEBUG SQUARE SETTINGS:` printed both the `SQUARE_APPLICATION_ID` and `SQUARE_LOCATION_ID` inside the terminal.
5. Removed all temporary debug print statements from both `settings.py` and the payment views.

After these changes, the *Square* app and location IDs finally appeared in the template, and the credit card form rendered correctly.

**Lesson Learned:** Environment variables must load before *Django* initializes any of its settings. The placement of `load_dotenv()` inside `settings.py` is critical—if it’s too low, environment values won’t be read in time. Always define `DJANGO_SETTINGS_MODULE` explicitly when using a nested configuration folder like `config/`. When debugging missing credentials or blank values, check the live runtime using `python manage.py diffsettings` to confirm what *Django* actually sees instead of assuming the `.env` file is being read correctly.

## Deployment and Payment Integration

**Bug:** After deploying to *Heroku*, the payment page failed to show the Square credit card input. Console logs reported `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')` and later `InvalidApplicationIdError: The Payment 'applicationId' option is not in the correct format.`

**Fix:** I discovered that the card field was being blocked initially because my script (`square-checkout.js`) ran before the DOM had fully loaded. I replaced `document.addEventListener("DOMContentLoaded", ...)` with `window.addEventListener("load", ...)` and removed the old `setTimeout` wrapper. This ensured that all elements were available before binding the event listener. The corrected bottom section of the file was as follows:

    window.addEventListener("load", async () => {
        console.log("Window fully loaded — starting Square init");
        ...
        initSquare(appId, locationId);
    });

Once this was corrected, I redeployed using the standard *Heroku* workflow.

The `InvalidApplicationIdError` appeared because my *Heroku* `Config Vars` had not been set for `SQUARE_APPLICATION_ID` and `SQUARE_LOCATION_ID`. I fixed this by opening *Heroku → Settings → Reveal Config Vars* and adding:

    SQUARE_APPLICATION_ID = sandbox-sq0idb-xxxxxxxxxxxxxx
    SQUARE_LOCATION_ID = Lxxxxxxxxxx

After redeployment, the console output confirmed valid values and the **Square* `iframe` loaded correctly. To verify HTTPS integrity, I ran an *SSL Labs* test and received three A– ratings, proving the encryption setup was sound. The *Chrome* dangerous warning was confirmed as a temporary false positive due to *Heroku*’s new subdomain reputation and did not affect site security.

**Lesson Learned:** The credit card `iframe` will not load unless both HTTPS and valid *Square* credentials are present. Always test the page after full load events to avoid null references, confirm that *Heroku* `Config Vars` are set correctly, and verify SSL status using external tools before assuming an error in code. The *Chrome* red “Dangerous site” warning can safely be ignored on a new *Heroku* domain once the *SSL* rating is verified as A or higher.

## Calculation Error

**Bug:** The basket subtotal displayed correctly, but the delivery fees were being calculated as a flat £5.00 per merch item, regardless of quantity or additional items. This meant that multiple merch products did not apply the intended 50% reduction for subsequent items, and quantities were not being multiplied correctly.

**Fix:** I updated the delivery fee logic inside the `calculate_fees()` function in `views.py`. The new code calculates £5.00 for the first merch item and £2.50 (50%) for each additional merch item multiplied by its quantity.  
The corrected section:

    # Per-item delivery fee (£5 for first merch item, +50% per additional item * quantity)
    if item.merch:
        if delivery_charge == 0:
            # First merch item (whatever its quantity)
            item.delivery_fee = Decimal("5.00") * item.quantity
        else:
            # Additional merch items at 50% of base per quantity
            item.delivery_fee = Decimal("2.50") * item.quantity
        delivery_charge += item.delivery_fee
    else:
        item.delivery_fee = Decimal("0.00")

After this fix, each merch item line now adds the correct delivery fee.  
For example:  
- Hoodie (£5 delivery)  
- 4 × T-shirt (£2.50 × 4 = £10 delivery)  
- Event tickets (no delivery fee, just 10% booking)

**Lesson Learned:** I learned that accumulating delivery charges across multiple items must consider both item count and type. Using a simple accumulator (`+=`) with condition-based logic ensures flexible delivery calculations while maintaining accuracy. Always confirm quantity multiplication when fees depend on item counts.

## Navigation Routing Error

**Bug:**  After clicking *Proceed to Payment* and moving to the order summary, clicking *View Basket* from the navbar or hamburger menu redirected to an empty basket instead of restoring the previous basket contents. The issue occurred because the navigation links always pointed to `basket_view`, which displays the active basket model — but after an order was created, the basket was cleared, leaving nothing to show.

**Fix:** I implemented conditional logic in both the main navbar and hamburger menu templates. When a user is logged in and has a pending order, *View Basket* now routes to the `restore_basket` view instead of `basket_view`. This view rebuilds the basket from the pending order items, restoring all previous contents.  

Now, when a user proceeds to payment and then clicks *View Basket*, their previous basket is correctly restored, and a confirmation message appears: *“Your previous basket has been restored.”*

**Lesson Learned:** I learned that once an order is generated, the basket becomes empty because its items are moved to the order model. To restore continuity for the user, it’s best to provide a dedicated `restore_basket` route and conditionally link to it in the navigation. This preserves a seamless shopping flow without losing the user’s original basket context.

## 404 & 500 Template Routing Error

**Bug:** The custom `404` and `500` error pages were not displaying. Instead, *Django*’s default debug pages appeared, even though the custom templates existed in the `templates/` directory. This happened because there were no properly configured global `error handlers` or routes telling *Django* to use the custom templates. Additionally, the original `404` and `500` pages only had “Return Home” buttons rather than a contextual back button that linked users to their previous page.

**Fix:** I created a new `config/views.py` file to define global `error handlers` for both `404` and `500` responses and passed a `previous_page` variable to each template. This variable uses `request.META.get("HTTP_REFERER", "/")` to safely identify the previous URL or default to the homepage. I then registered these handlers in `config/urls.py` and replaced the static “Return Home” button in both templates with a contextual back button.  

**Lesson Learned:** I learned that *Django* only uses custom error templates when global `error handlers` are explicitly defined and registered. 

Testing Logs

## Testing

All functionality was tested manually by working through user stories. Testing was carried out in Google Chrome, Edge, Brave and Firefox across desktop and mobile screen sizes. DevTools were used to check responsiveness and console errors. Forms and dynamic elements were tested for validation, correct behaviour, and feedback.

### User Stories

#### Ticket Oversell Guardrail

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

#### Input Text Visibility Fix

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

#### Delivery and Booking Fees Carry Over to Order Summary

**User Story:** 

As a **user**, I want **delivery and booking fees shown in my basket to be accurately carried over to my checkout summary**, so that I **always see the correct final total before payment**.

**What Was Tested:** 

I tested whether event booking fees (10%) and merch delivery fees (£5 + 50% per additional item) displayed in the basket were reflected correctly in the order summary after checkout creation.

**Acceptance Criteria:** 

[x] Booking fee included per event ticket in checkout total.  
[x] Delivery fee included per merch item in checkout total.  
[x] Checkout total matches basket total exactly.  
[x] Order stored with both fee values in subtotal and total.  

**Tasks Completed:** 

[x] Updated `basket_checkout` view to include both fees.  
[x] Verified totals using multiple event and merch combinations.  
[x] Cross-checked database entries for accurate totals.  
[x] Confirmed display consistency in both basket and checkout templates.  

**Notes:** 

Initial totals excluded additional fees due to logic mismatch between basket and checkout views. Adjusting `basket_checkout` to include both charges resolved the discrepancy entirely.

#### Order Deletion Messages Appear Under Orders in Progress

**User Story:**  

As a **user**, I want **confirmation messages for deleted orders to appear directly under “Orders in Progress”** so I can **clearly see the result of my action without confusion**.

**What Was Tested:** 

Tested visibility and location of deletion messages after removing pending orders from the user profile page.

**Acceptance Criteria:**

[x] Deleted order message appears in red below “Orders in Progress”.  
[x] Message no longer appears in basket view.  
[x] Message persists only for current request and clears on refresh.  
[x] Basket error messages remain unaffected.  

**Tasks Completed:** 

[x] Tagged order deletion messages with `extra_tags="orders"`.  
[x] Filtered message rendering in `basket.html` to exclude `"orders"`.  
[x] Added message block under Orders in Progress to show only `"orders"` messages.  
[x] Verified display after both single and bulk deletions.  

**Notes:** 
 
The original “4 order(s) deleted” message was caused by shared message context between basket and orders views. Introducing message tags allowed each section to handle its own alerts cleanly and consistently.

#### Search Input Responsive Sizing

**User Story:**

As a **user**, I want **the search inputs in the mobile menu to fit within the screen** so that **the interface remains clean and easy to use on smaller devices**.

**What Was Tested:**

Tested how search inputs for Artist, Venue, and Merch displayed across mobile widths, ensuring they only expand when active and stay aligned.

**Acceptance Criteria:** 

- [x] Inputs do not exceed the screen width.  
- [x] Offcanvas width matches search input width.  
- [x] Inputs expand only when search is clicked.  
- [x] Layout remains consistent between 320px and 750px.  

**Tasks Completed:**  

- [x] Adjusted mobile media query for offcanvas width.  
- [x] Limited input width under 768px.  
- [x] Ensured expansion only triggers when search toggled.  

**Notes:**  

After adjustments, the offcanvas now expands dynamically without breaking layout. Input boxes scale properly, maintaining perfect alignment.

#### Merch Search Functionality

**User Story:**  

As a **user**, I want to **search for merch items (like hoodies or flags)** and see **all relevant results or a single item displayed consistently with the merch list design**.

**What Was Tested:** 

Tested merch search on both desktop and mobile for single and multiple results.

**Acceptance Criteria:**  

- [x] Pressing enter on merch search triggers a result.  
- [x] Multiple matches display as a merch list grid.  
- [x] Single match displays centered using the same card style.  
- [x] Back button returns to merch list.  

**Tasks Completed:** 

- [x] Replaced static input with a form using `name="q"`.  
- [x] Unified JS logic for desktop and mobile search IDs.  
- [x] Updated view logic to detect and render single vs. multiple results.  

**Notes:**

The merch search now behaves identically to artist and venue searches. Single-item searches render a centered card, maintaining layout consistency.

#### Continue Shopping Button Redirect

**User Story:** 

As a **user**, I want to **click a "Continue Shopping" button on the basket page**  so that **return to browsing merch or events without starting over**.

**What Was Tested:**  

I tested the functionality of the new "Continue Shopping" button on the basket page to ensure that it redirected users back to the merch list when the basket page was their referrer. I also confirmed that the button worked when the user arrived at the basket from either the events or merch page.

**Acceptance Criteria:** 

[x] The "Continue Shopping" button appears correctly at the top of the basket page.  
[x] Clicking the button from the basket redirects to the previous page if the user came from events or merch.  
[x] No redirect loop occurs.  
[x] The button works the same in both desktop and mobile views.

**Tasks Completed:**
  
[x] Added `continue_shopping` view to `apps/basket/views.py`.  
[x] Added corresponding URL path to `apps/basket/urls.py`.  
[x] Imported the new view properly at the top of the file.  
[x] Updated the view logic to prevent redirect loops when `HTTP_REFERER` matches the basket page.  
[x] Tested redirection from basket, events, and merch pages.  

**Notes:** At first, the button did nothing because I forgot to import the `continue_shopping` view. After importing it, I noticed a redirect loop caused by the `HTTP_REFERER` pointing back to the basket. Adding a comparison between the basket URL and the referrer fixed the loop. Once that was done, both the "Continue Shopping" and test links redirected correctly to the merch list. The button now behaves as expected in all cases, ensuring smooth navigation for users.

#### Continue Shopping Persistent Redirect Fallback Logic

**User Story:** 

As a **user**, I wanted the **Continue Shopping button to return me to my last shop section, even after logging back in**, so I **don’t lose my place while shopping**.

**What Was Tested:** 

I tested the updated `continue_shopping` logic to ensure it redirected to the correct page under all conditions — whether I was logged in, logged out, or had no session memory. 

**Acceptance Criteria:**

[x] Redirects to events page if basket contains event tickets.  
[x] Redirects to merch page if basket contains merch items.  
[x] Works immediately after adding an item without page reload.  
[x] Works correctly after logging out and back in.  
[x] Falls back to merch if basket is empty.  
[x] No redirect loops or broken links occur.

**Tasks Completed:**  

[x] Updated `continue_shopping` view to inspect basket contents.  
[x] Added logical priority: referrer → session → basket → default.  
[x] Verified that basket queries return correct event/merch results.  
[x] Tested in both logged-in and logged-out states.  
[x] Confirmed consistent behaviour across desktop and mobile.

**Notes:**

Before the change, the button always redirected to merch after logout because session data was cleared. By checking basket contents when the session is gone, the redirect now behaves intuitively every time. This made the *Continue Shopping* button resilient, predictable, and user-friendly across all scenarios.

#### Checkout Summary Fee and Total Calculations

**User Story:**  

As a **user**, I wanted the **checkout summary to clearly display item costs including booking and delivery fees**, so that I **can understand exactly how my total is calculated before payment**.

**What Was Tested:**  

I tested the updated checkout summary view and template to confirm that all cost breakdowns were displayed accurately. This included checking quantity, unit price, booking fees (for tickets), and delivery fees (for merch). I also confirmed that the totals on the right reflected the full cost of each item with all applicable charges.  

**Acceptance Criteria:**  

[x] Each item displays “Cost: X × £Y ea” under its description.  
[x] Merch items show “Delivery: £Z” correctly.  
[x] Ticket items show “Booking Fee (10%): £Z” correctly.  
[x] The total on the right reflects full cost (item + applicable fees).  
[x] Subtotal and final total correctly sum all charges.  
[x] Layout remains aligned and consistent across all items.  

**Tasks Completed:**  

[x] Updated `checkout_view` in `apps/checkout/views.py` to properly calculate `total_with_fees` per item.  
[x] Multiplied the 10% booking fee by the quantity of tickets for accurate totals.  
[x] Ensured delivery fee scales correctly for multiple merch items.  
[x] Updated the template to display full fee breakdown beneath each item.  
[x] Verified subtotal, delivery, and total calculations match backend logic.  

**Notes:**  

Before the fix, the total for each item didn’t include the 10% booking fee or delivery charge, and the fee calculation only applied once per item line instead of per quantity. After the correction, each item’s total reflects the full cost with all fees, matching the intended checkout logic and user expectations. The summary is now accurate, readable, and consistent with the basket display.

#### Checkout and Payment Summary Totals

**User Story:** 

As a **user**, I wanted to **see accurate per-item totals that include all booking and delivery fees on both the checkout and payment summary pages** so that I **can clearly understand the full cost before completing my order**.

**What Was Tested:** 

I tested that each item’s right-hand total correctly included booking and delivery fees, and that the basket total matched the combined value of all item totals. I verified that both templates displayed consistent values and that no incorrect base prices were shown.

**Acceptance Criteria:**  

- [x] Each item’s total includes all fees (booking and delivery).  
- [x] The checkout and payment templates show matching totals.  
- [x] The overall basket total equals the sum of all item totals.  
- [x] No item displays only the base price × quantity.  
- [x] Debug prints confirm that fee attributes persist in the context.

**Tasks Completed:** 

- [x] Converted `order.items.all()` to a list in `prepare_order_context()` to preserve in-memory attributes.  
- [x] Ensured `calculate_fees()` attaches `booking_fee`, `delivery_fee`, and `total_with_fees` to each item.  
- [x] Updated both templates to display `item.total_with_fees` instead of `item.line_total`.  
- [x] Verified debug output in the terminal showed correct per-item totals.  
- [x] Reloaded pages to confirm right-hand totals reflected all fees.

**Notes:**

Before the fix, only base prices were shown because *Django* re-fetched the queryset during rendering, losing the in-memory fee attributes. After converting the queryset to a list and ensuring the templates referenced `item.total_with_fees`, all per-item and basket totals displayed correctly, matching the backend calculations.

#### Basket and Checkout Totals Calculation

**User Story:** 

As a **user**, I want **the basket and checkout totals to include the correct booking and delivery fees for each item** so that I can **see accurate costs before payment**.

**What Was Tested:** 

I tested the basket and checkout pages to confirm that all per-item totals (including booking and delivery fees) displayed correctly and that the new `get_line_total()` method was being called consistently across both models.

**Acceptance Criteria:** 

[x] Basket page loads without `TypeError` or `AttributeError`.  
[x] Checkout page loads without backend errors.  
[x] Each event item correctly applies a 10% booking fee.  
[x] Each merch item correctly adds a £5 delivery fee.  
[x] The totals on the right reflect base price + fees accurately.  
[x] Both `BasketItem` and `OrderItem` use the same `get_line_total()` logic.  

**Tasks Completed:**

[x] Renamed `line_total()` method to `get_line_total()` in `OrderItem`.  
[x] Added matching method and property to `BasketItem`.  
[x] Updated `calculate_fees()` to use `item.get_line_total()`.  
[x] Restarted *Django* server to clear overwritten cached class definitions.  
[x] Verified totals render correctly in templates after the fix.  

**Notes:** 
 
This bug was caused by method overwriting and inconsistent naming between models. Aligning both models resolved the problem and ensured that totals remain accurate across all views. The `calculate_fees()` function now works universally for both basket and order items without risk of breaking callable logic again.

#### Payment Integration and Deployment Testing

**User Story:** 

As a **user**, I want to **complete a secure checkout using the *Squar*e* payment form** so that I can **confidently pay for my order online**.

**What Was Tested:** 

I tested the deployment of the live app on *Heroku* and verified that the *Square* credit card form rendered correctly, processed sandbox payments, and redirected to the success confirmation page without any console or SSL errors. The test covered both the technical flow (payment tokenization and order confirmation) and the security integrity (HTTPS and certificate validation).

**Acceptance Criteria:** 

- [x] The app deployed successfully on *Heroku* with `DEBUG = False`  
- [x] All static files collected and loaded without errors  
- [x] The *Square* card input field appeared correctly after page load  
- [x] Sandbox test cards processed successfully with valid redirects  
- [x] `SQUARE_APPLICATION_ID` and `SQUARE_LOCATION_ID` loaded from Config Vars  
- [x] The checkout used HTTPS with a valid SSL certificate  
- [x] No mixed-content or *JavaScript* console errors on live site  
- [x] *Chrome*’s “dangerous site” flag identified as a false positive  
- [x] *SSL Labs* test returned three A– ratings confirming certificate validity  

**Tasks Completed:**

- [x] Updated `square-checkout.js` to use `window.addEventListener("load", ...)` instead of `DOMContentLoaded`  
- [x] Removed old `setTimeout` wrapper to prevent premature execution  
- [x] Set *Heroku* Config Vars for *Square* sandbox keys  
- [x] Verified live deployment with `git push heroku main`  
- [x] Tested sandbox payments using *Square*-provided card numbers (e.g., Visa `4111 1111 1111 1111`)  
- [x] Checked SSL integrity using *SSL Labs* external tool  
- [x] Confirmed *Chrome* red warning was unrelated to app security  

**Notes:** 

During initial tests, the payment form did not appear due to the script running before the DOM had fully loaded. Switching to the `window.onload` event solved this. A second issue occurred when the app and location IDs returned `None` in the console; adding them to *Heroku Config Vars* fixed the integration. After successful redeployment, the sandbox card form rendered perfectly, payments processed, and the confirmation page loaded over secure HTTPS. The A– SSL rating confirmed encryption was valid, and the *Chrome* red screen was verified as a harmless new-domain flag. The payment integration is now live, stable, and secure.

#### Delivery Fee Multiplier Logic

**User Story:** 

As a **user**, I want the **basket to correctly apply delivery charges where the first merch item costs £5.00 and each additional item adds £2.50 per quantity**, so that **delivery fees are fair and consistent across multiple purchases**.

**What Was Tested:**

I tested the basket display to confirm delivery charges and totals were calculated and displayed accurately, including different combinations of merch and event items.  

**Acceptance Criteria:** 

- [x] First merch item shows a £5.00 delivery fee.  
- [x] Additional merch items apply £2.50 × quantity.  
- [x] Event tickets apply only a 10% booking fee.  
- [x] Subtotal and basket total reflect all delivery and booking fees accurately.  
- [x] Debug console confirms correct per-item fee breakdown.

**Tasks Completed:**

- [x] Added conditional delivery logic inside `calculate_fees()` for first and subsequent merch items.  
- [x] Tested various basket combinations (single item, multiple items, mixed merch + event).  
- [x] Confirmed subtotal and total values update correctly in the template.  
- [x] Verified debug logs show expected line totals and fee breakdowns.  

**Notes:**
  
This fix restored the intended delivery fee calculation after it was lost during earlier refactoring. The debug output was crucial for confirming the multiplier worked correctly and aligned with displayed totals. The fix now ensures delivery logic is scalable and consistent.

#### Basket Restoration After Proceeding to Payment

**User Story:** 

As a **user**, I want to **return to my basket with all items restored after clicking *Proceed to Payment***, so that I can **review or change my order without losing my selections**.

**What Was Tested:**

I tested the navigation and basket behavior after proceeding to payment and returning via the *View Basket* links in both the navbar and the hamburger menu.  

**Acceptance Criteria:** 

- [x] After proceeding to payment, *View Basket* restores the previous basket contents.  
- [x] The success message “Your previous basket has been restored” appears.  
- [x] *Order Summary* remains accessible in both navbar and hamburger menu.  
- [x] Non-logged-in users without a pending order only see *View Basket* linking to the normal basket.  
- [x] Navigation functions consistently across both desktop and mobile views.

**Tasks Completed:**

- [x] Added conditional logic for `restore_basket` routing in navbar dropdown.  
- [x] Applied identical logic to the hamburger menu basket section.  
- [x] Tested both navigation versions for pending and non-pending order states.  
- [x] Confirmed success message and basket repopulation work as expected.

**Notes:**
  
This fix resolved the empty basket issue and improved user flow between checkout and basket review. The new conditional routing ensures that users can always restore their previous basket if they return from payment or order summary pages.

#### Custom 404 and 500 Pages with Back Navigation

**User Story:**
 
As a **user**, I want to **see branded and consistent error pages when something goes wrong, with a back button that takes me to my previous page**, so I **don’t lose my place on the site**.

**What Was Tested:**

I tested both the 404 and 500 pages to confirm they render correctly with the back navigation feature and show the custom styling and messaging.  

**Acceptance Criteria:** 

- [x] Visiting a non-existent page loads the custom 404 template.  
- [x] Triggering the `/crash/` route loads the custom 500 template.  
- [x] Both pages show the “← Back” button and return to the referring page.  
- [x] If there’s no referrer, both pages safely link back to the homepage.  
- [x] The templates retain consistent site styling and layout.  

**Tasks Completed:** 

- [x] Created new `config/views.py` to hold global error handlers.  
- [x] Registered custom handlers in `config/urls.py`.  
- [x] Updated both 404 and 500 templates to use the `previous_page` variable.  
- [x] Tested functionality locally and in the deployed *Heroku* environment.  

**Notes:** 
 
Both error pages now function seamlessly and match the rest of the site’s branding. The back navigation works exactly like other templates, improving user flow and preventing unnecessary redirects to the homepage.
