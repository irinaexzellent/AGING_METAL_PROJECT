from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TestTemperature(models.Model):
    id_test_temperature = models.BigAutoField(primary_key=True)
    value_temperature = models.FloatField(unique=True)

    def __str__(self):
        return self.value_temperature

    class Meta:
        db_table = 'test_temperature'

class TestReportMetal(models.Model):
    id_test_report_metal = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    issue_date = models.DateField('Issue date')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'test_report_metal'

class ChemicalElement(models.Model):
    id_chemical_element = models.BigAutoField(primary_key=True)
    short_name = models.CharField(verbose_name='Short name', max_length=255, unique=True)
    full_name = models.CharField(verbose_name='Full name', max_length=255, unique=True)

    def __str__(self):
        return self.short_name

    class Meta:
        db_table = 'chemical_element'

class Design(models.Model):
    id_design = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'design'

class DocumentType(models.Model):
    id_document_type = models.BigAutoField(primary_key=True)
    full_name = models.CharField(verbose_name='Short name', max_length=255, unique=True)
    short_name = models.CharField(verbose_name='Full name', max_length=255, unique=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'document_type'

class Organization(models.Model):
    id_organization = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    description = models.CharField(verbose_name='Description', max_length=255)
    address = models.CharField(verbose_name='Address', max_length=255)
    email = models.CharField(verbose_name='Email', max_length=255)
    website = models.CharField(verbose_name='Website', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'

class ProductCategory(models.Model):
    id_product_category = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_category'

class Property(models.Model):
    id_property = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'property'

class RegulatoryDocument(models.Model):
    id_regulatory_document = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)
    code = models.CharField(verbose_name='Code', max_length=255)
    issue_date = models.DateField(verbose_name='Issue date')
    document_type_id = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE,
        related_name="%(class)s_document_type", blank=True, null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'regulatory_document'


class SteelGrade(models.Model):
    id_steel_grade = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Name', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'steel_grade'


class Assortment(models.Model):
    id_assortment = models.BigAutoField(primary_key=True)
    regulatory_document_id = models.ForeignKey(
        RegulatoryDocument, on_delete=models.CASCADE,
        related_name="%(class)s_regulatory_documents", blank=True, null=True
    )
    steel_grade_id = models.ForeignKey(
        SteelGrade, on_delete=models.CASCADE,
        related_name="%(class)s_steel_grades", blank=True, null=True
    )
    product_category_id = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE,
        related_name="%(class)s_product_categories", blank=True, null=True
    )
    assortment_parameter = models.CharField(max_length=255)

    class Meta:
        unique_together = (('regulatory_document_id', 'steel_grade_id', 'product_category_id', 'assortment_parameter'),)
        db_table = 'assortment'

class QualityDocument(models.Model):
    id_quality_document = models.BigAutoField(primary_key=True)
    name_certificate = models.CharField(verbose_name='Name', max_length=255, unique=True)
    issue_date = models.DateField(verbose_name='Issue date', auto_now_add=True)
    product_category_id = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE,
        related_name="%(class)s_product_categories", blank=True, null=True
    )
    design_id = models.ForeignKey(
        Design, on_delete=models.CASCADE,
        related_name="%(class)s_designs", blank=True, null=True
    )
    manufacturer_id = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name="%(class)s_organizations", blank=True, null=True
    )
    regulatory_document_id = models.ForeignKey(
        Organization, on_delete=models.CASCADE,
        related_name="%(class)s_regulatory_documents", blank=True, null=True
    )
    assortment_id = models.ForeignKey(
        Assortment, on_delete=models.CASCADE,
        related_name="%(class)s_assortments", blank=True, null=True
    )

    class Meta:
        db_table = 'quality_document'


class Heat(models.Model):
    quality_document_id = models.ForeignKey(
        QualityDocument, on_delete=models.CASCADE,
        related_name="%(class)s_quality_documents", blank=True
    )
    code = models.CharField(verbose_name='Code', max_length=255)

    class Meta:

        unique_together = (('quality_document_id', 'code'),)
        db_table = 'heat'

class Semiproduct(models.Model):
    heat_quality_document_id = models.ForeignKey(
        QualityDocument, on_delete=models.CASCADE,
        related_name="%(class)s_quality_documents", blank=True
    )
    heat_code = models.CharField(verbose_name='Code of heat', max_length=255)
    number = models.CharField(verbose_name='Number', max_length=255)
    nominal_diameter = models.FloatField(verbose_name='Nominal diameter', unique=True)

    class Meta:
        unique_together = (('heat_quality_document_id', 'heat_code', 'number'),)
        db_table = 'semiproduct'

class Product(models.Model):
    semiproduct_heat_quality_document_id = models.ForeignKey(
        QualityDocument, on_delete=models.CASCADE,
        related_name="%(class)s_quality_documents", blank=True
    )
    semiproduct_heat_code = models.CharField(verbose_name='Code of heat', max_length=255)
    semiproduct_number = models.CharField(verbose_name='Number of semiproduct', max_length=255)
    description = models.CharField(verbose_name='Description', max_length=255)

    class Meta:
        unique_together = (('semiproduct_heat_quality_document_id', 'semiproduct_heat_code', 'semiproduct_number'),)
        db_table = 'product'


class TensileTest(models.Model):
    product_semiproduct_heat_quality_document_id = models.ForeignKey(
        QualityDocument, on_delete=models.CASCADE,
        related_name="%(class)s_quality_documents", blank=True
    )
    product_semiproduct_heat_code = models.CharField(verbose_name='Code of heat', max_length=255)
    product_semiproduct_number = models.CharField(verbose_name='Number of semiproduct', max_length=255)
    product_number = models.CharField(verbose_name='Number of product', max_length=255)
    marking = models.CharField(verbose_name='Marking', max_length=255)
    test_temperature_id = models.ForeignKey(
        TestTemperature, on_delete=models.CASCADE,
        related_name="%(class)s_test_temperatures", blank=True, null=True
    )
    tensile_strength = models.FloatField(unique=True)
    yield_strength = models.FloatField(unique=True)
    elastic_modulus = models.FloatField(unique=True)
    elongation = models.FloatField(unique=True)
    reduction = models.FloatField(unique=True)
    regulatory_document_id = models.ForeignKey(
        TestTemperature, on_delete=models.CASCADE,
        related_name="%(class)s_regulatory_documents", blank=True, null=True
    )

    class Meta:
        unique_together = (('product_semiproduct_heat_code', 'product_semiproduct_number', 'product_number', 'marking'),)
        db_table = 'tensile_test'