import json
import command

from flask import Flask, request, Response

app = Flask(__name__)

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
        
        icon = json_body['icon'] if 'icon' in json_body else False
        multiple = json_body['multiple'] if 'multiple' in json_body else False
        item_separator = json_body['item_separator'] if 'item_separator' in json_body else " "

        cmd = command.Command(
            command=json_body['command'], 
            mui_verb=json_body['mui_verb'], 
            icon=icon, item_separator=item_separator,
            multiple=multiple)

        app.logger.info(f"Adding command {cmd}")
        cmd.save()
        return _struct_response(200, "Command added", cmd.json())
    except Exception as e:
        app.logger.exception(e)
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
        app.logger.exception(e)
        return _struct_response(500, str(e))

@app.route("/command/<keyname>", methods=["DELETE"])
def delete_command(keyname):
    try:
        cmd = command.Command(keyname=keyname)
        cmd.remove()
        return _struct_response(200, "Command removed")
    except Exception as e:
        app.logger.exception(e)
        return _struct_response(500, str(e))
        