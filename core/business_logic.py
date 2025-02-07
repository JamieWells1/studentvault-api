def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, proxies={"https": proxy, "http": proxy}
        )
        captions = " ".join([item["text"] for item in transcript])

        return jsonify(captions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
