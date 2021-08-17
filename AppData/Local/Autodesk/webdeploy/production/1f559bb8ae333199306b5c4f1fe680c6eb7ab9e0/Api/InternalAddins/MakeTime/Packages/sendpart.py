from . import requests


def send(url, payload_data, step_file, time, verification=True):
    # Set default message
    message = "Unfortunately, there are invalid entries in your project form. Please check the entries in your project form and try submitting again."

    # Send to platform
    try:
        # Get response
        res = requests.post(url, data=payload_data, files=step_file, timeout=time, verify=verification)

        # Check status
        if res.status_code == 200:  # success
            if 'user_name' in res.json():
                message = "Thank you for submitting your project to MakeTime, " + res.json()['user_name'] + "! Please check your e-mail for instructions on the next steps."
            else:
                message = "Thank you for submitting your project to MakeTime! Please check your e-mail for instructions on the next steps."

        else:  # failure/res.status_code==422
            if 'errors' in res.json():  # invalid entry
                if 'author_name' in res.json()['errors']:
                    message = "Unfortunately, the length of your name is too long. Please enter a shorter name and try submitting again."
                elif 'email' in res.json()['errors']:
                    if 'is too long (maximum is 255 characters)' in res.json()['errors']['email']:
                        message = "Unfortunately, the length of your e-mail is too long. Please enter a shorter e-mail address and try submitting again."
                    elif'is invalid' in res.json()['errors']['email']:
                        message = "Unfortunately, your e-mail address is invalid. Please check the e-mail you entered and try submitting again."
                elif 'phone' in res.json()['errors']:
                    message = "Unfortunately, the phone number you entered is too short (minimum is 10 digits). Please enter a longer phone number and try submitting again."
                elif 'material_type' in res.json()['errors']:
                    message = "Unfortunately, the length of the name of your material type is too long. Please enter a shorter material type name and try submitting again."
                elif 'material_grade' in res.json()['errors']:
                    message = "Unfortunately, the length of the name of your material grade is too long. Please enter a shorter material grade name and try submitting again."
                elif 'part_number' in res.json()['errors']:
                    message = "Unfortunately, the length of your part number is too long. Please enter a shorter part number and try submitting again."
                elif 'name' in res.json()['errors']:
                    if "can\'t be blank" in res.json()['errors']['name']:
                        message = "Unfortunately, we were not able to process your request. Please make sure your part number is entered and try submitting again."
                    elif 'is too long (maximum is 128 characters)' in res.json()['errors']['name']:
                        message = "Unfortunately, the length of the name of your part is too long. Please enter a shorter part number and try submitting again."
                elif 'description' in res.json()['errors']:
                    message = "Unfortunately, the length of one or more of your entries is too long. Please check the length of each of your entries and try submitting again."

            elif 'fields' in res.json(): # missing field
                if 'user_company_name' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your company name is entered and try submitting again."
                elif 'user_name' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your name is entered and try submitting again."
                elif 'user_email' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your e-mail is entered and try submitting again."
                elif 'user_phone' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your phone number is entered and try submitting again."
                elif 'part_number' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your part number is entered and try submitting again."
                elif 'material_type' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your material type is entered and try submitting again."
                elif 'material_grade' in res.json()['fields']:
                    message = "Unfortunately, we were not able to process your request. Please make sure your material grade is entered and try submitting again."

    # Connection timed out
    except requests.exceptions.ConnectTimeout:
        message = "Connection timed out."

    # Failed to connect
    except requests.exceptions.ConnectionError:
        message = "Connection error."

    # Return result
    return message
