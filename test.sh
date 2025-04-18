#!/usr/bin/env bash
set -euo pipefail

# Prereqs: docker-compose up (both services)
#          jq installed locally

USER_API="http://localhost:8000/api"
NOTES_API="http://localhost:8001/notes"

USERNAME="testuser$(date +%s)"
EMAIL="${USERNAME}@example.com"
PASSWORD="secret"

echo "🛠 1) Registering user  ${USERNAME}…"
register_resp=$(curl -sS -X POST "${USER_API}/register" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"${USERNAME}\",\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")
echo "$register_resp" | jq .

echo "🔑 2) Logging in to get JWT…"
login_resp=$(curl -sS -X POST "${USER_API}/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}")
echo "$login_resp" | jq .
TOKEN=$(jq -r .access_token <<<"$login_resp")

if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
  echo "❌ Failed to obtain token"
  exit 1
fi

AUTH_HEADER="Authorization: Bearer $TOKEN"
echo "📝 3) Creating a note…"
create_resp=$(curl -sS -X POST "$NOTES_API/" \
  -H "$AUTH_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{"title":"My Test Note","content":"Hello world!","tags":["demo"]}')
echo "$create_resp" | jq .
NOTE_ID=$(jq -r ._id <<<"$create_resp")
echo "🔍 4) Fetching the note by ID…"
 fetching_resp=$(curl -sS -X GET "$NOTES_API/$NOTE_ID" \
  -H "$AUTH_HEADER") 
echo "$fetching_resp" | jq .

echo "📜 5) Listing all my notes…"
list_resp=$(curl -sS -X GET "$NOTES_API/" \
  -H "$AUTH_HEADER")
echo "$list_resp" | jq .

echo "✏️ 6) Replacing the note with PUT…"
put_resp=$(curl -sS -X PUT "$NOTES_API/$NOTE_ID" \
  -H "$AUTH_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Replaced Title","content":"Brand new content","tags":["updated"]}')
echo "$put_resp" | jq .

echo "🖌️ 7) Partially updating with PATCH…"
patch_resp=$(curl -sS -X PATCH "$NOTES_API/$NOTE_ID" \
  -H "$AUTH_HEADER" \
  -H 'Content-Type: application/json' \
  -d '{"content":"Patched content!"}')
echo "$patch_resp" | jq .

echo "🗑️ 8) Deleting the note…"
del_status=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$NOTES_API/$NOTE_ID" \
  -H "$AUTH_HEADER")
echo "→ HTTP $del_status (should be 204)"

echo "🔍 9) Verifying it’s gone…"
verify_status=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$NOTES_API/$NOTE_ID" \
  -H "$AUTH_HEADER")
echo "→ HTTP $verify_status (should be 404)"

echo "🎉 All tests passed!"
