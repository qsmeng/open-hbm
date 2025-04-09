from flask import request, jsonify
from backend import app
from db.hbm_db import get_db_connection
import mysql.connector

@app.route('/save_game', methods=['POST'])
def save_game():
    data = request.get_json()
    user_id = data.get('user_id')
    game_uuid = data.get('game_uuid')
    score = data.get('score')
    game_type = data.get('game_type')
    story_id = data.get('story_id')
    user_story_id = data.get('user_story_id')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user_game_info (user_id, game_uuid, score, game_type, story_id, user_story_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, game_uuid, score, game_type, story_id, user_story_id)
        )
        connection.commit()
        return jsonify({'message': '游戏记录保存成功！'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 400
    finally:
        cursor.close()
        connection.close()