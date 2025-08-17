import os, requests, json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Property
from .data_extract import extract


WABA_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

sessions = {}


def send_message(to: str, body: str):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WABA_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body}
    }

    try:
        r = requests.post(url, headers=headers, json=payload)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error sending message:", e)


def fetch_media(request, media_id):
    url = f"https://graph.facebook.com/v23.0/{media_id}"
    params = {"access_token": WABA_TOKEN}
    res = requests.get(url, params=params).json()
    media_url = res.get("url")

    if not media_url:
        return HttpResponse("Not found", status=404)

    media_res = requests.get(media_url, headers={"Authorization": f"Bearer {WABA_TOKEN}"})
    if media_res.status_code == 200:
        return HttpResponse(media_res.content, content_type=media_res.headers.get("Content-Type"))
    return HttpResponse("Error fetching media", status=500)

@csrf_exempt
def whatsapp_webhook(request):

    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("auth done")
            return HttpResponse(challenge)
        print("auth not done")
        return HttpResponse(status=403)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            entry = data.get('entry', [])[0]
            changes = entry.get('changes', [{}])[0]
            value = changes.get('value', {})
            messages = value.get('messages')

            if messages:
                msg = messages[0]
                from_number = msg["from"]
                msg_type = msg.get("type")
                session = sessions.get(from_number)
                if not session:
                    sessions[from_number] = {"stage": None, "draft": {"images": []}}
                    session = sessions[from_number]


                if session['stage'] is None:
                    if msg_type == 'text':
                        desc = msg.get('text', {}).get('body', '')
                        session['draft']["description"] = desc
                    elif msg_type == 'image':
                        image_id = msg.get('image', {}).get('id')
                        session['draft']["description"] = "(Image)"
                        session['draft']["images"].append(image_id)
                    else:
                        session['draft']["description"] = "(Unsupported message)"
                    session['stage'] = 'confirm'
                    send_message(from_number, 'Do you want to upload this property? (yes/no)')
                    return HttpResponse(status=200)

                if session['stage'] == 'confirm':
                    if msg_type == 'text' and msg.get('text', {}).get('body', '').strip().lower() == 'yes':
                        session['stage'] = 'image_upload'
                        send_message(from_number, 'Please upload property images. Send "DONE" when finished.')
                    else:
                        session.pop(from_number, None)
                        send_message(from_number, 'Okay, not saved.')
                    return HttpResponse(status=200)

                if session['stage'] == 'image_upload':
                    if msg_type == 'image':
                        image_id = msg.get('image', {}).get('id')
                        session['draft']["images"].append(image_id)
                        send_message(from_number, 'Image received ✅. Send more or type "DONE".')
                    elif msg_type == 'text' and msg.get('text', {}).get('body', '').strip().lower() == 'done':
                        session['stage'] = 'broker'
                        send_message(from_number, 'Great! Now, under which broker name should I save this?')
                    return HttpResponse(status=200)

                if session['stage'] == 'broker':
                    if msg_type == 'text':
                        broker_name = msg.get('text',{}).get('body', '').strip()
                        desc = session['draft'].get('description', '')

                        ai_data = extract(desc)

                        Property.objects.create(
                            broker_name = broker_name,
                            description = desc,
                            images = session['draft'].get('images', []),
                            ai_structure = ai_data.dict(),
                        )

                        send_message(from_number, 'Property saved ✅')
                        session.pop(from_number, None)
                    return HttpResponse(status=200)

        except Exception as e:
            print("webhook error", e)
            return HttpResponse(status=200)
    
    return HttpResponse(status=200)

def property_list(request):
    props = Property.objects.all().order_by("-timestamp").values(
        "id", "broker_name", "description", "images", "timestamp", "ai_structure"
    )
    return JsonResponse(list(props), safe=False)
