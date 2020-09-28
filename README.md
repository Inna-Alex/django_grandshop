# Online store Grand Shop
Grand Shop is a typical online store, written in Python (Django, Vue.js). It is written as a separate application (app) with the possible connection of additional applications.
### Includes the following typical modules:
1. **Registration** of a new user (custom registration — by user email).
2. **Authorization** of the registered user (login, logout) — custom authorization.
3. **Logging system** of all sql-queries to the database.
4. The **Manufacturers** module - represents the manufacturers that you can select in the products.
5. Module **Categories** - represents product categories.
6. Module **Products** - represents specific products that the user can select in his order.
In the Products module, export to a file in CSV format is implemented using custom templates and custom filters for templates (located in the templatetags directory)
For the modules Manufacturers, Categories, Products, a standard CRUD is implemented using generic view classes. The main methods of generic view classes have also been redefined, and validation has been implemented.
7. The **Basket** module is a list of products that the user purchased (clicked the Buy button on the product). On the page, you can place an order using the Checkout button. After that, the order is added to the list of orders and automatically switches to the Created status.
8. Module **Orders**
9. **Rest API** using DRF

The following functionality is also available:
1. The Your Orders page - displays a list of orders of an authorized user. Not available if the user is not logged in. The Create order button is also available here. When choosing a product to add to the order, it is enough to fill in the Product and Quantity fields, The price is calculated automatically (AJAX is used to display the calculated product price depending on the quantity on the user's screen).
2. The order detail page displays information about the order (status, customer) as well as all ordered products. On the same page, the buttons Edit, Delete are available for the selected products (custom forms are used), as well as the button Add a new product to the order. Here you can also delete an order by clicking the corresponding button, followed by confirmation of deleting the order (the order and all associated products will be deleted - custom functionality).
3. Using **DRF**, an API (CRUD) is written for the Categories and Manufacturers modules. Both APIView and serializers were used.
4. Auto tests of 2 types have been written for the project:
   1. unit tests using **django’s TestCase**;
   2. unit tests using **pytest**
Also, using the coverage module, the percentage of code coverage by tests was calculated. The report can be viewed at grandshop \ htmlcov \ index.html.

To run the project, you need Django preinstalled, as well as the following modules:
1. Crispy forms: pip install django-crispy-forms
2. Current user: pip install django-currentuser
3. DRF: pip install djangorestframework
4. To export to csv (no template): pip install django-csv-export-view
5. To rerun coverage: pip install coverage
6. To install pytest: pip install pytest
                      pip install pytest-django.
7. To install widget-tweaks: pip install django_widget-tweaks
                      
Commands are given for installing modules via pip.

The project has a lot to improve and add, and the project is not ready for production, but it implements all the basic Django concepts (User model, CRUD, request logging, custom templates and template filters, custom migration, AJAX, unit tests) and some others.
