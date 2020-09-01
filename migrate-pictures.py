from frappeclient import FrappeClient
import base64

USERNAME = "administrator"
PASSWORD = "admin@123"
HOST = "https://nrp.gourmetpakistan.com/"

def migrate():
    print("logging in...")
    client = FrappeClient(HOST, USERNAME, PASSWORD)
    limit = 100
    offset = 0
    all_synced = True
    while(all_synced):
        employees_list = client.get_list('Employee', fields = ['name', 'cnic_no'], filters = {'name':'024232','status':'Active',"image":["<","0"]}, limit_start=offset, limit_page_length=limit)
        if(len(employees_list) < limit):
            all_synced = False

        for employee in employees_list:
            try:
                emp = client.get_doc('Employee', employee["name"])
                filename = "{0}.jpg".format(employee["cnic_no"])
                img_str = get_base64_encoded_image("source/pictures/{0}".format(filename))
                if(img_str):
                    file_path = upload_file(client=client, employee=employee["name"], filename=filename, filedata=img_str)

                    if(file_path):
                        emp = client.get_doc('Employee', employee["name"])
                        emp["image"] = file_path
                        client.update(emp)

            except Exception as e:
                print('Failed to upload file for employee: {0}   {1}'.format(employee["name"],e))
                continue
        
        offset += limit

def get_base64_encoded_image(image_location):
    with open(image_location, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    return False


def upload_file(client, employee, filename, filedata):
    if client:
        payload = {
            'cmd': 'uploadfile',
            'doctype': 'Employee',
            'docname':  employee,
            'filename': filename,
            'filedata': filedata,
            'from_form': '1'
        }
        res = client.post_api("uploadfile",params=payload)
        if("file_url" in res):
            return res["file_url"]

        return False

if __name__=="__main__":
    migrate()
