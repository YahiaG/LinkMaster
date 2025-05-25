from django.db import models

# Create your models here.

class Link(models.Model):
    site_no_b_end = models.CharField(max_length=200)
    site_no_a_end = models.CharField(max_length=200)
    site_name_b_end = models.CharField(max_length=200)
    site_name_a_end = models.CharField(max_length=200)
    link_supplier = models.CharField(max_length=200)
    capacity = models.CharField(max_length=200)
    transmission_type = models.CharField(max_length=200)
    path_length_km = models.CharField(max_length=200)
    antenna_size_b_end = models.CharField(max_length=200)
    antenna_size_a_end = models.CharField(max_length=200)
    azimuth_b_end = models.CharField(max_length=200)
    azimuth_a_end = models.CharField(max_length=200)
    antenna_height_b_end = models.CharField(max_length=200)
    antenna_height_a_end = models.CharField(max_length=200)
    band = models.CharField(max_length=200)
    tx_freq_b_end = models.CharField(max_length=200)
    tx_freq_a_end = models.CharField(max_length=200)
    polarization = models.CharField(max_length=200)
    mmu_id_b_end = models.CharField(max_length=200)
    mmu_id_a_end = models.CharField(max_length=200)
    hub_name = models.CharField(max_length=200)
    link_name = models.CharField(max_length=200)
    comments_and_grooming = models.TextField()
    tx_power_dbm = models.CharField(max_length=200)
    received_power_b_end_mdb = models.CharField(max_length=200)
    conc = models.CharField(max_length=200)
    activity = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.site_no_b_end}<>{self.site_no_a_end} - {self.transmission_type}"
