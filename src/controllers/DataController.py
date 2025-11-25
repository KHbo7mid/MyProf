from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os ,re
from .ProjectController import ProjectController
class DataController(BaseController) :
    
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 # convert MB to bytes
        
        
    def validate_uploaded_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False ,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True ,ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filepath(self,original_filename:str,project_id:str):
        random_str=self.generate_random_string(12)
        project_path=ProjectController().get_project_path(project_id=project_id)
        cleaned_filename=self.get_clean_filename(original_filename)
        new_file_name=f"{random_str}_{cleaned_filename}"
        new_file_path=os.path.join(project_path,new_file_name)
        while os.path.exists(new_file_path):
            random_str=self.generate_random_string(12)
            new_file_path=os.path.join(project_path,new_file_name)
            
            
        return new_file_path ,new_file_name
    
    def get_clean_filename(self,filename:str):
        cleaned_filename=re.sub(r'[^a-zA-Z0-9_.]', '', filename)
        return cleaned_filename
    
