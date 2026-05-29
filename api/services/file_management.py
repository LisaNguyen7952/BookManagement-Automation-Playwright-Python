class FileManagement:
    BASE_PATH = "/api/file"

    def __init__(self, api_client):
        self.api = api_client

    def upload_file(self, file_path, server_path="/"):
        import os

        file_name = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            return self.api.post(
                self.BASE_PATH,
                multipart={
                    "files[]": {
                        "name": file_name,
                        "mimeType": "application/octet-stream",
                        "buffer": f.read()
                    },
                    "path": server_path
                }
            )

    def get_file_list(self, headers=None, params=None):
        return self.api.get(f"{self.BASE_PATH}", headers=headers, params=params)
    def delete_file(self, file_id):
        return self.api.delete(f"{self.BASE_PATH}/{file_id}")
    def rename_file(self, file_name, file_path):
        return self.api.put(f"{self.BASE_PATH}/rename", json={"path": file_path,"name":file_name})
    def move_file(self, oldPath, newPath):
        return self.api.put(f"{self.BASE_PATH}/move", json={"oldPath": oldPath,"newPath": newPath})