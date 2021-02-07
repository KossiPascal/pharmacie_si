from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
 
from PIL import Image
import os

class District(models.Model):
    district = models.CharField(max_length=100)
    def __str__(self):
        return self.district

class Site(models.Model):
    site = models.CharField(max_length=100)
    district = models.ForeignKey(District, related_name='SiteDistrict', on_delete=models.DO_NOTHING, blank=True, null=True)
    def __str__(self):
        return self.site

class Year(models.Model):
    year = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.year)
  
class Month(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)
    month = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.month
 
class Category(models.Model):
    category = models.CharField(max_length=100)
    def __str__(self):
        return self.category

class DrugSupplier(models.Model):
    drug_supplier = models.CharField(max_length=100)
    def __str__(self):
        return self.drug_supplier

class Drug(models.Model):
    drug = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='DrugCategory', on_delete=models.DO_NOTHING, null=True, blank=True)
    expiry_date =  models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    cameg_available_quantity = models.PositiveIntegerField(null=True, blank=True, default=0, editable=False)
    ih_available_quantity = models.PositiveIntegerField(null=True, blank=True, default=0, editable=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.drug
 
class CamegDrugServed(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, max_length=255)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    drug = models.ForeignKey(Drug, related_name='CamegServedDrug', on_delete=models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey(District, related_name='CamegServedDistrict', on_delete=models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(Site, related_name='CamegServedSite', on_delete=models.DO_NOTHING, blank=True, null=True) 
    quantity_ordered = models.IntegerField(null=True, blank=True, default=0)
    quantity_served = models.IntegerField(null=True, blank=True, default=0)
    unit_price = models.IntegerField(null=True, blank=True, default=0)
    total_amount = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    created_by = models.ForeignKey(User, related_name='CamegServedCreatedBy', on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='CamegServedUpdatedBy', on_delete=models.DO_NOTHING, blank=True, null=True)

class IhDrugServed(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, max_length=255)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    drug = models.ForeignKey(Drug, related_name='IhServedDrug', on_delete=models.DO_NOTHING, blank=True, null=True)
    district = models.ForeignKey(District, related_name='IhServedDistrict', on_delete=models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(Site, related_name='IhServedSite', on_delete=models.DO_NOTHING, blank=True, null=True) 
    quantity_ordered = models.IntegerField(null=True, blank=True, default=0)
    quantity_served = models.IntegerField(null=True, blank=True, default=0)
    unit_price = models.IntegerField(null=True, blank=True, default=0)
    total_amount = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    created_by = models.ForeignKey(User, related_name='IhServedCreatedBy', on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='IhServedUpdatedBy', on_delete=models.DO_NOTHING, blank=True, null=True)

class PatientDrugServed(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, max_length=255)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    drug = models.ForeignKey(Drug, related_name='PatientServedDrug', on_delete=models.DO_NOTHING, blank=True, null=True)
    quantity_source = models.CharField(max_length=100)
    patient_fullname = models.CharField(max_length=100, blank=True, null=True)
    quantity_served = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    created_by = models.ForeignKey(User, related_name='PatientServedCreatedBy', on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='PatientServedUpdateBy', on_delete=models.DO_NOTHING, blank=True, null=True)
 
class DrugStock(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, max_length=255)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    drug = models.ForeignKey(Drug, related_name='Drug_served', on_delete=models.DO_NOTHING, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True, default=0)
    stock_quantity = models.IntegerField(null=True, blank=True, default=0)
    drug_supplier = models.ForeignKey(DrugSupplier, related_name='DrugStock_suppier', on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    created_by = models.ForeignKey(User, related_name='StockCreatedBy', on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='StockUpdateBy', on_delete=models.DO_NOTHING, blank=True, null=True)
 
class DrugStockAdjustment(models.Model):
    id = models.CharField(primary_key=True, auto_created=False, max_length=255)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    drug = models.ForeignKey(Drug, related_name='DrugServed', on_delete=models.DO_NOTHING, blank=True, null=True)
    stock_adjustment_quantity = models.IntegerField(null=True, blank=True, default=0)
    drug_source = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    created_by = models.ForeignKey(User, related_name='StockAdjustmentCreated_by', on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_by = models.ForeignKey(User, related_name='StockAdjustmentUpdated_by', on_delete=models.DO_NOTHING, blank=True, null=True)

class Etats(models.Model):
    n = models.IntegerField(null=True, blank=True)
    drug = models.ForeignKey(Drug, related_name='DrugEtat', on_delete=models.DO_NOTHING, blank=True, null=True)
    cameg_stock = models.IntegerField(null=True, blank=True)
    # new_cameg_stock = models.IntegerField(null=True, blank=True)
    ih_stock = models.IntegerField(null=True, blank=True)
    # new_ih_stock = models.IntegerField(null=True, blank=True)
    cameg_served = models.IntegerField(null=True, blank=True)
    ih_served = models.IntegerField(null=True, blank=True)
    patient_cameg_served = models.IntegerField(null=True, blank=True)
    patient_ih_served = models.IntegerField(null=True, blank=True)
    cameg_stock_remaining = models.IntegerField(null=True, blank=True)
    ih_stock_remaining = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    situation = models.CharField(max_length=100)
    amount = models.BooleanField(default=False)
    total_amount = models.BooleanField(default=False)
    single_amount = models.BooleanField(default=False)

class ServedEtats(models.Model):
    n = models.IntegerField(null=True, blank=True)
    drug = models.ForeignKey(Drug, related_name='DrugServedEtat', on_delete=models.DO_NOTHING, blank=True, null=True)
    jan = models.IntegerField(null=True, blank=True)
    fev = models.IntegerField(null=True, blank=True)
    mar = models.IntegerField(null=True, blank=True)
    avr = models.IntegerField(null=True, blank=True)
    mai = models.IntegerField(null=True, blank=True)
    jun = models.IntegerField(null=True, blank=True)
    jul = models.IntegerField(null=True, blank=True)
    aou = models.IntegerField(null=True, blank=True)
    sep = models.IntegerField(null=True, blank=True)
    ocb = models.IntegerField(null=True, blank=True)
    nov = models.IntegerField(null=True, blank=True)
    dec = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    amount = models.BooleanField(default=False)
 
class VariousParameters(models.Model):
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    district = models.ForeignKey(District, related_name='DashDistrict', on_delete=models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey(Site, related_name='DashSite', on_delete=models.DO_NOTHING, blank=True, null=True)
    dash_type = models.CharField(max_length=100, null=True, blank=True)
    data_source = models.CharField(max_length=100, null=True, blank=True)
    user_language = models.ForeignKey(User, related_name='UserLanguage', on_delete=models.DO_NOTHING, blank=True, null=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    # big_total_amount = models.IntegerField(null=True, blank=True)
    # cameg_total_amount_served = models.IntegerField(null=True, blank=True)
    # cameg_total_amount_served_now = models.IntegerField(null=True, blank=True)
    # ih_total_amount_served = models.IntegerField(null=True, blank=True)
    # ih_total_amount_served_now = models.IntegerField(null=True, blank=True)

class Translation(models.Model):
    acronym_fr = models.CharField(max_length=100, null=True, blank=True,verbose_name="Translationacronym_fr")
    acronym_en = models.CharField(max_length=100, null=True, blank=True,verbose_name="Translationacronym_en")
    trans_fr = models.TextField(null=True, blank=True,verbose_name="TranslationEnFrancais")
    trans_en = models.TextField(null=True, blank=True,verbose_name="TranslationEnAnglais")

# def update_drug_stock(sender, instance, **kwargs):
#     drug = instance.drug
#     ds = int(instance.drug_supplier.id)
#     if ds == 1:
#         drug.cameg_available_quantity += int(instance.stock_quantity)
#     else:
#         drug.ih_available_quantity += int(instance.stock_quantity)
#     drug.save()


# def update_remaining_drug_stock(sender, instance, **kwargs):
#     drug = instance.drug
#     if sender == CamegDrugServed:
#         drug.cameg_available_quantity -= int(instance.quantity_served)
#     elif sender == IhDrugServed:
#         drug.ih_available_quantity -= int(instance.quantity_served)
#     elif sender == PatientDrugServed:
#         drug.ih_available_quantity -= int(instance.quantity_served)
#     else:
#         pass
#     drug.save()
 
# pre_save.connect(update_drug_stock, sender=DrugStock)
# pre_save.connect(update_remaining_drug_stock, sender=CamegDrugServed)
# pre_save.connect(update_remaining_drug_stock, sender=IhDrugServed)
# pre_save.connect(update_remaining_drug_stock, sender=PatientDrugServed)
