from django.contrib import admin
from .models import Login, Medicine,Customer,Sale

# --------------------------------------
# Register your models with the Admin site
# --------------------------------------

admin.site.register(Login)
admin.site.register(Medicine)
admin.site.register(Customer)
admin.site.register(Sale)
