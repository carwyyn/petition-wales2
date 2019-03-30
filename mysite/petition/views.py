from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import requests



# Create your views here.
def index (request):
    response  = requests.get('https://petition.parliament.uk/petitions/241584.json')
    petition_data = response.json()
    constituency_data = petition_data['data']['attributes']['signatures_by_constituency']
    constituency_df = pd.DataFrame(constituency_data)

    wales_response  = requests.get('https://martinjc.github.io/UK-GeoJSON/json/wal/topo_wpc.json')
    wales_data = wales_response.json()

    constituencies = []
    for constituency in wales_data['objects']['wpc']['geometries']:
        constituencies.append(constituency['properties']['PCON13NM'])

    df2 = constituency_df[constituency_df['name'].isin(constituencies)]

    sum1 = df2.sum(axis = 0, skipna = True)

    total=sum1.signature_count

    context = {
        'total_signatures': total
    }

    return render(request, 'petition/index.html', context)
