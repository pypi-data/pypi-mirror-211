import pandas as pd
import msal
import auth
import requests
import json
import base64
import os


class GraphAPI:
    def __init__(self, appid, client_secret, tenant_id, userid):
        self.appid = appid
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.userid = userid
        self.token = self.generate_token()

    def generate_token(self):
        app = msal.PublicClientApplication(
            self.appid, authority=f"https://login.microsoftonline.com/{self.tenant_id}/")
        token = auth.GenerateToken(
            self.appid, ['.default'], self.client_secret, 'client_credentials', self.tenant_id)
        return token

    def get_information(self):
        endpoint = 'https://graph.microsoft.com/v1.0/me'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        print(response.json())

    def get_mail(self):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/messages'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def get_all_mail(self):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/messages?$top=100000'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def get_top_100_mail(self):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/messages?$top=100'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def get_top_n_mail(self, n):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/messages?$top={str(n)}'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def get_top_10_mail(self):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/messages?$top=10'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def download_email_attachments(self, dir, id):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/messages/{id}/attachments'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        print(response.json())
        nameoffile = response.json()['value'][0]['name']
        base64Str = response.json()['value'][0]['contentBytes']
        decoded = base64.b64decode(base64Str)
        if not os.path.exists(dir):
            os.makedirs(dir)
        if os.path.isfile(dir + nameoffile):
            return {'filename': nameoffile}
        with open(dir + nameoffile, 'wb') as f:
            f.write(decoded)
        return {'filename': nameoffile}

    def upload_to_onedrive(self, filename, file_path, access_token):
        endpoint = f"https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root/children/{filename}/content"
        with open(file_path, "rb") as f:
            contents = f.read()
        encoded = base64.b64encode(contents).decode("utf-8")
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "text/plain"
        }
        payload = json.dumps({
            "@microsoft.graph.conflictBehavior": "replace",
            "base64": encoded
        })
        response = requests.put(endpoint, headers=headers, data=payload)
        if response.status_code == 200:
            print(response.text)
            return {"success": True, "message": "File uploaded successfully"}
        else:
            return {"success": False, "message": "Error uploading file: " + response.text}

    def create_folder(self, foldername):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root/children'
        if self.check_if_folder_exists(foldername):
            return {"success": False, "message": "Folder already exists"}
        else:
            headers = {
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "name": foldername,
                "folder": {},
                "@microsoft.graph.conflictBehavior": "rename"
            })
            response = requests.post(endpoint, headers=headers, data=payload)
            if response.status_code == 200:
                print(response.text)
                return {"success": True, "message": "Folder created successfully"}
            else:
                return {"success": False, "message": "Error creating folder: " + response.text}

    def list_items_in_drive(self):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root/children'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def search_for_file(self, queryname):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root/search(q=\'{queryname}\')'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def upload_file_to_folder(self, filename, path):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{path}/{filename}:/content'
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'text/plain'
        }
        with open(filename, "rb") as f:
            contents = f.read()
        payload = contents
        response = requests.put(endpoint, headers=headers, data=payload)
        if response.status_code == 200:
            print(response.text)
            return {"success": True, "message": "File uploaded successfully"}
        else:
            return {"success": False, "message": "Error uploading file: " + response.text}

    def download_file(self, filename, path, destination):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{path}/{filename}:/content'
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'text/plain'
        }
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            if os.path.exists(destination):
                os.remove(destination)
            fileData = response.content
            with open(destination, 'wb') as f:
                f.write(fileData)
            return {"success": True, "message": "File downloaded successfully"}
        else:
            return {"success": False, "message": "Error downloading file: " + response.text}

    def view_files_in_folder(self, folder):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{folder}:/children'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def delete_file(self, filename, folder):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{folder}/{filename}'
        response = requests.delete(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        if response.status_code == 204:
            return {"success": True, "message": "File deleted successfully"}
        else:
            return {"success": False, "message": "Error deleting file: " + response.text}

    def delete_folder(self, folder):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{folder}'
        response = requests.delete(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        if response.status_code == 204:
            return {"success": True, "message": "Folder deleted successfully"}
        else:
            return {"success": False, "message": "Error deleting folder: " + response.text}

    def create_share_link(self, filename, folder):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{folder}/{filename}:/createLink'
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "type": "view",
            "scope": "anonymous"
        })
        response = requests.post(endpoint, headers=headers, data=payload)
        if response.status_code == 200:
            return {"success": True, "message": "Link created successfully", "link": response.json()["link"]["webUrl"]}
        else:
            return {"success": False, "message": "Error creating link: " + response.text}

    def list_folders_in_dir(self, path):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{path}:/children'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def create_folder_dir(self, path, foldername):
        folders = self.list_folders_in_dir(path)
        for folder in folders["value"]:
            if folder["name"] == foldername:
                return {"success": False, "message": "Folder already exists"}
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{path}:/children'
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "name": foldername,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        })
        response = requests.post(endpoint, headers=headers, data=payload)
        if response.status_code == 200:
            print(response.text)
            return {"success": True, "message": "Folder created successfully"}
        else:
            return {"success": False, "message": "Error creating folder: " + response.text}

    def return_all_folders(self):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root/children'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()['value']

    def remove_all_empty_folders(self, directory):
        bCompletedDelete = False
        while not bCompletedDelete:
            dfAPI = pd.DataFrame(
                self.return_all_folders_in_directory(directory)['value'])
            bEmpty = True
            for index, row in dfAPI.iterrows():
                if row['folder']['childCount'] == 0:
                    self.delete_folder(row['name'])
                    print('Deleted folder: ' + row['name'])
                    bEmpty = False
                else:
                    pass
            if bEmpty:
                print('All empty folders deleted')
                bCompletedDelete = True

    def return_all_folders_in_directory(self, path):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{path}:/children'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        return response.json()

    def check_if_folder_exists(self, path):
        endpoint = f'https://graph.microsoft.com/v1.0/users/{self.userid}/drive/root:/{path}'
        response = requests.get(
            endpoint, headers={'Authorization': 'Bearer ' + self.token})
        if response.status_code == 200:
            return True
        else:
            return False


# Usage example:
if __name__ == '__main__':
    appid = ''
    client_secret = ''
    tenant_id = ''
    userid = ''

    api = GraphAPI(appid, client_secret, tenant_id, userid)
    api.get_information()
    mail = api.get_mail()
    print(mail)
