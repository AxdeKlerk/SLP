# Searchlight Promotions (Upgrade)

![searchlight promotions logo and text](DOCS/images/logo.jpg)

# Table of contents

<details><summary>1 Introduction</summary>

[1.1 The Aim, Purpose and Goal of the Site](#11-the-aim-purpose-and-goal-of-the-site)

[1.2 Target Audience](#12-target-audience)  
</details>

<details><summary>2 Planning and Development</summary>

[2.1 Project Statement and ERD](#21-project-statement-and-erd)

[2.1.1 Identified Entities (Key Nouns)](#221-identified-entities-key-nouns)

[2.1.2 Key Relationships](#212-key-relationships)

[2.2 Wifreframes](#22-wireframes)

[2.3 User Journeys](#23-user-journeys)

[2.4 User Stories](#24-user-stories)

[2.4 Agile Methodology](#24-agile-methodology)

[2.4.1 Epics](#241-epics)

</details>

<details><summary>3 Features</summary>
[3.1 Typography]

[3.2 Colour Pallett]
</details>
<details><summary>4 Debugging, Testing, Deployment and Future Developments</summary></details>
<details><summary>5 Credits and Acknowledgements</summary></details>

[Insert images of responsive designs]

## 1 Introduction
This project is the natural progression of my first project *'Searchlight Promotions'*. For my first project I asked a fellow metal head, who runs a music promotion company in and for the Norwich rock and metal scene, if I could design him a website for my project, as he did not have one. After completing and submitting the project he asked me to maintain it going forward as he absolutely loved it. This ultimately meant that I had retained my first customer, and for the conclusion of this course, it is timely that the website is upgraded as the business has developed, my skills have progressed and as a true work-experience piece of practical evidence.

Project 1 can be found here in this *Github* repository (as it was submitted for P1): https://github.com/AxdeKlerk/Searchlight-Promotions, and here as the current working website: www.searchlightpromotions.co.uk. 

What is evident here is that the website has already had various upgrades, notable the inclusion of the link to the *ROXOFF* page using the logo in the navbar, shown here in the mobile view:

![roxoff logo shown in mobile view navbar](DOCS/images/nav-mobile.jpg)

### 1.1 The Aim, Purpose and Goal of the Site

The primary aim of the website has always been to *"create a presence beyond the scope of social media to attract rock and metal fans, as well as emerging [..] rock and metal [artists], to current events happening in Norwich"*(Project 1). 

The website’s purpose is to highlight upcoming events and increase ticket sales for each gig by reaching rock and metal fans who may not follow social media. Additionally, it should clearly communicate the company’s promotional services to attract unsigned rock and metal artists interested in partnering for promotion within Norwich.

The goal of the upgrade is to bring the project to the same level of development and success that Searchlight Promotions has achieved and advance it further by introducing a dedicated online store for merchandise and establishing a proprietary ticketing system for events, eliminating the need for an external booking and payment system via a 3rd party website.

### 1.2 Target Audience

The target audience is niche and focuses only on the rock and metal musicians and fans. It is specifically aimed at an aging demographic of rock and metal fans who don’t rely on social media for gig information in Norwich, the new rise in younger rock and metal fans who are looking to support up-and-coming artists locally, emerging (and unsigned) rock and metal artists looking for promotion in Norwich, other music promoters who may want to collaborate, as well as music journalists wanting to cover gigs.

[add merch and ticket sales]

## 2. Planning and Development

### 2.1 Project Statement and ERD

This project involves developing a web application focused on promoting and managing rock and metal music **events** held at a **single fixed venue**. The website allows **users** to either **log in** or browse as **guests**. Logged in users have the the ability to browse upcoming events, **search for merchandise and/or tickets**, add them to a **basket** and **purchase** event tickets and merch.

Each event offers **tickets for sale**, which users can select and add to their **basket** alongside any **merchandise**. The store offers official **products** such as shirts, hoodies, and accessories, which can be **filtered by product description**. Users can then proceed to **checkout**, where they provide payment securely via **Stripe**.

Users will also be able to view and **track the status of their orders**,  
receive **email confirmations** for purchases, and search for **artists and bands** to discover more music.
    

### 2.1.1 Identified Entities (Key Nouns):

-   **User** (covers both registered and guest users)
-   **Event**
-   **Ticket**
-   **Artist/Band**
-   **Product** (Merch)
-   **Order**
-   **OrderStatus**
-   **Payment**
-   **Venue** (fixed, but modelled for potential reuse)
    

### 2.1.2 Key Relationships:

-   A **User** can place multiple **Orders**
-   Each **Order** can include multiple **Products** and **Tickets** 
-   Each **Ticket** is linked to one **Event**  
-   An **Event** features one or more **Artists / Bands** and belongs to one **Venue**
-   A **Product** may be associated with a single **Order**
-   Each **Order** is linked to one **Payment** and one **OrderStatus**
-   All **Events** occur at the event **Venue**
    
This structured statement sets a clear foundation for building an ERD and a relational database that supports both **ticketing** and **e-commerce features** within a unified system. 

### 2.1.3 ERD (Entity Relationship Diagram)

![erd](DOCS/images/erd_v2.jpg)

### 2.2 Wireframes
After completing the first draft of the ERD I draw it out visually as a low fidelity-wireframe for desktops in *Balsamic*, as shown here:

![low-fidelity desktop wireframe](DOCS/images/wireframe-desktop.jpg)

 Once I was happy with what it looked like I converted it into a low-fidelity wireframe for mobiles, as shown here also in *Balsamic*:

![low-fidelity mobile website](DOCS/images/wireframe-mobile.jpg)

Having completed the above I went on to create a high-fidelity wireframe in *Figma*, focusing only on the desk top as everything would be responsive and feature as the low-fidelity wireframe for mobiles depicts above. All 3 versions focus on the functionality of the navbar. Meaning that all 3 were drawn around the navbar and plotted out as progressions. 

The high-fidelity wireframe show below helps to fully visualise the various screens and how they would look as a finished project. I decided to use some of the styling from my P3 for the tilting merch to create a more visually appealing view of the merch. This came about after doing some research on other websites (mainly rock and metal bands that I know and two festival sites that I go to each year) as to how they displayed their merch on their dedicated pages. 

The findings were mixed, however, most of the websites seemed to display their merch as an after thought that didn't follow the styling of the rest of their websites. The three stand-out websites, that did follow their overall styling, were *[Blacklakes](https://www.blacklakes.com/merch)*, *[South of Salem](https://www.southofsalem.com/)* and *[Slipknot](https://slipknotmerch.com/)*.

Slipknot's merch page stood out amoungst the rest and the decidion was made that, this project's website would follow Slipknot's style of layout, but make it different to anything else that could be found, by including the tilt styling.

![high-fidelity desktop wireframe](DOCS/images/hf-wireframe-desktop.jpg)

### 2.3 User Journeys

Having completed the wireframes, user journeys were plotted out as imagined the user would journey ould be through the website. First, the  current user journey was plotted out, from the *[Searchlight Promotions](www.searchlightpromotions.co.uk)* website, as shown here:

![current user journey](DOCS/images/current-user-journey.jpg)

What stood out were the 'dead ends' (depicted in red) that navigate the user away from the website with the user having to return to the website by clicking back on the website tab. This blocks the user from an easy transition back to the website and considered 'bad' UI/UX.

This was pointed out to the client as a pitfall to the UX and stated that by upgrading the site to manage its own ticket sales we would create a seamless experience for the user, that kept them on the website for further browsing in the hope that it would encourage further sales and interest.

Below is the new user journey as first imagined. The items in red are still 3rd party websites for payment and email confirmations for logging in, however, with the introduction of a 'thank you' page the user would be returned to the website for further browsing after payment. After the email confirmation, the user will be redirected back to the website automatically.

![imagined new user journey](DOCS/images/proposed-user-journey.jpg)

### 2.4 Agile Methodology

This project was developed using Agile methodologies to ensure a user-focused, iterative, and flexible development process. Key Agile principles were applied throughout.

Having plotted the new user journey and user stories, 'Epics' were extracted form the user journey into the categories that follow. Each 'Epic' represents an App in the *Django* project design. Under each 'Epic', user stories were created using the "As a **user** I want to **action** so that I can **benefit**" statement to ensure a user story driven development and that all development decisions were tied directly to user needs. From each user story actionable tasks were created representing the acceptance criteria for each user story. 

The project was created in *[Github](https://github.com/users/AxdeKlerk/projects/7)*.

#### 2.4.1 Epics

Each epic was added to the Project Board using labels as can be seen here:

![project board](DOCS/images/project-board-v2.jpg)

From the collapsable Core Epic, for example, the below details a descrption of the covered features, with the first 3 user stories below, and the tasks listed below the user stories:

![core epic](DOCS/images/core-epic.jpg)

The below shows the Site Indentification User Story as well as its corresponding Tasks List, as an example:

![site identification user story](DOCS/images/user-site-identification.jpg)

The above is a representation of the Kaban board and all its components. As the project developed more user stories and tasks were created. Throughout the design of the website this project baord was referenced to keep the scope of the project realistic and on track. For convenience the project board can be found here: ![project board](DOCS/images/project-board.jpg)

Below details all the Epic headings with their user story headings: 

#### 2.4.1.1 Core Epic

- Site Identification  

- Navigation  

- Search  

- Contact Form  

- Footer  

- Base Template  

#### 2.4.1.2 Products Epic  

- Event Listings  

- Event Detail Page  

- Merch Listings  

- Merch Detail Page  

- Ticket Availability Tracking  

- Roxoff Page & Event Tickets  

### 2.4.1.3 Basket Epic  

- Add to Basket  

- View Basket  

- Update Basket  

- Remove from Basket  

- Basket Totals  

### 2.4.1.4 User Epic  

- Sign Up  

- Log In  

- Password Reset  

- Log Out  

- Profile  

- Email Confirmations (Backlog – Not MVP)  

### 2.4.1.5 Checkout & Payments Epic  

- Checkout Page  

- Square Payments Integration  

- Order Confirmation Page  

- Order History in Profile  

### 2.4.1.6 DevOps Epic  

- Deployment  

- 400 Error Page  

- 500 Error Page  

### 2.4.2 User stories (following the same order as above)

- As a **user** I want to **land on the website and immediately recognise that it is for a rock and metal music promotion company** so that I **know I am in the right place**.  

- As a **user** I want to **be able to navigate between Home, About, Event, Merch, Contact Form and Basket** so that I can **reach any section quickly**. 

- As a **user,** I want to **be able to search for artists, merch and venues** so that I can **navigate quickly to my selected choice**.  

- As a **user**, I want to **contact the promotions company** so that **my query reaches the right place**.  .  

- As a **user**, I want to **see a basic footer with copyright information** so that I can **know where the end of the page is by the consistent copyright protection displayed beneath**.  

- As a **developer**, I want a **reusable base.html template** so that **all pages share the same layout, styling, and design consistency**.  

- As a **user**, I want to **view all upcoming events** so that I **can decide which ones to attend**.  

- As a **user**, I want to **view available merchandise** so that I can **browse and choose items to buy**.  

- As a **user**, I want to **view details of a merch item** so that I can **decide whether to purchase it**. 

- As an **event organiser**, I want ticket sales to **update availability** so that **users cannot purchase more tickets than exist**.   

- As a **user**, I want to **access the Roxoff page** so that I can **easily view and purchase tickets for upcoming events promoted under the Roxoff brand**.   

- As a **user**, I want to **add event tickets or merchandise to my basket** so that I can** purchase them later**.  

- As a **user**, I want to **view my basket** so that I can **see the items I intend to purchase**.  

- As a **user**, I want to **update the quantity of basket items** so that I can **adjust my order before checkout**.    

- As a **user**, I want to **delete items from my basket** so that I **don’t purchase items I no longer want**.    

- As a **user**, I want to **see my basket total** so that I **know the total cost before checkout**.  .  

- As a **new user**, I want to **create an account** so that I can **log in, purchase tickets/merch, and track my orders**.    

- As a **registered user**, I want to **log in** so that I can **access my account and complete purchases**.   

- As a **registered user**, I want to **reset my password if I forget it** so that I can **regain access to my account**.   

- As a **logged in user**, I want to **log out** so that **my account is secure when I leave the site**.    

- As a **logged in user**, I want to **view my profile** so that I can **track my order history**.  

- As a **registered user**, I want to **receive email confirmations** so that I can **verify my account and trust the platform**.  

- As a **logged in user**, I want to **proceed to a checkout page** so that I can **review my order and complete my purchase**.   

- As a **logged in user**, I want to **pay securely with Square** so that I can **complete my order with confidence**.   

- As a **logged in user**, I want to see **an order confirmation page after payment** so that I **know my purchase was successful**.    

- As a **logged in user**, I want to **view my past orders in my profile** so that I **can track what I’ve purchased**.  

- As a **developer**, I want to **deploy the application to Heroku** so that **users can access the live site**.   

- As a **user**, I want to **see a friendly 400 error page when I make a bad request** so that I **am not shown a confusing error message**.    

- As a **user**, I want **to see a friendly 500 error page when something goes wrong** so that I **understand the site is temporarily unavailable.** 


## Credits and Acknowledgements

### Credits

Below are the list of resources that I used to complete this project along with aknowledgements for the people who have supportedme and helped me test my ideas.

- Short Pixel for image compressions
- The following resources were used to help with the development of the website:
- [Adobe Express](https://new.express.adobe.com/?xProduct=&xProductLocation=&locale=en-US) for the logo creation
- [Balsamic](https://balsamiq.com/) for the wireframes
- [BootStrap](https://simple.wikipedia.org/wiki/Bootstrap_(front-end_framework)) - used for the layout and styling of the website
- [Bootstrap Docs](https://getbootstrap.com/) for reference to all Bootstrap syntax
- [Chat-GPT](https://chatgpt.com/) - An AI tool used for understanding where things went wrong, how to fix code and generally used for deeper understanding of software development and the principles and languages used for coding
- [coolors.co](https://coolors.co/) for the colour palette
- [CSS](https://en.wikipedia.org/wiki/CSS) - used for main content styling
- [Django](https://simple.wikipedia.org/wiki/Django_(web_framework)) - used for the backend of the website
- [draw.io](https://app.diagrams.net/) for the ERD
- [Google Fonts](https://fonts.google.com/) - for typology
- [Google Images](https://images.google.co.uk/) - for the band and venue logos
- [HTML](https://en.wikipedia.org/wiki/HTML) - used to build main site content
- [JavaScript](https://simple.wikipedia.org/wiki/JavaScript) - used for all interactivity within the website
- [JSHint](https://jshint.com/) for Javascript validation
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) - for the performance and accessibility testing
- [MSWord](https://www.microsoft.com/en-us/microsoft-365/word) - used for grammar and spelling checking
- [Perplexity](https://www.perplexity.ai/) - An AI tool used for general queries and learning
- [Python](https://simple.wikipedia.org/wiki/Python_(programming_language)) - used for the backend of the website
- [Responsive Viewer](https://responsiveviewer.org/)- used for responsive screen testing
- [Short Pixel](https://shortpixel.com/) - for image compressions
- [Slack Edit](https://stackedit.io/) - for markdown references
- [Slack Overflow](https://stackoverflow.com/questions) - for general queries
- [W3schools](https://www.w3schools.com/) a constant source of reference for all html, CSS, JavaScript, BootStrap and Django explanations
- [W3C Markup Validation Service](https://validator.w3.org/) for the html validation
- [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) for the CSS validation
