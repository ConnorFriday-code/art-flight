# User story testing

| **User Story**                                                                                         | **How Tested**                                          | **Outcome**                                 |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------- |
| As an artist, I want to sign up quickly so I can start posting my work                                 | Created an account using email registration             | Successfully created account and logged in  |
| As an artist, I want to create and manage my posts so that I can showcase services to customers        | Added new artist posts, then edited and updated details | Posts saved correctly and updates reflected |
| As an artist, I want to remove posts that are no longer available so my profile stays accurate         | Used the delete option on existing posts                | Posts deleted successfully                  |
| As a customer, I want to browse artist services by category or search so I can find what I want easily | Searched using tags and keywords                        | Relevant posts displayed correctly          |
| As a customer, I want to add services to a basket so I can decide what to buy                          | Added commissions to basket                             | Items correctly appeared in the basket      |
| As a customer, I want to adjust quantities or options in my basket so my order matches my needs        | Edited quantity and commission details in basket        | Changes saved and reflected in the basket   |
| As a customer, I want to remove items from my basket if I change my mind                               | Deleted items from basket                               | Items removed successfully                  |
| As a customer, I want to review my past purchases so I can keep track of orders                        | Checked past orders page                                | Orders displayed correctly                  |


# Manual Testing

**Feature**         | **Testing method**      | **Result**                                            |
| ------------------ | ------------------- | ----------------------- |
Create accounts        |Attempting to create an account using an email| Works as  intended   |
Create artist posts         |   Using the create a service button/form in the user profile   |   Works as  intended |
Read commissions/artist posts         |  Find and reading an artist post using the tags or search bar    |   Both work as  intended |
Read basket list         |  Adding an item to my basket then checking if it is being displayed properly |   Works as  intended |
Read past orders         |  Finding the past orders page in the user profile section to find past orders    |   Works as  intended |
Update artist posts        |    Using the edit a service button/form in the user profile section |   Works as  intended |
Update basket quantity     |    Using the edit button/form on an item already in my basket to change the quantity   |   Works as  intended |
Update basket item options |    Using the edit button on an item already in my basket to change my commision option   |   Works as  intended |
Delete own artist posts    |    Using the delete a service button in the user profile section |   Works as  intended |
Delete basket list items   |    Adding an commission request to my basket then attempting to remove it with the delete button   |   Works as  intended |

# Lighthouse

## Welcome Page

![Welcome page lighthouse report](readme_assets/lighthouse/welcome-page-lh.png)

## Artist page

![Artist page lighthouse report](readme_assets/lighthouse/artist-page-lh.png)

## Artist post

![Artist post page lighthouse report](readme_assets/lighthouse/artist-post-lh.png)

# Basket and checkout

## Bag page

![Bag page lighthouse report](readme_assets/lighthouse/bag-lh.png)

## Checkout page

UNABLE

Lighthouse is kicked back to artist page when attempting to test it (an error message is visable in the page screenshot that lighthouse takes).

![Checkout page failed lighthouse report](readme_assets/lighthouse/checkout-lh.png)

# Profile

## My account page

![My account page lighthouse report](readme_assets/lighthouse/my-account-page-lh.png)

## Create artist post page

![Create artist page lighthouse report](readme_assets/lighthouse/create-artist-lh.png)

## Past orders page

![Past order page lighthouse report](readme_assets/lighthouse/past-orders-lh.png)

## Receipt page

![Receipt page lighthouse reports](readme_assets/lighthouse/receipt-page-lh.png)

# HTML, CSS, & Python validation

All the minor errors are related to the table drop down in the nav bar. I do not have time to fix/remake the navigation bar, as such I will simply have to mark down the minor errors.

| **Page**                 | **HTML Validator**                      | **CSS Validator**                          | **Python Validator**      |
| ------------------------ | -------------------------------         | ------------------------------------------ | ------------------------- |
| Home page                | Minor HTML warnings          | Valid CSS, 24 vendor extension warnings                                  | Passed                    |
| Signup page              | Minor HTML warnings, Django related warnings                 | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Login page               | Minor HTML warnings, Django related warnings                 | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Profile page             | Minor HTML warnings                     | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Create a service page    | Minor HTML warnings                     | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Edit a service page      | Minor HTML warnings                           | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Past orders list page    | Minor HTML warnings                                | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Receipt page             | Minor HTML warnings                     | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Artist posts page        | Minor HTML warnings                                | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Artist post details page | Minor HTML warnings                     | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Basket page              | Minor HTML warnings                               | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Edit an item page        | Minor HTML warnings                           | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
| Checkout page            | Minor HTML warnings , several Stripe warnings  | Valid CSS, 24 vendor extension warnings                                   | Passed                    |
