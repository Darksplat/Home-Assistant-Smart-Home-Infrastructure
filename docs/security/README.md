# Security

## Public repository rules

Never commit:

- Home Assistant access tokens
- passwords
- API keys
- MQTT credentials
- Wi-Fi credentials
- webhook identifiers
- private certificates
- authentication cookies
- cloud integration tokens

Use placeholders and `secrets.yaml` references instead.
