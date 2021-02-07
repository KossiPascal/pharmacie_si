from django import forms
from django.db.models.enums import IntegerChoices
from .models import CamegDrugServed, District, DrugStockAdjustment, IhDrugServed, DrugStock, DrugSupplier, Drug, Category, Month, PatientDrugServed, Site, Translation, Year
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea, CheckboxInput, Select
from django.forms.widgets import DateInput, SelectDateWidget, Input


DRUG_SOURCE = (
    ("ih", "ih"),
    ("cameg", "cameg"),
)

class CamegDrugServedForm(forms.ModelForm):
    class Meta:
        model = CamegDrugServed
        fields = ('date','drug','district','quantity_ordered','quantity_served','unit_price','total_amount')
        widgets = {
            'district': Select(attrs={'id': "district", 'onChange': "ActiveAjax(this.id, this.value)", 'class': "form-control", 'required': "required"}),
            # 'site': Select(attrs={'id': "site", 'class': "form-control", 'required': "required"}),
            'date': DateInput(attrs={'id': 'date', 'type': 'date', 'required': "required", 'class': "form-control"}),
            'drug': Select(attrs={'id': "drug", 'class': "form-control", 'required': "required"}),
            'quantity_ordered': Input(attrs={'id': "quantity_ordered", 'type': 'number', 'class': "form-control", 'style': "font-size:x-large", 'placeholder': "-------", 'step': "any"}),
            'quantity_served': Input(attrs={'id': "quantity_served", 'type': 'number', 'onchange': "Montant()", 'class': "form-control", 'style': "font-size:x-large",'placeholder':"-------",'step': "any", 'required': "required"}),
            'unit_price': Input(attrs={'id': "unit_price", 'type': 'number', 'onchange': "Montant()", 'class': "form-control", 'style': "font-size:x-large",'placeholder':"-------",'step': "any", 'required': "required"}),
            'total_amount': Input(attrs={'id': "total_amount", 'type': 'number', 'style': "display:none; background-color: black!important; color:white; font-size:x-large",'placeholder':"-------",'step':"any", 'class': "form-control"}),
        
        }
 
class IhDrugServedForm(forms.ModelForm):
    class Meta:
        model = IhDrugServed
        fields = ('date','drug','district','quantity_ordered','quantity_served','unit_price','total_amount')
        widgets = {
            'district': Select(attrs={'id': "district", 'onChange': "ActiveAjax(this.id, this.value)", 'class': "form-control", 'required': "required"}),
            # 'site': Select(attrs={'id': "site", 'class': "form-control", 'required': "required"}),
            'date': DateInput(attrs={'id': 'date', 'type': 'date', 'required': "required", 'class': "form-control"}),
            'drug': Select(attrs={'id': "drug", 'class': "form-control", 'required': "required"}),
            'quantity_ordered': Input(attrs={'id': "quantity_ordered", 'type': 'number', 'class': "form-control", 'style': "font-size:x-large", 'placeholder': "-------", 'step': "any"}),
            'quantity_served': Input(attrs={'id': "quantity_served", 'type': 'number', 'onchange': "Montant()", 'class': "form-control", 'style': "font-size:x-large",'placeholder':"-------",'step': "any", 'required': "required"}),
            'unit_price': Input(attrs={'id': "unit_price", 'type': 'number', 'onchange': "Montant()", 'class': "form-control", 'style': "font-size:x-large",'placeholder':"-------",'step': "any", 'required': "required"}),
            'total_amount': Input(attrs={'id': "total_amount", 'type': 'number', 'style': "display:none; background-color: black!important; color:white; font-size:x-large",'placeholder':"-------",'step':"any", 'class': "form-control"}),
        }

class PatientDrugServedForm(forms.ModelForm):
    class Meta:
        model = PatientDrugServed
        fields = ('date','drug','patient_fullname','quantity_served','quantity_source')
        widgets = {
            'date': DateInput(attrs={'id': 'date', 'type': 'date', 'required': "required", 'class': "form-control"}),
            'drug': Select(attrs={'id': "drug", 'class': "form-control", 'required': "required"}),
            'quantity_source': Select(choices=DRUG_SOURCE, attrs={'id': "quantity_source", 'class': "form-control", 'style': "font-size:large", 'required': "required"}),
            'patient_fullname': Input(attrs={'id': "patient_fullname", 'type': 'text', 'class': "form-control", 'style': "font-size:x-large", 'required': "required"}),
            'quantity_served': Input(attrs={'id': "quantity_served", 'type': 'number', 'class': "form-control", 'style': "font-size:x-large", 'required': "required"}),
        }


