import json

import os
import psycopg2
import queries
from django.shortcuts import render_to_response, HttpResponse, redirect
from django.template import RequestContext
from geonode.geoserver.helpers import *
from django.contrib.auth import get_user_model
from geonode.layers.models import Layer

current_folder = os.path.dirname(os.path.dirname(__file__))
datastors_file_path = os.path.join(current_folder, 'odk', 'datastore.json')
from geonode.tasks.update import geoserver_update_layers

GEONODE_WORKSPACE = 'geonode'
ODK_DATASTORE = 'odkgeonodeds'


def _create_odk_store():
    """
    Create a database store.
    """
    cat = gs_catalog
    dsname = ODK_DATASTORE
    db = get_db_settings()

    try:
        ds = cat.get_store(dsname)
    except FailedRequestError:
        ds = cat.create_datastore(dsname)
        ds.connection_parameters.update(
            host=db['HOST'],
            port=db['PORT'],
            database=db['NAME'],
            user=db['USER'],
            passwd=db['PASSWORD'],
            dbtype='postgis'
        )
        cat.save(ds)
        ds = cat.get_store(dsname)
    return ds

def create_geometry_view(table_name):
    view_name = 'GEONODE_%s_LAYER' % table_name
    db_connection = get_db_settings()
    try:
        conn = psycopg2.connect(
            "dbname=" + db_connection["NAME"] + " user=" + db_connection["USER"] + " host=" + db_connection[
                "HOST"] + " password=" + db_connection["PASSWORD"] + " port=" + db_connection["PORT"])
        query = queries.create_view % (view_name,table_name);
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return view_name
    except:
        print "Unable to connect to the database"
        return None

def _publish_layer(request, table_name):
    cat = gs_catalog
    layer_name = 'GEONODE_%s_LAYER' % table_name
    # data_store = cat.get_store('odkgeonodeds', 'geonode')
    data_store = _create_odk_store()
    try:
        layer = cat.get_resource(layer_name, store=ODK_DATASTORE)
        if layer is None:
            workspace = cat.get_workspace('geonode')
            geometry_view = create_geometry_view(table_name)
            if geometry_view is not None:
                layer = cat.publish_featuretype(name=geometry_view, store=data_store, native_crs="4326", srs="EPSG:4326")
                cat.save(layer)
    except FailedRequestError:
        print "Create Layer Error"
    owner = request.user
    """ Publish layer to GeoNode """
    geoserver_update_layers.delay(ignore_errors=False, owner=owner, workspace=GEONODE_WORKSPACE,store=ODK_DATASTORE, filter=layer_name)
    return layer_name

def get_db_settings():
    if not os.path.isfile(datastors_file_path):
        return {}
    with open(datastors_file_path) as data_file:
        data = json.load(data_file)
    return data


def save_db_settings(data):
    with open(datastors_file_path, 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()


def odk_tables_list(request):
    context = {'tables': []}
    tables = []
    if request.method == 'POST':
        layer_name = _publish_layer(request, request.POST['layer'])
        return HttpResponse(json.dumps({"success":True,"layer":layer_name}),content_type="application/json")
    else:
        db_connection = get_db_settings()
        try:
            conn = psycopg2.connect(
                "dbname=" + db_connection["NAME"] + " user=" + db_connection["USER"] + " host=" + db_connection[
                    "HOST"] + " password=" + db_connection["PASSWORD"] + " port=" + db_connection["PORT"])
            cur = conn.cursor()
            cur.execute("select table_name from information_schema.columns where column_name = 'LOCATION_LNG' AND table_name IN (select table_name from information_schema.tables WHERE table_type ='BASE TABLE')")
            odk_tables = cur.fetchall()
            for odk_table in odk_tables:
                if Layer.objects.filter(name='GEONODE_%s_LAYER' % odk_table[0]).count() > 0:
                    display_name = Layer.objects.get(name='GEONODE_%s_LAYER' % odk_table[0]).title_en
                    tables.append({"title":odk_table[0],"name":'%s:GEONODE_%s_LAYER' % (GEONODE_WORKSPACE,odk_table[0]),"display_name":display_name,"published":True})
                else:
                    tables.append({"title":odk_table[0],"name":'%s:GEONODE_%s_LAYER' % (GEONODE_WORKSPACE,odk_table[0]),"display_name":'',"published":False})
            cur.close()
            conn.close()
            context = {'tables': tables, 'odk_url': db_connection["ODK_URL"]}
        except:
            print "Unable to connect to the database"
    return render_to_response('odk/home.html', context, context_instance=RequestContext(request))


def odk_settings(request):
    context = {}
    if request.method == 'POST':
        db_settings = {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": request.POST['db_name'],
            "USER": request.POST.get('db_user'),
            "PASSWORD": request.POST.get('db_password'),
            "HOST": request.POST.get('db_host'),
            "PORT": request.POST.get('db_port'),
            "ODK_URL" :request.POST.get('odk_url')
        }
        save_db_settings(db_settings)
        context = db_settings
        return redirect('odk_list')
    else:
        context = get_db_settings()
    return render_to_response('odk/settings.html', context, context_instance=RequestContext(request))