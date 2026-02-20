# Add Webhook Directive

## Purpose
Set up a new Modal webhook endpoint mapped to a directive.

## Steps
1. Create a new directive in `directives/` for the webhook logic.
2. Add an entry to `execution/webhooks.json` mapping the webhook slug to the directive file.
3. Deploy the webhook: `modal deploy execution/modal_webhook.py`
4. Test the endpoint.

## Available tools for webhooks
- `send_email`
- `read_sheet`
- `update_sheet`

## Endpoints
- List: `https://nick-90891--claude-orchestrator-list-webhooks.modal.run`
- Execute: `https://nick-90891--claude-orchestrator-directive.modal.run?slug={slug}`
- Test email: `https://nick-90891--claude-orchestrator-test-email.modal.run`

## Notes
- All webhook activity streams to Slack in real-time.
- Only update this directive with explicit user approval.
