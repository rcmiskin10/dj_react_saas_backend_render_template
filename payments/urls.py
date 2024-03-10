import payments.views as views
from django.urls import path

urlpatterns = [
    path(
        "update-subscription/",
        views.UpdateSubscription.as_view(),
        name="api_update_subscription",
    ),
    path(
        "add-payment-method/",
        views.AddPaymentMethod.as_view(),
        name="api_add_payment_method",
    ),
    path("retrieve-billing-info/", views.RetrieveBillingInfo.as_view()),
    path("retrieve-product-info/", views.RetrieveProductInfo.as_view()),
    path("retrieve-all-products/", views.RetrieveAllProducts.as_view()),
]
