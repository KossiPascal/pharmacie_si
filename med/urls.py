from django.conf.urls import url
from . import views
from django.urls import path

from ih_pharmacie.views import home

urlpatterns = [
    path('', home, name="home"),

    path('cameg/', views.DrugServedData, name='cameg'),
    path('cameg/create/', views.CamegDataCreateUpdateDelete, name='cameg_create'),
    path('cameg/update/<str:id>/', views.CamegDataCreateUpdateDelete, name='cameg_update'),
    path('cameg/delete/<str:delete>/',views.CamegDataCreateUpdateDelete, name='cameg_delete'),

    path('patient/', views.DrugServedData, name='patient'),
    path('patient/create/', views.PatientDataCreateUpdateDelete, name='patient_create'),
    path('patient/update/<str:id>/', views.PatientDataCreateUpdateDelete, name='patient_update'),
    path('patient/delete/<str:delete>/',views.PatientDataCreateUpdateDelete, name='patient_delete'),
 
    path('ih/', views.DrugServedData, name='ih'),
    path('ih/create/', views.IhDataCreateUpdateDelete, name='ih_create'),
    path('ih/update/<str:id>/', views.IhDataCreateUpdateDelete, name='ih_update'),
    path('ih/delete/<str:delete>/', views.IhDataCreateUpdateDelete, name='ih_delete'),

    path('stock/', views.DrugServedData, name='stock'),
    path('stock/create/', views.StockDataCreateUpdateDelete, name='stock_create'),
    path('stock/update/<str:id>/', views.StockDataCreateUpdateDelete, name='stock_update'),
    path('stock/delete/<str:delete>/', views.StockDataCreateUpdateDelete, name='stock_delete'),

    path('drug/stock_adjustment/', views.DrugServedData, name='stock_adjustment'),
    path('drug/stock_adjustment/create/', views.StockAdjustmentDataCreateUpdateDelete, name='stock_adjustment_create'),
    path('drug/stock_adjustment/update/<str:id>/', views.StockAdjustmentDataCreateUpdateDelete, name='stock_adjustment_update'),
    path('drug/stock_adjustment/delete/<str:delete>/', views.StockAdjustmentDataCreateUpdateDelete, name='stock_adjustment_delete'),

    path('drug/drugs_list/', views.DrugDataCreateUpdateDelete, name='drug'),
    path('drug/drugs_list/create/', views.DrugDataCreateUpdateDelete, name='drug_create'),
    path('drug/drugs_list/update/<int:id>/', views.DrugDataCreateUpdateDelete, name='drug_update'),
    path('drug/drugs_list/delete/<int:delete>/', views.DrugDataCreateUpdateDelete, name='drug_delete'),

    path('drug/drug_supplier/', views.DrugSupplierDataCreateUpdateDelete, name='drug_supplier'),
    path('drug/drug_supplier/create/', views.DrugSupplierDataCreateUpdateDelete,name='drug_supplier_create'),
    path('drug/drug_supplier/update/<int:id>/',views.DrugSupplierDataCreateUpdateDelete, name='drug_supplier_update'),
    path('drug/drug_supplier/delete/<int:delete>/',views.DrugSupplierDataCreateUpdateDelete, name='drug_supplier_delete'),

    path('drug/category/', views.CategoryDataCreateUpdateDelete, name='category'),
    path('drug/category/create/', views.CategoryDataCreateUpdateDelete, name='category_create'),
    path('drug/category/update/<int:id>/', views.CategoryDataCreateUpdateDelete, name='category_update'),
    path('drug/category/delete/<int:delete>/', views.CategoryDataCreateUpdateDelete, name='category_delete'),

    path('drug/year/', views.YearDataCreateUpdateDelete, name='year'),
    path('drug/year/create/', views.YearDataCreateUpdateDelete, name='year_create'),
    path('drug/year/update/<int:id>/', views.YearDataCreateUpdateDelete, name='year_update'),
    path('drug/year/delete/<int:delete>/', views.YearDataCreateUpdateDelete, name='year_delete'),

    path('drug/month/', views.MonthDataCreateUpdateDelete, name='month'),
    path('drug/month/create/', views.MonthDataCreateUpdateDelete, name='month_create'),
    path('drug/month/update/<int:id>/', views.MonthDataCreateUpdateDelete, name='month_update'),
    path('drug/month/delete/<int:delete>/', views.MonthDataCreateUpdateDelete, name='month_delete'),

    path('drug/district/', views.DistrictDataCreateUpdateDelete, name='district'),
    path('drug/district/create/', views.DistrictDataCreateUpdateDelete, name='district_create'),
    path('drug/district/update/<int:id>/',views.DistrictDataCreateUpdateDelete, name='district_update'),
    path('drug/district/delete/<int:delete>/',views.DistrictDataCreateUpdateDelete, name='district_delete'),

    path('drug/site/', views.SiteDataCreateUpdateDelete, name='site'),
    path('drug/site/create/', views.SiteDataCreateUpdateDelete, name='site_create'),
    path('drug/site/update/<int:id>/',views.SiteDataCreateUpdateDelete, name='site_update'),
    path('drug/site/delete/<int:delete>/',views.SiteDataCreateUpdateDelete, name='site_delete'),

    path('drug/translation/', views.TranslationDataCreateUpdateDelete, name='translation'),
    path('drug/translation/create/', views.TranslationDataCreateUpdateDelete, name='translation_create'),
    path('drug/translation/update/<int:id>/', views.TranslationDataCreateUpdateDelete, name='translation_update'),
    path('drug/translation/delete/<int:delete>/', views.TranslationDataCreateUpdateDelete, name='translation_delete'),

    path('drug/language/', views.LanguageUpdate, name='language'),
    path('dashborad/general/', views.Dash, name='dash'),
    path('dashborad/served/', views.ServedEtat, name='dashS'),
]

