from .models import TourPackage


def booking_packages(request):

    packages = TourPackage.objects.all().order_by("name")

    return {
        "booking_packages": packages
    }