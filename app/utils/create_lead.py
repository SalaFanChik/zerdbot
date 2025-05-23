import aiohttp
from app.core.settings import get_settings

config = get_settings() 

ACCESS_TOKEN = config.access_token
BASE_DOMAIN = config.base_domain
if not ACCESS_TOKEN or not BASE_DOMAIN:
    raise ValueError("ACCESS_TOKEN and BASE_DOMAIN must be set in the environment variables.")

PIPELINE_ID = 8309902
STATUS_ID = 70850646

async def create_amocrm_lead_and_contact(name: str, phone: str, region: str):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        # 1. Сначала создаём контакт
        contact_payload = [{
            "name": name,
            "custom_fields_values": [{
                "field_code": "PHONE",
                "values": [{"value": phone, "enum_code": "MOB"}]
            }]
        }]

        async with session.post(
            f"https://{BASE_DOMAIN}/api/v4/contacts",
            headers=headers,
            json=contact_payload
        ) as contact_response:
            contact_result = await contact_response.json()
            if contact_response.status not in [200, 202]:
                return False, f"Ошибка при создании контакта: {contact_result}"

            contact_id = contact_result["_embedded"]["contacts"][0]["id"]

        # 2. Теперь создаём сделку с привязкой к контакту
        lead_payload = [{
            "name": f"{name} ({region})",
            "pipeline_id": PIPELINE_ID,
            "status_id": STATUS_ID,
            "custom_fields_values": [
                {
                    "field_id": 948743,  # ID поля "ВЫБЕРИТЕ_ОБЛАСТЬ"
                    "values": [{"value": region}]
                }
            ],
            "_embedded": {
                "contacts": [{"id": contact_id}],
                "tags": [{"name": "Telegram"}]
            }
        }]

        async with session.post(
            f"https://{BASE_DOMAIN}/api/v4/leads",
            headers=headers,
            json=lead_payload
        ) as lead_response:
            lead_result = await lead_response.json()
            if lead_response.status not in [200, 202]:
                return False, f"Ошибка при создании сделки: {lead_result}"

        return True, contact_id
