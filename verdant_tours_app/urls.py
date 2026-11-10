from django.urls import path

from . import views


urlpatterns = [

    # ============================================================
    # ADMIN AUTHENTICATION
    # ============================================================

    path(
        "login/",
        views.admin_login,
        name="admin_login",
    ),

    path(
        "admin-logout/",
        views.admin_logout,
        name="admin_logout",
    ),


    # ============================================================
    # ADMIN DASHBOARD
    # ============================================================

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard",
    ),


    # ============================================================
    # BLOGS
    # ============================================================

    path(
        "dashboard/blogs/",
        views.admin_blog_list,
        name="admin_blog_list",
    ),

    path(
        "dashboard/blogs/create/",
        views.blog_create,
        name="blog_create",
    ),

    path(
        "dashboard/blogs/<int:pk>/edit/",
        views.blog_update,
        name="blog_update",
    ),

    path(
        "dashboard/blogs/<int:pk>/delete/",
        views.blog_delete,
        name="blog_delete",
    ),


    # ============================================================
    # TOUR PACKAGES
    # ============================================================

    path(
        "dashboard/packages/",
        views.admin_package_list,
        name="admin_package_list",
    ),

    path(
        "dashboard/packages/create/",
        views.package_create,
        name="package_create",
    ),

    path(
        "dashboard/packages/<int:pk>/edit/",
        views.package_update,
        name="package_update",
    ),

    path(
        "dashboard/packages/<int:pk>/delete/",
        views.package_delete,
        name="package_delete",
    ),


    # ============================================================
    # DESTINATIONS
    # ============================================================

    path(
        "dashboard/destinations/",
        views.admin_destination_list,
        name="admin_destination_list",
    ),

    path(
        "dashboard/destinations/create/",
        views.destination_create,
        name="destination_create",
    ),

    path(
        "dashboard/destinations/<int:pk>/edit/",
        views.destination_update,
        name="destination_update",
    ),

    path(
        "dashboard/destinations/<int:pk>/delete/",
        views.destination_delete,
        name="destination_delete",
    ),


    # ============================================================
    # GALLERY
    # ============================================================

    path(
        "dashboard/gallery/",
        views.gallery_images,
        name="list_image",
    ),

    path(
        "dashboard/gallery/add/",
        views.add_image,
        name="add_image",
    ),

    path(
        "dashboard/gallery/<int:image_id>/delete/",
        views.delete_image,
        name="delete_image",
    ),


    # ============================================================
    # GALLERY CATEGORIES
    # ============================================================

    path(
        "dashboard/categories/",
        views.category_list,
        name="category_list",
    ),

    path(
        "dashboard/categories/add/",
        views.add_category,
        name="add_category",
    ),

    path(
        "dashboard/categories/<int:pk>/edit/",
        views.update_category,
        name="update_category",
    ),

    path(
        "dashboard/categories/<int:pk>/delete/",
        views.delete_category,
        name="delete_category",
    ),


    # ============================================================
    # TESTIMONIALS
    # ============================================================

    path(
        "dashboard/testimonials/",
        views.testimonial_list,
        name="review_list",
    ),

    path(
        "dashboard/testimonials/add/",
        views.testimonial_create,
        name="testimonial_create",
    ),

    path(
        "dashboard/testimonials/<int:pk>/edit/",
        views.testimonial_update,
        name="testimonial_update",
    ),

    path(
        "dashboard/testimonials/<int:pk>/delete/",
        views.testimonial_delete,
        name="testimonial_delete",
    ),


    # ============================================================
    # CONTACT MESSAGES
    # ============================================================

    path(
        "dashboard/contacts/",
        views.view_contacts,
        name="view_contacts",
    ),

    path(
        "dashboard/contacts/<int:pk>/delete/",
        views.delete_contact,
        name="delete_contact",
    ),


    # ============================================================
    # BOOKING ENQUIRIES
    # ============================================================

    path(
        "dashboard/enquiries/",
        views.admin_enquiry_list,
        name="admin_enquiry_list",
    ),

    path(
        "dashboard/enquiries/<int:pk>/delete/",
        views.admin_enquiry_delete,
        name="admin_enquiry_delete",
    ),




     # ============================================================
    # FRONTEND
    # ============================================================

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "about/",
        views.about,
        name="about",
    ),

    path(
        "contact/",
        views.contact,
        name="contact",
    ),

    path(
        "packages/",
        views.packages,
        name="packages",
    ),
    path("packages/<slug:slug>/", views.package_details, name="package_details"),

    path(
        "destination/",
        views.destination,
        name="destination",
    ),
    path("destination/<slug:slug>/", views.destination_details, name="destination_details"),

    path(
        "blogs/",
        views.blogs,
        name="blogs",
    ),
   
path(
    "blog/<slug:slug>/",
    views.blog_detail,
    name="blog_detail",
),
path('gallery/', views.gallery, name='gallery'),

path(
    "terms-and-conditions/",
    views.terms_conditions,
    name="terms_conditions",
),

path(
    "booking-enquiry/",
    views.booking_enquiry,
    name="booking_enquiry",
),


]