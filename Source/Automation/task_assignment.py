"""
    This module is used for interpreting requested operation
    information and assign task for the execution of that operation.

    The task_assignment_execution(operation) function typically takes
    input a dictionary responsible for carrying data and operation command.

    for example,

    {
        "operation" : "open app",
        "application" : "spotify"
    }


    {
        "operation" : "send a sms",
        "phone" : "0123456789",
        "message" : "hi"
    }

        
    {
        "operation" : "open app",
        "application" : "spotify"
    }

    {
        "operation": "shell command",
        "command" : "dir"
    }

    {
        "operation" : "send an email with attachment",
        "reciever" : "marvelfan389@gmail.com",
        "subject" : "Wishing Happy birthday",
        "body" : "Happy birthday Dragon. Wish you a very happy birthday."
    }

    {
        "operation" : "send an email",
        "reciever" : "marvelfan389@gmail.com",
        "subject" : "Greetings from Jadugar",
        "body" : "Hello, I am jadugar how are you?"
    }


    {
        "operation" : "send a sms",
        "phone" : "0123456789",
        "message" : "hi"
    }

"""





# Main Assignment function


def task_assignment_and_execution(operation: dict):
    """
    This function is used to assign task to appropriate modules
    that can handle them and execute them.

    To run a specific task each task has a example of how it will
    take the operation dictionary as input to execute a certain 
    operation.

    """

    if "open app" in operation['operation']:
        from app_starter import app_runner
        app_runner(operation['app'])


    elif "shell command" in operation['operation']:
        from subprocess import run 
        run(operation['command'], shell=True)

        
    elif ("send an email with attachment" in operation['operation']) or ("send email with attachment" in operation['operation']):
        from my_mail import email
        email(
            reciever = operation['reciever'], 
            subject = operation['subject'], 
            body = operation['body'], 
            attachment = True
        )


    elif "send email" in operation['operation']:
        from my_mail import email
        email(
            reciever = operation['reciever'], 
            subject = operation['subject'], 
            body = operation['body']
        )


    
    elif "send bulk email with attachment" in operation['operation']:
        from my_mail import bulk_email
        bulk_email(
            recievers = operation['recievers'],
            subject = operation['subject'],
            body = operation['body'],
            attachment = True
        )


    elif "send bulk email" in operation['operation']:
        from my_mail import bulk_email
        bulk_email(
            recievers = operation['recievers'],
            subject = operation['subject'],
            body = operation['body']
        )

            
    elif "send sms" in operation['operation']:
        from sms_sender import sms_sender

        sms_sender(
                phone = operation['phone'],
                message = operation['message']   
            )
        
        

    elif "send whatsapp with attachment" in operation['operation']:
         from send_whatsapp import send_whatsapp_with_attachment

         send_whatsapp_with_attachment(phone = operation['phone'],
                                       message = operation['message']
                                       )
 
    elif ("send whatsapp" in operation['operation']) or ("sending whatsapp message" in operation['operation']):
        from send_whatsapp import send_whatsapp

        send_whatsapp(
            phone = operation['phone'],
            message = operation['message']
        )


    elif "volume" in operation['operation']:
        from volume import set_volume

        set_volume(int(operation['volume']))
        print("Volume Set successful")


    elif "my location" in operation['operation']:
        from my_location import get_my_location
        
        get_my_location()


    elif "text_to_audio" in operation['operation']:
        from text_to_audio import text_to_audio

        text_to_audio(operation['text'], operation['file_name'])

    
    elif "sms_via_mobile" in operation['operation']:
        from sms_via_mobile import sms_via_mobile

        sms_via_mobile(operation['phone'], operation['message'])

    elif "capture two images and paste second on first somewhere at top-left" in operation['operation']:
        from two_photo import capture_and_merge_interactive

        capture_and_merge_interactive()


    elif "sunglass filter" in operation['operation']:
        from sunglass_filter import filter
        filter()

    elif "gray filter" in operation['operation']:
        from gray_image import capture_and_process_image
        capture_and_process_image()

    
    elif "open website" in operation['operation']:
        from webbrowser import open

        open(operation['website_link'])

  