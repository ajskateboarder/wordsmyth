from youtube_comment_downloader.downloader import YoutubeCommentDownloader


def get_comments(video_id, limit):
    comment = YoutubeCommentDownloader()
    gen = comment.get_comments(video_id)
    count = 1

    for comment in gen:
        yield comment["text"]
        count += 1

        if count == limit:
            break
