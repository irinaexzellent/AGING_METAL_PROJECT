from django.contrib import admin

from .models import *


class TestTemperatureAdmin(admin.ModelAdmin):
    list_display = ('value_temperature', )
    search_fields = ('value_temperature',)
    list_filter = ('value_temperature',)

models = [
    TestReportMetal,
    ChemicalElement,
    Design,
    DocumentType,
    Organization,
    ProductCategory,
    Property,
    RegulatoryDocument,
    SteelGrade,
    Assortment,
    QualityDocument,
    Heat,
    Semiproduct,
    Product,
    TensileTest]

admin.site.register(models)
admin.site.register(TestTemperature, TestTemperatureAdmin)