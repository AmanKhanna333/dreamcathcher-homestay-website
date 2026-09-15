import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }

    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}

    try:
        # Debug — print everything
        print("EVENT:", json.dumps(event))
        
        body = json.loads(event.get('body', '{}'))
        print("BODY:", json.dumps(body))

        name      = body.get('name', '')
        email     = body.get('email', '')
        phone     = body.get('phone', '')
        room      = body.get('room', '')
        check_in  = body.get('checkIn', '')
        check_out = body.get('checkOut', '')
        guests    = body.get('guests', '')
        trekking  = body.get('trekking', '')
        message   = body.get('message', '')

        booking_id = str(uuid.uuid4())[:8].upper()
        timestamp  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connect to DynamoDB
        print("Connecting to DynamoDB...")
        dynamodb = boto3.resource('dynamodb')
        
        # List all tables for debugging
        client = boto3.client('dynamodb')
        tables = client.list_tables()
        print("TABLES FOUND:", tables['TableNames'])

        table = dynamodb.Table('DreamcatherBookings')
        print("Table object created:", table.name)

        # Save to DynamoDB
        table.put_item(Item={
            'bookingID':  booking_id,
            'timestamp':  timestamp,
            'name':       name,
            'email':      email,
            'phone':      phone,
            'room':       room,
            'checkIn':    check_in,
            'checkOut':   check_out,
            'guests':     guests,
            'trekking':   trekking,
            'message':    message,
            'status':     'pending'
        })
        print("DynamoDB save successful!")

        # Send emails
        ses = boto3.client('ses', region_name='ap-south-1')
        HOST_EMAIL = 'meseize4@gmail.com'
        FROM_EMAIL = 'meseize4@gmail.com'

        booking_id_display = f"#{booking_id}"

        guest_subject = f"Booking Request Received — Dreamcatcher Homestay {booking_id_display}"
        guest_body = f"""
Dear {name},

Thank you for choosing Dreamcatcher Homestay, Dharamkot.

Your booking request has been received and we will confirm via WhatsApp within a few hours.

BOOKING DETAILS
───────────────────────────
Booking ID  : {booking_id_display}
Room        : {room}
Check-in    : {check_in} at 10:00 AM
Check-out   : {check_out} at 11:30 AM
Guests      : {guests}
Trekking    : {trekking}
───────────────────────────

We will reach you on WhatsApp at {phone} shortly.
For anything urgent: +91 97368 92850

Come as a stranger. Leave as someone who remembers.

Warm regards,
Dreamcatcher Homestay
Dharamkot, Dharamshala
@dreamcatcher_homestays
        """

        host_subject = f"NEW BOOKING {booking_id_display} — {name} — {room}"
        host_body = f"""
NEW BOOKING REQUEST
Received: {timestamp}

GUEST
─────────────────────────
Name     : {name}
Email    : {email}
WhatsApp : {phone}
─────────────────────────

STAY
─────────────────────────
Room     : {room}
Check-in : {check_in}
Check-out: {check_out}
Guests   : {guests}
Trekking : {trekking}
─────────────────────────

MESSAGE:
{message if message else 'None'}

Reply on WhatsApp: {phone}
        """

        try:
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': guest_subject},
                    'Body': {'Text': {'Data': guest_body}}
                }
            )
            print("Guest email sent!")
        except Exception as e:
            print(f"Guest email error: {e}")

        try:
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': [HOST_EMAIL]},
                Message={
                    'Subject': {'Data': host_subject},
                    'Body': {'Text': {'Data': host_body}}
                }
            )
            print("Host email sent!")
        except Exception as e:
            print(f"Host email error: {e}")

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': f"Thank you {name}! Booking {booking_id_display} received. We will confirm on WhatsApp at {phone} within a few hours.",
                'bookingID': booking_id
            })
        }

    except Exception as e:
        print(f"MAIN ERROR: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'message': 'Something went wrong. Please WhatsApp us directly at +91 97368 92850.'
            })
        }
