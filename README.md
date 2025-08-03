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

[2.4.1.1 User Epic](#2411-user-epic)

[2.4.1.2 Core Epic](#2412-core-epic)

[2.4.1.3 Products Epic](#2413-products-epic)

[2.4.1.3.1 Merch (subset)](#24131-merch-subset)

[2.4.1.3.2 Events (subset)](#24132-events-subset)

[2.4.1.4 Basket Epic](#2414-basket-epic)

[2.4.1.4.1 Order Status (subset)](#24141-order-status-subset)

[2.4.1.4.2 Payment Method (subset)](#24142-payment-method-subset)

[2.4.2 Kaban Board](#242-kaban-board)
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

![ERD](DOCS/images/erd.jpg)

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

Once I had completed my wireframes I decided to plot out how I imagined the user would journey through the website. First I plotted the current user journey as it  stands for the current *[Searchlight Promotions](www.searchlightpromotions.co.uk)* website, as shown here:

![current user journey](DOCS/images/current-user-journey.jpg)

What stands out is the 'dead ends' (depicted in red) that navigate the user away from the website with the user having to return to the website by clicking back on the website tab. 

I pointed this out to the client as a pitfall to the UX and stated that by upgrading the site to manage its own ticket sales we would create a seamless experience for the user, that kept them on the website for further browsing in the hope that it would encourage further sales and interest.

Below is the new user journey as first imagined. The items in red are still 3rd party websites for payment and email confirmations for logging in, however, with the introduction of a 'thank you' page the user would be returned to the website for further browsing after payment, and after the email confirmations the user will be redirected back to the website.

![imagined new user journey](DOCS/images/proposed-user-journey.jpg)

### 2.4 Agile Methodology

This project was developed using Agile methodologies to ensure a user-focused, iterative, and flexible development process. Key Agile principles were applied throughout.

Having plotted the new user journey, 'Epics' were extracted form the user journey into the categories that follow, as shown below. Each 'Epic' represents an App in the *Django* project design. Under each 'Epic', user stories were created using the "As a **user** I want to **action** so that I can **benefit**" statement to ensure a user story driven development and that all development decisions were tied directly to user needs. They are are as follows:

#### 2.4.1 Epics

##### 2.4.1.1 User Epic


##### 2.4.1.2 Core Epic


##### 2.4.1.3 Products Epic

###### 2.4.1.3.1 Merch (subset)

###### 2.4.1.3.2 Events (subset)


##### 2.4.1.4 Basket Epic

###### 2.4.1.4.1 Order Status (subset)

###### 2.4.1.4.2 Payment Method (subset)

#### 2.4.2 Kaban Board