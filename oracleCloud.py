import os
from dotenv import load_dotenv
load_dotenv()
import oci
from oci.config import validate_config

class OracleCloud:
    def __init__(self):
        self.config = {
            "user": os.environ.get("OCI_USER"),
            "key_file": os.environ.get("OCI_KEY_FILE"),
            "fingerprint": os.environ.get("OCI_FINGERPRINT"),
            "tenancy": os.environ.get("OCI_TENANCY"),
            "region": os.environ.get("OCI_REGION")
        }
        validate_config(self.config)
        self.speech_client = oci.ai_speech.AIServiceSpeechClient(self.config)
        self.compartment_id = os.environ.get("OCI_COMPARTMENT_ID")
        self.bucket_namespace = os.environ.get("OCI_BUCKET_NAMESPACE")
        self.bucket_name = os.environ.get("OCI_BUCKET_NAME")
        self.transcriptions_to_be_processed = []
        self.object_storage_client = oci.object_storage.ObjectStorageClient(self.config)
    
    def create_transcribe_job(self, display_name: str = '', description: str = '', job_prefix: str = '', file_list: list = []) -> None:
        sample_object_location = oci.ai_speech.models.ObjectLocation(namespace_name=self.bucket_namespace, bucket_name=self.bucket_name,
            object_names=file_list)
        sample_input_location = oci.ai_speech.models.ObjectListInlineInputLocation(
            location_type="OBJECT_LIST_INLINE_INPUT_LOCATION", object_locations=[sample_object_location])
        sample_output_location = oci.ai_speech.models.OutputLocation(namespace_name=self.bucket_namespace, bucket_name=self.bucket_name,
                                                             prefix=job_prefix)
        transcription_job_details = oci.ai_speech.models.CreateTranscriptionJobDetails(
                                                                                    display_name=display_name,
                                                                                    description=description,
                                                                                    compartment_id=self.compartment_id,
                                                                                    input_location=sample_input_location,
                                                                                    output_location=sample_output_location)
        
        self.transcription_job = None
        print("***CREATING TRANSCRIPTION JOB***")
        
        try:
            self.transcription_job = self.speech_client.create_transcription_job(create_transcription_job_details=transcription_job_details)
        except Exception as e:
            print(e)
        else:
            self.transcriptions_to_be_processed.append(self.transcription_job.data.id)
            print(self.transcription_job.data)
            
    def process_transcribed_jobs(self):
        print('starting getting transcriptions')
        aweme_transcript = {}
        for i in range(len(self.transcriptions_to_be_processed)):
            transcription_tasks = self.speech_client.list_transcription_tasks(self.transcriptions_to_be_processed[i])
            
            transcription_job = self.speech_client.get_transcription_job(self.transcriptions_to_be_processed[i])
            try:
                if transcription_job.data.lifecycle_state == 'SUCCEEDED':
                    #print(transcription_tasks.data)
                    for task in range(len(transcription_tasks.data.items)):
                        transcription_task = self.speech_client.get_transcription_task(self.transcriptions_to_be_processed[i], transcription_tasks.data.items[task].id)
                        object_name = transcription_task.data.output_location.object_names[0]
                        aweme_transcript[transcription_task.data.display_name.split('.')[0]] = self.get_transcript_by_name(object_name)
                    self.transcriptions_to_be_processed.pop(i)
                else:
                    continue
                
            except Exception as e:
                print(e)
                continue
        return aweme_transcript
                
    def get_transcript_by_name(self, name):
        object_list = self.object_storage_client.get_object(namespace_name=self.bucket_namespace, bucket_name=self.bucket_name, object_name=name)
        return object_list.data.json()["transcriptions"][0]["transcription"]
        #for o in object_list.data.objects:
        #    print(o.etag)
        
    def insert_into_bucket(self, file_stream, name, format='.mp4'):
        try:
            put_object_response = self.object_storage_client.put_object(namespace_name=self.bucket_namespace, bucket_name=self.bucket_name, object_name=name+format, put_object_body=file_stream)
        except Exception as e:
            print(e)
        else:
            print(put_object_response.headers)
    
    def list_bucket_items(self, prefix=''):
        try:
            item_list = []
            bucket_response = self.object_storage_client.list_objects(namespace_name=self.bucket_namespace, bucket_name=self.bucket_name, prefix=prefix)
        except Exception as e:
            print(e)
        else:
            for i in bucket_response.data.objects:
                item_list.append(i.name)
        
        


"""object_storage_client = oci.object_storage.ObjectStorageClient(config)
object_list = object_storage_client.list_objects('axs30owyng21', 'tiktok' , fields="name,timeCreated,size")
for o in object_list.data.objects:
    print(o.name)"""
if __name__ == '__main__':
    speech = OracleCloud()
    speech.transcriptions_to_be_processed.append('ocid1.aispeechtranscriptionjob.oc1.mx-queretaro-1.amaaaaaa5g4nx6qazyqpko5hsrnzt23vsqxgcpnxiiwu7tfxufzmxwjiucoa')
    speech.process_transcribed_jobs()
    #item = 'pythoncode/job-amaaaaaa5g4nx6qanvjq4ywkq4eovudepd3xcb3mwfatcvu7b2i7zdirvpga/axs30owyng21_tiktok_tiktoktext.mp4.json'
    #speech.get_bucket_item(item)
    #request = requests.get('https://v16m-default.akamaized.net/f0026ecefc9ebddaced812abcb55de7d/65399b2a/video/tos/maliva/tos-maliva-ve-0068c799-us/oM8hQEVLzEob0kLCABfQSZRenBt9lDDIhigXEJ/?a=0&ch=0&cr=0&dr=0&er=0&cd=0%7C0%7C1%7C0&cv=1&br=616&bt=308&bti=OTg7QC0wM2A%3D&cs=0&ds=3&ft=iJOG.y7oZZv0PD1K3ZVxg9wA.vDjkEeC~&mime_type=video_mp4&qs=0&rc=M2YzPDM7aTZmZmZkaGk0NkBpMzo3b2U6Zmk3bjMzZzczNEBfNDZgY2FjXl4xLy4vYzIwYSNuMHAycjRfLmZgLS1kMS9zcw%3D%3D&l=202310251646242AD1CC376E791274D97B&btag=e00090000')
    #request_content = request.content
    #speech.insert_into_bucket(file_stream=request_content, name='from_python/from_python.mp4')
    #speech.list_bucket_items('from_python/')
