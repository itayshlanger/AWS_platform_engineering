from flask import Flask, request, jsonify
from ec2_managment import *
from S3_managment import *
from Route53_managment import *
from Itay_project import ec2, s3, route53

app = Flask(__name__)

@app.route('/project', methods=['POST'])

def project():
    data = request.get_json()
    if 'ec2' == data.get('resource'):
        if 'manage' in request.args:
            if 'start' in request.args:
                result = handle_ec2(data.get('action'), instance_type=data.get('type'), ami=data.get('AMI'),
                                  resource=ec2,instance_id=data.get('start'), arg='start')
                return result
            elif 'stop' in request.args:
                result = handle_ec2(data.get('action'), instance_type=data.get('type'), ami=data.get('AMI'),
                                  resource=ec2,instance_id=data.get('stop'), arg='stop')
                return result
        else:
            result = handle_ec2(data.get('action'),instance_type=data.get('type'),ami=data.get('AMI'), resource=ec2)
            return result
    elif 's3' == data.get('resource'):
        result = handle_s3(data.get('action'),public=data.get('public'),name=data.get('name'),file=data.get('file'),resource=s3)
        return result
    elif 'route53' == data.get('resource'):
        if data.get('action') == 'record':
            if ('create' and 'delete') or ('delete' and 'update') or ('update' and 'create') in request.args:
                return "Error: only one from create/delete/update can be stated for managing records!"
            else:
                result = handle_route53(data.get('action'), name=data.get('name'), public=data.get('public'), resource=route53,
                               delete=data.get('delete'), update=data.get('update'), create=data.get('create'),
                               values=data.get('values'), ttl=data.get('ttl'), rtype=data.get('rtype'))
                return result
        else:
            result = handle_route53(data.get('action'),name=data.get('name'),public=data.get('public'),resource=route53,
                       delete=data.get('delete'),update=data.get('update'),create=data.get('create'),
                       values=data.get('values'),ttl=data.get('ttl'),rtype=data.get('rtype'))
            return result
    elif not data:
        return jsonify({"error": "No data provided"}), 400


if __name__ == '__main__':
    app.run(port=2310, host="127.0.0.1", debug=True)

