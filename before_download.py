
import os
import os
import zipfile



def remove_files(directory):
    for file in os.listdir(directory):
        os.remove(directory+'/'+file)

def remove_coordinates():
    os.remove("static/coordinates.list")



def compress_results():
    fantasy_zip = zipfile.ZipFile('static/result.zip', 'w')

    for folder, subfolders, files in os.walk('static/detected'):

        for file in files:
            fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'static/detected'), compress_type = zipfile.ZIP_DEFLATED)



    fantasy_zip.write(os.path.join('static/', 'coordinates.list'), os.path.relpath(os.path.join('static/','coordinates.list'), 'static/'), compress_type = zipfile.ZIP_DEFLATED)

    fantasy_zip.close()


def main():
    compress_results()
    remove_files('static/temp')
    remove_files('static/img')
    remove_files('static/detected')
    remove_coordinates()
