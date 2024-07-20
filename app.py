from flask import Flask, request, jsonify
from flask_expects_json import expects_json
import boto3
import time
from boto3 import exceptions

def schedule_image_overlay(channel_id, image_s3_path, region_name='ap-south-1'):
    client = boto3.client('medialive', region_name=region_name, aws_access_key_id="access_key",
                aws_secret_access_key="secret_key")

    insert_action = {
        'ScheduleActionSettings': {
            'StaticImageActivateSettings': {
                'Image': {
                    'Uri': image_s3_path
                },
                'ImageX': 1440,
                'ImageY': 0,
                'Width': 480,
                'Height': 270,
                'Layer': 1
            }
        },
        'ScheduleActionStartSettings': {
            'ImmediateModeScheduleActionStartSettings': {}
        }
    }

    remove_action = {
        'ScheduleActionSettings': {
            'StaticImageDeactivateSettings': {
                'Layer': 1
            }
        },
        'ScheduleActionStartSettings': {
            'ImmediateModeScheduleActionStartSettings': {}
        }
    }

    client.batch_update_schedule(
        ChannelId=channel_id,
        Creates={
            'ScheduleActions': [
                {
                    'ActionName': 'InsertOverlay2654',
                    'ScheduleActionSettings': insert_action['ScheduleActionSettings'],
                    'ScheduleActionStartSettings': insert_action['ScheduleActionStartSettings']
                }
            ]
        }
    )
    print('Inserted the overlay')

    time.sleep(30)

    # Remove the overlay
    client.batch_update_schedule(
        ChannelId=channel_id,
        Creates={
            'ScheduleActions': [
                {
                    'ActionName': 'RemoveOverlay',
                    'ScheduleActionSettings': remove_action['ScheduleActionSettings'],
                    'ScheduleActionStartSettings': remove_action['ScheduleActionStartSettings']
                }
            ]
        }
    )
    print('Removed the Overlay')

app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'channel_id': {'type': 'string'},
        'image_path': {'type': 'string'},
        'region_name': {'type': 'string'}
    },
    'required': ['channel_id', 'image_path'],
    'additionalProperties': False
}

@app.route('/overlay-image', methods=['POST'])
@expects_json(schema)
def overlay():
    try:
        data = request.json
        channel_id = data['channel_id']
        image_path = data['image_path']
        region_name = data.get('region_name', 'ap-south-1')

        schedule_image_overlay(channel_id, image_path, region_name)

        return jsonify({'message': 'Overlay scheduled successfully'}), 200

    except FileNotFoundError:
        return jsonify({'error': 'Image file not found'}), 404

    except boto3.exceptions.Boto3Error as e:
        return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)