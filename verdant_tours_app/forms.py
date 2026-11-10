from django import forms

from .models import (
    Blog,
    BookingEnquiry,
    Category,
    ContactMessage,
    Destination,
    GalleryImage,
    Testimonial,
    TourPackage,
)


# ============================================================
# TOUR PACKAGE FORM
# ============================================================

class TourPackageForm(forms.ModelForm):

    class Meta:
        model = TourPackage

        fields = [
            "name",
            "description",
            "main_image",
            "duration",
            "price_from",
            "package_type",
            "highlights",
            "inclusions",
        ]


# ============================================================
# DESTINATION FORM
# ============================================================

class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destination

        fields = [
            "name",
            "description",
            "image",
            "location",
            "destination_type",
        ]


# ============================================================
# BLOG FORM
# ============================================================

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog

        fields = [
            "title",
            "description",
            "image",
        ]


# ============================================================
# CATEGORY FORM
# ============================================================

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category

        fields = [
            "name",
        ]


# ============================================================
# GALLERY IMAGE FORM
# ============================================================

class GalleryImageForm(forms.ModelForm):

    class Meta:
        model = GalleryImage

        fields = [
            "category",
            "title",
            "image",
        ]


# ============================================================
# TESTIMONIAL FORM
# ============================================================

class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial

        fields = [
            "name",
            "image",
            "review",
        ]


# ============================================================
# BOOKING ENQUIRY FORM
# ============================================================

class BookingEnquiryForm(forms.ModelForm):

    class Meta:
        model = BookingEnquiry

        fields = [
            "name",
            "phone",
            "package",
            "start_date",
            "end_date",
            "adults",
            "children",
            "message",
        ]

    def clean(self):

        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:

            raise forms.ValidationError(
                "End date cannot be before the start date."
            )

        return cleaned_data


# ============================================================
# CONTACT MESSAGE FORM
# The "I'm not a robot" check is done by Google reCAPTCHA in
# views.py (verify_recaptcha), so there is no robot field here.
# ============================================================

class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",
            "message",
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name", "").strip()

        if len(first_name) < 2:
            raise forms.ValidationError(
                "Please enter a valid first name."
            )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name", "").strip()

        if len(last_name) < 1:
            raise forms.ValidationError(
                "Please enter your last name."
            )

        return last_name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        # Allow common phone characters
        cleaned_phone = (
            phone.replace("+", "")
                 .replace(" ", "")
                 .replace("-", "")
                 .replace("(", "")
                 .replace(")", "")
        )

        if not cleaned_phone.isdigit():
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        if len(cleaned_phone) < 7 or len(cleaned_phone) > 15:
            raise forms.ValidationError(
                "Please enter a valid phone number."
            )

        return phone

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            return email.strip().lower()

        return email