from .app_starter import app_runner
from .task_assignment import task_assignment_and_execution
from .load_attachment_address import load_attachment_address
from .my_mail import email
from .sms_sender import sms_sender
from .send_whatsapp import send_whatsapp, send_whatsapp_with_attachment
from .load_attachment_address import load_attachment_address
from .volume import get_current_volume, get_default_audio_device, set_volume
from .my_location import get_my_location
from .gray_image import capture_and_process_image
from .click_photo import click_photo_main
from .sms_via_mobile import sms_via_mobile
from .text_to_audio import text_to_audio
from ..crop_face_and_paste import capture_and_crop_face