from arrplat.resources.core.upload import FileUpload
import io
import hashlib


def image_object_upload_2_qiniu(image_obj):
    class Tmp:
        pass

    img_byte_arr = io.BytesIO()
    image_obj.save(img_byte_arr, format='png')
    img_byte_arr = img_byte_arr.getvalue()

    file_storage_simulation = Tmp()
    file_storage_simulation.stream = img_byte_arr

    image_file_name = hashlib.sha1(img_byte_arr).hexdigest()

    url = FileUpload.qiniu_upload_stream(file_storage_simulation, save_file_name="{}.png".format(image_file_name))
    return url

