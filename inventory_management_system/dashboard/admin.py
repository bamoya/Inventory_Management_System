from django.contrib import admin
from .models import Category,Supplier,Product,Stock,PurchaseOrder,PurchaseOrderItem,Sale,SaleItem,Customer
# Register your models here.
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name','category','quantity',   )
#     list_filter = ('category',)


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Stock)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(Sale)
admin.site.register(SaleItem)