class DrugStockForm(forms.ModelForm):
    class Meta:
        model = DrugStock
        fields = ('date','drug','stock_quantity','drug_supplier')
        widgets = {
            'date': DateInput(attrs={'id': 'date', 'type': 'date', 'required': "required", 'class': "form-control"}),
            'drug': Select(attrs={'id': "drug", 'class': "form-control", 'required': "required"}),
            'stock_quantity': Input(attrs={'id': "stock_quantity", 'type': 'number', 'class': "form-control", 'style': "font-size:x-large"}),
            'drug_supplier': Select(attrs={'id': "drug_supplier", 'class': "form-control", 'required': "required"}),
        }

class DrugStockAdjustmentForm(forms.ModelForm):
    class Meta:
        model = DrugStockAdjustment
        fields = ('date', 'drug', 'stock_adjustment_quantity', 'drug_source')
        widgets = {
            'date': DateInput(attrs={'id': 'date', 'type': 'date', 'required': "required", 'class': "form-control"}),
            'drug': Select(attrs={'id': "drug", 'class': "form-control", 'required': "required"}),
            'stock_adjustment_quantity': Input(attrs={'id': "stock_adjustment_quantity", 'type': 'number', 'class': "form-control", 'style': "font-size:x-large"}),
            'drug_source': Select(choices=DRUG_SOURCE, attrs={'id': "drug_source", 'class': "form-control", 'required': "required"}),
        }

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ('drug', 'category', 'expiry_date', 'is_available')
        widgets = {
            'drug': Input(attrs={'id': "drug", 'type': 'text', 'class': "form-control", 'required': "required"}),
            'category': Select(attrs={'id': "category", 'class': "form-control", 'required': "required"}),
            'expiry_date': DateInput(attrs={'id': 'expiry_date', 'type': 'date', 'class': "form-control"}),
            'is_available': CheckboxInput(attrs={'id': 'is_available', 'style':'zoom:2.5'}),
        }

class DrugSupplierForm(forms.ModelForm):
    class Meta:
        model = DrugSupplier
        fields = ('drug_supplier',)
        widgets = {
            'drug_supplier': Input(attrs={'id': "drug_supplier", 'type': 'text', 'class': "form-control", 'required': "required"}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)
        widgets = {
            'category': Input(attrs={'id': "category", 'type': 'text', 'class': "form-control", 'required': "required"}),
        }

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ('year',)
        widgets = {
            'year': Input(attrs={'id': "year", 'type': 'number', 'class': "form-control", 'required': "required"}),
        }

class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ('id','month',)
        widgets = {
            'id': Input(attrs={'type': 'number', 'class': "form-control", 'required': "required"}),
            'month': Input(attrs={'id': "month", 'type': 'text', 'class': "form-control", 'required': "required"}),
        }

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ('district',)
        widgets = {
            'district': Input(attrs={'id': "district", 'type': 'text', 'class': "form-control", 'required': "required"}),
        }

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('site', 'district')
        widgets = {
            'site': Input(attrs={'type': 'text', 'class': "form-control", 'required': "required"}),
            'district': Select(attrs={'class': "form-control", 'required': "required"}),
        }

class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ('acronym_fr', 'acronym_en', 'trans_fr', 'trans_en',)
        widgets = {
            'acronym_fr': Input(attrs={'id': "acronym_fr", 'type': 'text', 'class': "form-control"}),
            'acronym_en': Input(attrs={'id': "acronym_en", 'type': 'text', 'class': "form-control"}),
            'trans_fr': Input(attrs={'id': "trans_fr", 'type': 'text', 'class': "form-control", 'required': "required"}),
            'trans_en': Input(attrs={'id': "trans_en", 'type': 'text', 'class': "form-control", 'required': "required"}),
        }
