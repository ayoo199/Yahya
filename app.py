import requests
import httpx
import random
import string
import uuid
import time
from datetime import datetime
from user_agent import generate_user_agent

karbo ='7544050270:AAGcCNPdh-yS1W85jnAi3eziLDf1Xlzk44w'

karbo_api = f"https://api.telegram.org/bot{karbo}"

user_states = {}

state_karbo = {
    "ar": {
        "welcome":       "- هلا حب اختار شتريد :",
        "btn_reset":     "ارسال ريست",
        "btn_change":    "تغيير باسورد",
        "ask_user":      "ارسل الايميل او اليوزر:",
        "ask_link":      "- ارسل رابط الريست :",
        "ask_pass":      "- ارسل كلمة السر الجديدة:",
        "success_reset": "- تم ارسال الريست\n{}",
        "fail_reset":    "- فشل الارسال\n{}",
        "success_pass":  "- تم تغيير الباسورد بنجاح\nالباسورد الجديد : {}",
        "fail_pass":     "- فشل تغيير الباسورد\n{}",
        "choose_lang":   "- اختر اللغة / Choose Language :",
        "btn_ar":        "العربية",
        "btn_en":        "English",
    },
    "en": {
        "welcome":       "- Hello my love choose :",
        "btn_reset":     "Send Reset",
        "btn_change":    "Change Password",
        "ask_user":      "- Send your Email or Username :",
        "ask_link":      "- Send the Reset Link :",
        "ask_pass":      "- Send the new password :",
        "success_reset": "- Reset sent successfully\n{}",
        "fail_reset":    "- Failed to send reset\n{}",
        "success_pass":  "- Password changed successfully\nNew password: {}",
        "fail_pass":     "- Failed to change password\n{}",
        "choose_lang":   "- اختر اللغة / Choose Language :",
        "btn_ar":        "العربية",
        "btn_en":        "English",
    }
}

def t(chat_id, key):
    lang = user_states.get(chat_id, {}).get("lang", "ar")
    return state_karbo[lang][key]


def _gDv(new_password):
    aid = f"android-{''.join(random.choices(string.hexdigits.lower(), k=16))}"
    ua = (
        f"Instagram 394.0.0.46.81 Android "
        f"({random.choice(['29/10', '30/11', '31/12'])}; "
        f"{random.choice(['320dpi', '480dpi'])}; "
        f"{random.choice(['720x1280', '1080x1920'])}; "
        f"{random.choice(['samsung', 'xiaomi', 'google'])}; "
        f"{random.choice(['SM-G975F', 'Mi-9T', 'Pixel-4'])}; "
        f"en_US; {random.randint(100000000, 999999999)})"
    )
    wf = str(uuid.uuid4())
    ts = int(datetime.now().timestamp())
    pw = f"#PWD_INSTAGRAM:0:{ts}:{new_password}"
    return aid, ua, wf, pw


def Eizonxtool(user):
    try:
        headers = {
            "user-agent": generate_user_agent(),
            "x-ig-app-id": "936619743392459",
            "x-requested-with": "XMLHttpRequest",
            "x-instagram-ajax": "1032099486",
            "x-csrftoken": "missing",
            "x-asbd-id": "359341",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/accounts/password/reset/",
            "accept-language": "en-US",
            "priority": "u=1, i",
        }
        r = httpx.Client(http2=True, headers=headers, timeout=20).post(
            "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
            data={"email_or_username": user}
        )
        response = r.json()
        contact = response.get('contact_point', 'Not found')
        return {"success": True, "contact": contact}
    except Exception as e:
        return {"success": False, "error": str(e)}


def make_headers(mid="", user_agent=""):
    return {
        "User-Agent": user_agent,
        "X-Mid": mid,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
    }


