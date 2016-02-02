import os 
import pdb
from PIL import Image

'''
    TODO
    - Create Placemark.name, desc from file name/caption and folder?
'''

TAG = {34853: 'GPSInfo'}

def create_point(path): 
    img = Image.open(path)
    final_long = ''
    final_lat = ''
    try:
        if img:
            #print(path)
            exif_items = img._getexif()
            if exif_items:
                exif_data = {TAG[k]: v for k, v in exif_items.items() if k in TAG}
                if exif_data and 'GPSInfo' in exif_data:
                    exif = exif_data['GPSInfo']
                    # get lat
                    lat_deg = exif[2][0][0]/float(exif[2][0][1])
                    lat_min = exif[2][1][0]/float(exif[2][1][1])
                    lat_sec = exif[2][2][0]/float(exif[2][2][1])
                    lat_dec = (lat_min + lat_sec/60)/60
                    if str(exif[1]) == 'S':
                        lat_deg *= -1
                        lat_dec *= -1
                    final_lat = '%s' % (lat_deg + lat_dec)
                    # get long
                    long_deg = exif[4][0][0]/float(exif[4][0][1])
                    long_min = exif[4][1][0]/float(exif[4][1][1])
                    long_sec = exif[4][2][0]/float(exif[4][2][1])
                    long_dec = (long_min + long_sec/60)/60
                    if str(exif[3]) == 'W':
                        long_deg *= -1
                        long_dec *= -1
                    final_long = '%s' % (long_deg + long_dec)
    finally:
        return "<Point><coordinates>%s,%s,0</coordinates></Point>" % (final_long, final_lat)

    
def begin_file():
    text = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document>'
    start_folder = 'G:/Pictures/'
    start_folder = '/Users/matthewc/Pictures/'
    dirs_to_ignore = ['$RECYCLE.BIN', 'Aperture Library.aplibrary', 'Temp','.picasaoriginals']
    for root, dirs, files in os.walk(start_folder):
        for ignore in dirs_to_ignore:
            if ignore in dirs:
                dirs.remove(ignore)

        for folder in dirs:
            dir_path = os.path.join(root, folder)
            for folder_root, folder_dirs, folder_files in os.walk(dir_path):
                if '.picasaoriginals' in folder_dirs:  # TODO going through po?
                    folder_dirs.remove('.picasaoriginals')

                images = [i for i in folder_files if os.path.splitext(i)[1] in (
                        '.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG')]
                #pdb.set_trace()
                for image_file in images:
                    file_link = os.path.join(dir_path, image_file)
                    image_kml = '<Placemark>'
                    image_kml += '<name>%s - %s</name>' % (folder, os.path.splitext(image_file)[0])  # TODO
                    image_kml += '<description>%s</description>' % image_file  # TODO
                    image_kml += '%s' % create_point(file_link)
                    image_kml += '</Placemark>'
                    text += image_kml
    text += '</Document></kml>'
    with open("/Users/matthewc/Pictures/points.kml", "w") as text_file:
        text_file.write("%s" % text)
        
'''
    EXAMPLE KML 
    -- floating point values for longitude, latitude, and altitude (in that order)
    -- lat < 0 for S
    -- long < 0 for W

    <?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
    <Placemark>
      <name>New York City</name>
      <description>New York City</description>
      <Point>
        <coordinates>-74.006393,40.714172,0</coordinates>
      </Point>
    </Placemark>
    <Placemark>
        <name>Simple placemark</name>
        <description>Attached to the ground. Intelligently places itself at the
          height of the underlying terrain.</description>
        <Point>
          <coordinates>-122.0822035425683,37.42228990140251,0</coordinates>
        </Point>
      </Placemark>
    </Document>
    </kml>
'''

begin_file()
