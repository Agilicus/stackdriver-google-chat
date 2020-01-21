import sys
import logging
import json
import os
import aiohttp
from http import HTTPStatus

from quart import Quart
from quart import Response, request

logger = logging.getLogger(__name__)
logger.info(
    "Stackdriver webhook-sample starting up on %s"
    % (sys.version.replace("\n", " "))
)

APP = Quart("webhook-to-chat")


@APP.route("/", methods=["POST"])
async def token_auth_handler():
    """ Handle a webhook post with an associated authentication token """
    auth_token = request.args.get("token")

    if not auth_token or not _check_token_auth(auth_token):
        error_msg = "403 Please pass the correct authentication token"
        logger.error(error_msg)
        return Response(error_msg, 403)
    else:
        req = await request.get_data()
        try:
            logger.info(req)
            json_data = json.loads(req)
            #logger.info(json.dumps(json_data, indent=4))
        except json.decoder.JSONDecodeError:
            return Response("Malformed JSON", 400)
        resp, status = await postit(formatit(json_data))
        return Response(resp, status)


def _check_token_auth(auth_token):
    """This function is called to check if a submitted token argument matches
       the expected token """
    token = os.getenv('TOKEN')
    if token:
        return auth_token == os.getenv('TOKEN')
    else:
        return False

def formatit(json_data):
    txt = json.dumps(json_data, indent=2, sort_keys=True)
    if 'incident' in json_data and 'state' in json_data['incident']:
        if json_data['incident']['state'] == 'open':
            state = 'FAILING'
            colour = "#ff0000"
        else:
            state = 'RESTORED'
            colour = "#00ff00"
        card = { "cards" : [ { "sections": [ { "widgets": [ { "textParagraph": {
          "text": f"<font color=\"{colour}\">{state}: {json_data['incident']['condition_name']}</font><br><a href=\"{json_data['incident']['url']}\">Details</a><br>"
        } } ] } ] } ], "text": f"```\n{txt}\n```"}
        return str(card)
    else:
        return str({"text": f"```\n{txt}\n```"})

async def postit(data):
    url = os.getenv('URL')
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            allow_redirects=True,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            data=data,
        ) as response:
            resp = await response.json()
            if response.status != HTTPStatus.OK:
                return "Error to upstream %s" % response.status, 503
        return "OK", 200
