from django.db.models.signals import pre_save, post_save,pre_delete,post_delete
from django.dispatch import receiver
from accounts.models import Product,Orders

# print("in signals")
@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance,**kwargs):
    print(f"About to save product: {instance.name}")

@receiver(post_save, sender=Product)
def mymodel_post_save(sender, instance, created,**kwargs):
    if instance.quantity == 0:
        instance.quantity = 10
        instance.save()
    # if created:
    #     print("product updated")
    #     print(instance)

@receiver(pre_delete, sender=Orders)
def product_pre_delete(sender, instance, **kwargs):
    print(f"About to delete product: {instance}")


@receiver(post_delete, sender=Orders)
def product_post_delete(sender, instance, **kwargs):
    quantity = instance.quantity
    # user = instance.user
    pk = instance.product.id
    product = Product.objects.get(pk=pk)
    product.quantity += quantity
    product.save()
    print(f"Product deleted: {instance},{product},{quantity}")