import pika, json

def upload(file, fs, channel, access):
    try:
        file_id = fs.put(file)
    except Exception as error:
        return "internal server error", 500
    
    message = {
        "video_file_id" : str(file_id),
        "mp3_file_id" : None,
        "username" : access["email"]
    }

    try:
        channel.basic.publish(
            exchange = "",
            routing_key = "video",
            body = json.dumps(message),
            propertiese = pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except:
        fs.delete(file_id)
        return "internal server error", 500