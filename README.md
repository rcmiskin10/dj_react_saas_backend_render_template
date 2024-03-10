# SaaS Boilerplate - Backend Setup

##### Create project folder and git clone into it.

1. `cd Desktop`
2. `mkdir saas-boilerplate` or whatever you would like to call it
3. `cd saas-boilerplate`
4. `mkdir backend`
5. `cd backend`
6. `git clone https://github.com/rcmiskin10/dj_react_backend_render_template.git .`
7. `pip install virtualenv`
8. `python3.8 -m venv env`
9. `source env/bin/activate`
10. `pip install -r requirements.txt`
11. Create a file called `.env` and place the environmental variables from below:
```
STRIPE_API_TEST_PK=<STRIPE_API_TEST_PK>
STRIPE_API_TEST_SK=<STRIPE_API_TEST_SK>
STRIPE_LIVE_MODE=False
PROD_BACKEND_URL=<PROD_BACKEND_URL>
PROD_FRONTEND_URL=<PROD_FRONTEND_URL>
BACKEND_URL=http://127.0.0.1
FRONTEND_URL=http://localhost:3000
DEBUG=True
DEV_EMAIL_HOST_USER=<DEV_EMAIL_HOST_USER>
DEV_EMAIL_HOST_PASSWORD=<DEV_EMAIL_HOST_PASSWORD>
POSTMARK_SERVER_TOKEN=<POSTMARK_SERVER_TOKEN>
DEFAULT_FROM_EMAIL=<DEFAULT_FROM_EMAIL>
```
12. Now you need to set up Stripe.
    1. If you do not have a stripe account register a free one here: https://dashboard.stripe.com/register. If you do have a stripe account login here: https://dashboard.stripe.com/login.
    2. Once account is set up or you're logged in, turn on `Test Mode` (Toggle button in top right corner of dashboard) it should bring you to: https://dashboard.stripe.com/test/payments
    3. Go to https://dashboard.stripe.com/test/apikeys
       1. Grab your `Publishable key` token and set the environmental variable `STRIPE_API_TEST_PK` in your `.env` file created from step `11` above.
       2. Next grab your `Secret key` token and set the environmental variable `STRIPE_API_TEST_SK` in your `.env` file created from step `11` above.
    4. Next go to https://dashboard.stripe.com/test/products?active=true to add your products, i.e. subscription tiers
       1. Add as many tiers as you want i.e.
          1. Free w/ a description and price: $0
          2. Pro w/ a description and price: say $10
          3. Make sure both are Recurring and Monthly or however you would like to set up your subscriptions.
13. Now set up your local Postgres database
    1.  Download Postgres v13 (or latest version) from https://www.postgresql.org/download/macosx/ and follow instructions.
    2. Create database, i.e. `postgres`
    3. Make sure your database default setting in `settings.py` is `default="postgresql://postgres:postgres@localhost/postgres"`, if your database name is `postgres`.
    4. Now run `python manage.py migrate`
       1. you should see all migrations applied
    5. Then `python manage.py createsuperuser` so you can log into Django Admin
       1. Enter email and password.
    6. Now run `python manage.py runserver` and head to http://127.0.0.1:8000/admin/login/ and login with email and password created in `13.5.1`
    7. you should be able to get to the Django Admin now and see all of the tables.
14.  Now go to Products admin here: http://127.0.0.1:8000/admin/payments/product/
    1. Add First product from Stripe above in step `12.4.1`
       1. Enter the Product Name
       2. Tier
       3. Stripe product id
          1. You can find Stripe Product Id in https://dashboard.stripe.com/test/products?active=true and click on product and in the URL you will see an ID with prefix `prod_xxxxxxxx` and letters and numbers as the unique id.
          2. Do the same for all products
    2. Now go to http://127.0.0.1:8000/admin/payments/productprice/
       1. Add the price for each product from Stripe here: http://127.0.0.1:8000/admin/payments/productprice/add/
          1. Select `Product` that you added to Django in `14.1`
          2. Add the Price from what you entered in on Stripe
          3. Add the interval, i.e. Monthly
          4. Add the stripe price id
             1. Go to https://dashboard.stripe.com/test/products?active=true
             2. Select the Product and scroll down to `Pricing` and look under `API ID` and copy id with prefix and numbers/letters like `price_xxxxxxxxx` and pase into stripe price id on django admin.
          5. Do for all products
    3. Now you can add descriptions of the tiers here: http://127.0.0.1:8000/admin/payments/productdescriptionitem/add/
       1. Add as many description list items for each product
