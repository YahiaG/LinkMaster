from django.contrib import admin
from .models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('link_name', 'site_name_b_end', 'site_name_a_end', 'link_supplier', 'capacity', 'band', 'activity')
    list_filter = ('link_supplier', 'band', 'activity', 'transmission_type')
    search_fields = ('link_name', 'site_name_b_end', 'site_name_a_end', 'site_no_b_end', 'site_no_a_end')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('link_name', 'link_supplier', 'capacity', 'transmission_type', 'band', 'activity')
        }),
        ('Site B End', {
            'fields': ('site_no_b_end', 'site_name_b_end', 'antenna_size_b_end', 'azimuth_b_end', 
                      'antenna_height_b_end', 'tx_freq_b_end', 'mmu_id_b_end')
        }),
        ('Site A End', {
            'fields': ('site_no_a_end', 'site_name_a_end', 'antenna_size_a_end', 'azimuth_a_end', 
                      'antenna_height_a_end', 'tx_freq_a_end', 'mmu_id_a_end')
        }),
        ('Technical Details', {
            'fields': ('path_length_km', 'polarization', 'hub_name', 'tx_power_dbm', 
                      'received_power_b_end_mdb', 'conc')
        }),
        ('Additional Information', {
            'fields': ('comments_and_grooming', 'created_at')
        }),
    )
    ordering = ('-created_at',)