def _rLk(reset_link, new_password):
    try:
        ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD = _gDv(new_password)

        uidb36 = reset_link.split("uidb36=")[1].split("&token=")[0]
        token = reset_link.split("&token=")[1].split(":")[0]

        url = "https://i.instagram.com/api/v1/accounts/password_reset/"
        data = {
            "source": "one_click_login_email",
            "uidb36": uidb36,
            "device_id": ANDROID_ID,
            "token": token,
            "waterfall_id": WATERFALL_ID
        }

        r = requests.post(url, headers=make_headers(user_agent=USER_AGENT), data=data)

        if "user_id" not in r.text:
            return {"success": False, "error": r.text}

        mid = r.headers.get("Ig-Set-X-Mid")
        resp = r.json()

        user_id = resp.get("user_id")
        cni = resp.get("cni")
        nonce_code = resp.get("nonce_code")
        challenge_context = resp.get("challenge_context")

        url2 = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
        data2 = {
            "user_id": str(user_id),
            "cni": str(cni),
            "nonce_code": str(nonce_code),
            "bk_client_context": (
                '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",'
                '"styles_id":"instagram"}'
            ),
            "challenge_context": str(challenge_context),
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "get_challenge": "true"
        }

        r2 = requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data2).text

        if str(cni) not in r2:
            return {"success": False, "error": "Challenge failed"}

        challenge_final = r2.replace("\\", "").split(f"(bk.action.i64.Const, {cni}), \"")[1].split(
            "\", (bk.action.bool.Const, false)))"
        )[0]

        data3 = {
            "is_caa": "False",
            "cni": str(cni),
            "challenge_context": challenge_final,
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "enc_new_password1": PASSWORD,
            "enc_new_password2": PASSWORD
        }

        requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data3)

        return {"success": True, "password": new_password}

    except Exception as e:
        return {"success": False, "error": str(e)}

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{karbo_api}/sendMessage", json=payload)


def answer_callback(callback_id, text=""):
    requests.post(f"{karbo_api}/answerCallbackQuery", json={"callback_query_id": callback_id, "text": text})


def lang_menu(chat_id):
    markup = {
        "inline_keyboard": [
            [
                {"text": state_karbo["ar"]["btn_ar"], "callback_data": "lang_ar"},
                {"text": state_karbo["ar"]["btn_en"], "callback_data": "lang_en"}
            ]
        ]
    }
    send_message(chat_id, state_karbo["ar"]["choose_lang"], markup)


def main_menu(chat_id):
    markup = {
        "inline_keyboard": [
            [{"text": t(chat_id, "btn_reset"),  "callback_data": "send_reset"}],
            [{"text": t(chat_id, "btn_change"), "callback_data": "change_pass"}]
        ]
    }
    send_message(chat_id, t(chat_id, "welcome"), markup)


def get_updates(offset=None):
    params = {"timeout": 30, "allowed_updates": ["message", "callback_query"]}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(f"{karbo_api}/getUpdates", params=params, timeout=35)
        return r.json().get("result", [])
    except:
        return []


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        user_states[chat_id] = {"state": "choosing_lang", "lang": "ar"}
        lang_menu(chat_id)
        return

    state_data = user_states.get(chat_id, {"state": "idle", "lang": "ar"})
    state = state_data.get("state", "idle")

    if state == "waiting_user_reset":
        result = Eizonxtool(text.strip())
        if result.get("success"):
            send_message(chat_id, t(chat_id, "success_reset").format(result["contact"]))
        else:
            send_message(chat_id, t(chat_id, "fail_reset").format(result.get("error", "")))
        user_states[chat_id]["state"] = "idle"
        main_menu(chat_id)

    elif state == "waiting_reset_link":
        user_states[chat_id]["state"] = "waiting_new_pass"
        user_states[chat_id]["data"] = {"link": text.strip()}
        send_message(chat_id, t(chat_id, "ask_pass"))

    elif state == "waiting_new_pass":
        link = state_data.get("data", {}).get("link", "")
        new_pass = text.strip()
        result = _rLk(link, new_pass)
        if result.get("success"):
            send_message(chat_id, t(chat_id, "success_pass").format(f"<code>{result['password']}</code>"))
        else:
            send_message(chat_id, t(chat_id, "fail_pass").format(result.get("error", "")))
        user_states[chat_id]["state"] = "idle"
        main_menu(chat_id)


def handle_callback(callback):
    chat_id = callback["message"]["chat"]["id"]
    data = callback.get("data", "")
    callback_id = callback["id"]

    answer_callback(callback_id)

    if data == "lang_ar":
        user_states[chat_id] = {"state": "idle", "lang": "ar"}
        main_menu(chat_id)

    elif data == "lang_en":
        user_states[chat_id] = {"state": "idle", "lang": "en"}
        main_menu(chat_id)

    elif data == "send_reset":
        user_states[chat_id]["state"] = "waiting_user_reset"
        send_message(chat_id, t(chat_id, "ask_user"))

    elif data == "change_pass":
        user_states[chat_id]["state"] = "waiting_reset_link"
        send_message(chat_id, t(chat_id, "ask_link"))


def run():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            if "message" in update:
                handle_message(update["message"])
            elif "callback_query" in update:
                handle_callback(update["callback_query"])
        time.sleep(0.5)


if __name__ == "__main__":
    run()
