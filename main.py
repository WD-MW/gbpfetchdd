from flask import Flask, send_file, Response
import requests
import base64
import io

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate_pdf():
    try:
        url = "https://production-sfo.browserless.io/chromium/bql?token=SAho7NBFdqUTAn97462feca6224d92059ff2e5b643&humanlike=true&blockConsentModals=true"

        payload = {
            "query": """mutation CaptureDashboardData {
              useProxy: proxy(
                server: "http://eiztQOQ2Ov6L4Je:N0ogocryyUw2iJS@95.135.112.66:45275",
                type: [document, xhr]
              ) { time }
              setCookies: cookies(cookies: [
                { name: "_www_session", value: "48b51300ee5d92ec41bbcde90f2735df", domain: "admin.admin-gobetplay.com", path: "/", httpOnly: true, secure: false },
                { name: "ahoy_visit", value: "41e277cc-c0b3-4e2f-80d1-4f7b7f152985", domain: "admin.admin-gobetplay.com", path: "/" },
                { name: "ahoy_visitor", value: "db758ba8-4dc0-46a5-87e7-6633d6199088", domain: "admin.admin-gobetplay.com", path: "/" },
                { name: "cable_token", value: "48b51300ee5d92ec41bbcde90f2735df", domain: "admin.admin-gobetplay.com", path: "/" }
              ]) { time }
              goToDashboard: goto(
                url: "https://admin.admin-gobetplay.com/data_overviews?user_type=normal&period_time=today",
                waitUntil: networkIdle
              ) { status time }
              wait20Seconds: waitForTimeout(time: 20000) { time }
              capturePDF: pdf(
                format: a4,
                landscape: false,
                printBackground: false,
                scale: 0.75
              ) {
                base64
              }
            }""",
            "operationName": "CaptureDashboardData",
            "variables": {}
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        base64_pdf = response.json().get("data", {}).get("capturePDF", {}).get("base64")

        if not base64_pdf:
            return Response("No PDF returned", status=500)

        pdf_bytes = base64.b64decode(base64_pdf)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="dashboard.pdf"
        )

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)
