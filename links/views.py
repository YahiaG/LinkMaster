from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Link
import pandas as pd
import os, subprocess
from django.conf import settings
from django.db import transaction, OperationalError
import time
from django.http import JsonResponse
import json
from itertools import chain
import sqlite3
from django.db import connection
from django.db.models import Q
from pathlib import Path

def home(request):
    """View function for the home page"""
    return render(request, 'home.html')

# Global progress state
progress_state = {
    'progress': 0,
    'message': 'Not started',
    'status': 'idle'
}

def update_db(request):
    """
    View function to handle Excel file upload and update the database with Link records.
    Uses Django ORM with chunked processing for better performance.
    """
    global progress_state
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        try:
            # Check if processing is already in progress
            if progress_state['status'] == 'processing':
                return JsonResponse({'error': 'Processing already in progress'}, status=400)
                
            start_time = time.time()
            print("Starting process...")
            
            # Reset progress state
            progress_state.update({
                'progress': 0,
                'message': 'Starting...',
                'status': 'processing'
            })
            
            excel_file = request.FILES['excel_file']
            
            # Validate file type
            if not excel_file.name.lower().endswith(('.xlsx', '.xls')):
                raise ValueError("File must be an Excel file (.xlsx or .xls)")
            
            print(f"File validated: {time.time() - start_time:.2f} seconds")
            progress_state.update({
                'progress': 20,
                'message': 'Reading Excel file...'
            })
            
            # Define required columns
            required_columns = [
                'Site No (B End)', 'Site No (A End)', 'Site Name (B End)', 'Site Name (A End)',
                'Link Supplier', 'CAPACITY', 'Transmission Type', 'Path Length (Km)',
                'Antenna Size B End', 'Antenna Size A End', 'Azimuth (B End)', 'Azimuth (A End)',
                'Antenna Hight (B End)', 'Antenna Hight (A End)', 'BAND', 'Tx Freq (B End)',
                'Tx Freq (A End)', 'Polarization', 'MMU ID (B End)', 'MMU ID (A End)',
                'Hub_Name', 'Link Name', 'Comments and Grooming', 'Tx Power (dbm)',
                'Received Power (B End) (mdb)', 'Conc', 'Activity'
            ]
            
            field_mapping = {
                'Site No (B End)': 'site_no_b_end', 'Site No (A End)': 'site_no_a_end',
                'Site Name (B End)': 'site_name_b_end', 'Site Name (A End)': 'site_name_a_end',
                'Link Supplier': 'link_supplier', 'CAPACITY': 'capacity',
                'Transmission Type': 'transmission_type', 'Path Length (Km)': 'path_length_km',
                'Antenna Size B End': 'antenna_size_b_end', 'Antenna Size A End': 'antenna_size_a_end',
                'Azimuth (B End)': 'azimuth_b_end', 'Azimuth (A End)': 'azimuth_a_end',
                'Antenna Hight (B End)': 'antenna_height_b_end', 'Antenna Hight (A End)': 'antenna_height_a_end',
                'BAND': 'band', 'Tx Freq (B End)': 'tx_freq_b_end', 'Tx Freq (A End)': 'tx_freq_a_end',
                'Polarization': 'polarization', 'MMU ID (B End)': 'mmu_id_b_end',
                'MMU ID (A End)': 'mmu_id_a_end', 'Hub_Name': 'hub_name', 'Link Name': 'link_name',
                'Comments and Grooming': 'comments_and_grooming', 'Tx Power (dbm)': 'tx_power_dbm',
                'Received Power (B End) (mdb)': 'received_power_b_end_mdb', 'Conc': 'conc',
                'Activity': 'activity'
            }
            
            # Read Excel with optimized settings
            excel_start = time.time()
            df = pd.read_excel(
                excel_file,
                engine='openpyxl',
                dtype=str,
                na_filter=False,
                usecols=required_columns
            )
            print(f"Excel read time: {time.time() - excel_start:.2f} seconds")
            
            # Check for required columns
            progress_state.update({
                'progress': 40,
                'message': 'Validating columns...'
            })
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
            # Rename columns
            df = df.rename(columns=field_mapping)
            df = df[list(field_mapping.values())]
            
            # Clear existing records
            Link.objects.all().delete()
            
            # Process in chunks
            chunk_size = 10000
            total_rows = len(df)
            total_processed = 0  # Track total processed rows
            
            # Process chunks
            for chunk_start in range(0, total_rows, chunk_size):
                chunk_end = min(chunk_start + chunk_size, total_rows)
                chunk = df.iloc[chunk_start:chunk_end]
                
                # Prepare records for this chunk
                records = []
                for _, row in chunk.iterrows():
                    data = {
                        field: str(value) for field, value in row.items()
                    }
                    records.append(Link(**data))
                
                # Bulk create this chunk
                Link.objects.bulk_create(records)
                
                # Update progress
                chunk_size_processed = len(chunk)
                total_processed += chunk_size_processed
                
                # Calculate progress
                progress = min(100, int((total_processed / total_rows) * 100))
                progress = progress * 60 / 100 + 40  # Scale progress to 40-100 range
                
                # Update progress state
                progress_state.update({
                    'progress': progress,
                    'message': f'Processing records {total_processed}/{total_rows}...'
                })
                
                # Log progress (only once per chunk)
                print(f"Chunk {chunk_start}-{chunk_end}: Processed {chunk_size_processed} records. Total processed: {total_processed}/{total_rows}")
            
            total_time = time.time() - start_time
            print(f"Total processing time: {total_time:.2f} seconds")
            print(f"Number of records processed: {total_rows}")
            
            progress_state.update({
                'progress': 100,
                'message': f'Excel file processed successfully! {total_rows} records imported in {total_time:.2f} seconds.',
                'status': 'complete'
            })
            # Add a small delay to ensure frontend receives completion status
            time.sleep(2)
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            error_message = f'Error processing Excel file: {str(e)}'
            progress_state.update({
                'status': 'error',
                'message': error_message
            })
            return JsonResponse({'error': error_message}, status=500)
    
    return render(request, 'links/upload_excel.html')

