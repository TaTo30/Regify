import json
import command
import logging

from flask import Flask, request, Response

app = Flask(__name__)
logger = logging.getLogger(__name__)

def _struct_response(status, msg, data = None):
    return Response(status=status, headers=[('Content-Type', 'application/json')], response=json.dumps({'msg': msg, 'data': data}))

@app.route("/command", methods=["POST"])
def add_command():
    json_body = request.json
    try:       
        if 'command' not in json_body:
            return _struct_response(404, f"Missing 'command' field")
        if 'mui_verb' not in json_body:
            return _struct_response(404, f"Missing 'mui_verb' field")
    
        cmd = command.Command(json_body['command'], json_body['mui_verb'], json_body['icon'])
        logger.info(f"Adding command {cmd}")
        cmd.save()
        return _struct_response(200, "Command added", cmd.json())
    except Exception as e:
        logger.exception(e)
        return _struct_response(500, str(e))
    
@app.route("/command/", methods=["GET"])
@app.route("/command/<keyname>", methods=["GET"])
def get_commands(keyname=None):
    try: 
        cmds = []
        for cmd in command.commands():
            if keyname:
                if keyname == cmd.keyname:
                    cmds.append(cmd.json())
            else:
                cmds.append(cmd.json())
        if keyname:
            return _struct_response(200, "", cmds[0] if len(cmds) > 0 else None)
        return _struct_response(200, "", cmds)
    except Exception as e:
        logger.exception(e)
        return _struct_response(500, str(e))

@app.route("/command/<keyname>", methods=["DELETE"])
def delete_command(keyname):
    try:
        cmd = command.Command(keyname=keyname)
        cmd.remove()
        return _struct_response(200, "Command removed")
    except Exception as e:
        logger.exception(e)
        return _struct_response(500, str(e))
        