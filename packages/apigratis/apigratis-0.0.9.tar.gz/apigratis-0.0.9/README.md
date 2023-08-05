# SDK Python - APIGratis by API BRASIL 🚀
Conjunto de API, para desenvolvedores.

Transforme seus projetos em soluções inteligentes com nossa API. Com recursos como API do WhatsApp, geolocalização, rastreamento de encomendas, verificação de CPF/CNPJ e mais, você pode criar soluções eficientes e funcionais. Comece agora.
# Como instalar

https://pypi.org/project/apigratis/0.0.9/

```pip3 install apigratis==0.0.9```

# Como utilizar

```python

from apigratis.Service import Service
import json

def main():

    sendText = Service.whatsapp(json.dumps({
        "action": "sendText",
        "credentials": {
            "SecretKey": "SEU_SECRET_KEY"
            "PublicToken": "SEU_PUBLIC_TOKEN",
            "DeviceToken": "SEU_DEVICE_TOKEN",
            "BearerToken": "SEU_BEARER_TOKEN",
        },
        "body": {
            "message": "Hello World por Python",
            "phone": "5531994359434",
            "time_typing": 1
        }
    }))

    print(sendText)

if __name__ == "__main__":
    main()
```