def get_progress(request):
    """Endpoint to get the current progress"""
    return JsonResponse(progress_state)


def search_links(request):
    if request.method == 'POST':
        site_id = request.POST.get('site_no')
        b_links = Link.objects.filter(site_no_b_end__iexact=site_id)
        a_links = Link.objects.filter(site_no_a_end__iexact=site_id)
        links = list(chain(b_links, a_links)) 

        return render(request, 'view_links.html', {'links':links})
    return render(request, 'view_links.html')

def link_details(request, link_id):
    link = Link.objects.get(id=link_id)
    get_cascades(link.site_no_a_end)
    return render(request, 'link_details.html', {'link': link})

def get_cascades(site_id, visited=None):
    """
    Recursively get all cascaded sites for a given site_id.
    Returns a list of site IDs that are connected to the given site.
    """
    if visited is None:
        visited = set()
    
    if site_id in visited:
        return []
    
    visited.add(site_id)
    cascades = []
    
    # Get all active links where this site is either A-end or B-end
    links = Link.objects.filter(
        Q(site_no_a_end__iexact=site_id) & Q(activity__iexact='Active')
    )
    
    for link in links:
        # Get the other end of the link
        other_site = link.site_no_b_end 
        if other_site not in visited:
            cascades.append(other_site)
            # Recursively get cascades for the other site
            cascades.extend(get_cascades(other_site, visited))
    
    return list(set(cascades))

def get_site_tree(request):
    """
    View function to get the site hierarchy tree for a given site_id.
    Returns a JSON response with the site tree structure.
    """
    site_id = request.GET.get('site_id')
    if not site_id:
        return JsonResponse({'error': 'Site ID is required'}, status=400)
    
    try:
        # Get the main site's information
        main_site = Link.objects.filter(site_no_a_end__iexact=site_id, activity__iexact='Active').first()
        print(main_site)
        if not main_site:
            return JsonResponse({'error': 'Site not found or has no cascades'}, status=404)
        
        # Create the tree structure
        def build_tree(current_site_id, visited=None):
            if visited is None:
                visited = set()
            
            if current_site_id in visited:
                return None
            
            visited.add(current_site_id)
            
            # Get site information
            site_info = Link.objects.filter(
                Q(site_no_a_end__iexact=current_site_id) | Q(site_no_b_end__iexact=current_site_id)
            ).first()
            
            if not site_info:
                return None
            
            affected_sites = [current_site_id.upper()]
            
            # Get the site name
            site_name = (site_info.site_name_a_end if site_info.site_no_a_end == current_site_id 
                        else site_info.site_name_b_end)
            
            # Get connected sites
            links = Link.objects.filter( Q(site_no_a_end__iexact=current_site_id) & Q(activity__iexact='Active')  )
            
            children = []
            for link in links:
                other_site = link.site_no_b_end 
                if other_site not in visited:
                    child_tree = build_tree(other_site, visited)
                    if child_tree:
                        children.append(child_tree)
                        affected_sites.extend(child_tree['affected_sites'])

            return {
                'site_id': current_site_id,
                'site_name': site_name,
                'children': children,
                'affected_sites': affected_sites
            }
        BASE_DIR = Path(__file__).resolve().parent.parent

        tree = build_tree(site_id)
        with open(BASE_DIR/'PA_sites.csv', 'w') as f:
            f.write('Site, Include Logical\n')
            for site in tree['affected_sites']:
                f.write(site + ', Yes\n')

        # subprocess.Popen(r'explorer /select "{path2}"')
        # os.startfile(BASE_DIR)
        return JsonResponse(tree)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def connectivity_view(request):
    """View function for the connectivity page"""
    return render(request, 'links/connectivity.html')

def about(request):
    """View function for the about page"""
    return render(request, 'about.html')