15.  Now we can add the rest of our environmental variables in `.env`
    1. Set `DEV_EMAIL_HOST_USER` to your `gmail` for DEV testing
    2. Set your `DEV_EMAIL_HOST_PASSWORD` to the password set up in your gmail account from above. You need to create an App Password in: https://myaccount.google.com/security
       1. Make sure 2-Step Authentication is enabled.
       2. Then go to https://myaccount.google.com/apppasswords and create a new app and a new password will be created.
    3. Now Emails will be sent through gmail smtp in DEV
16. We will set up prod environmental variables later.
17. Next up is setting up the landing page data.
    1. Note here you can add whatever copy, images, icons, you would like through the Django admin
       1. Go to http://127.0.0.1:8000/admin/landingpage/landingpage/add/
          1. Add the hero section copy and image
          2. Add the features of your SaaS
             1. the `Feature mui icon name:` can be selected from https://mui.com/material-ui/material-icons/?query i.e. find `Add` and get the name of the icon from the end of the import in the modal `import AddIcon from '@mui/icons-material/Add';` i.e. `Add`
          3. You can add as many features as you like and `Order` them however you like by apply `1,2,3...` to each feature. i.e. 1 will be first in line.
          4. Do the same for how it works, Secondary hero, and Social Media Links
18. Next we will deploy to render.com.
    1. First set up Cloudinary by going to the [cloudinary](https://cloudinary.com/) website through this link and create a free cloudinary account. After your account has been created go to the dashboard page and copy the cloud name, api key and api secret.
    2. Follow tutorial here: https://docs.render.com/deploy-django#use-renderyaml-for-deploys
       1. The `backend/render.yaml` already exists in the saas boilerplate. You can change all the names to fit whatever you like, but our boilerplate named everything `backend`
       2. In the Render Dashboard, go to the [Blueprints](https://dashboard.render.com/blueprints) page and click New Blueprint Instance.
       3. Make sure to first create a repository to hold your `backend/` folder on github.
          1. Now you can select the repository that contains your blueprint and click Connect.
          2. Give your blueprint project a name and click Apply.
       4. Now add the Production Environmental Variables by clicking the `backend` app and going to `Environment`
          1. Add you Stripe `STRIPE_API_TEST_PK` found in your local .env file or if you are ready to use live Stripe data use the Production PK found in stripe dashboard.
          2. Same with the `STRIPE_API_TEST_SK`
          3. `STRIPE_LIVE_MODE=False`
          4. `BACKEND_URL` will be the url that your backend render app is pointing to: something similar to this `backend-xxxxonrender.com`
          5. For your media files first set up Cloudinary account by going to the [cloudinary](https://cloudinary.com/) website through this link and create a free cloudinary account. After your account has been created go to the dashboard page and copy the cloud name, api key and api secret.
             1. Add the cloud name to `CLOUDINARY_CLOUD_NAME`
             2. Add the api key to `CLOUDINARY_API_KEY`
             3. Add the api secret to `CLOUDINARY_API_SECRET`
          6. For your emails create a postmark account here https://postmarkapp.com/. Follow instructions here: https://postmarkapp.com/support/article/1008-what-are-the-account-and-server-api-tokens to find your Server API Token and set it to `POSTMARK_SERVER_TOKEN`
             1. Set `DEFAULT_FROM_EMAIL` to your email with postmark.
          7. After you deploy the frontend app below come back to setting `FRONTEND_URL`
       5. Finally run `python manage.py createsuperuser` in the Render shell in the settings of the backend app so that you can create an admin account.
          1. To see your backend admin page, go to `<YOUR_APP_URL>/admin` to login.
