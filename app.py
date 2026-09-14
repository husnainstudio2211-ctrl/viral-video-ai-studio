from google import genai

# اپنی AQ والی API کی یہاں درج کریں
client = genai.Client(api_key="AQ.آپ_کی_کی_یہاں_آئے_ਗੀ")

response = client.models.generate_content(
    model='gemini-2.5-flash', # یا gemini-2.0-flash
    contents='سلام! آپ کیسے ہیں؟'
)

print(response.text)
