import re


def get_youtube_id_from_url(url: str) -> str:
    youtube_id = re.sub(r'https:\/\/w{0,3}\.?youtube\.com\/shorts\/', '', url)
    if '?' in youtube_id:
        index = youtube_id.find('?')
        return youtube_id[:index]
    return youtube_id


def get_inst_shortcode_from_url(url: str) -> str:
    inst_shortcode = url.removeprefix('https://www.instagram.com/reel/')
    if '/' in inst_shortcode:
        index = inst_shortcode.find('/')
        return inst_shortcode[:index]
    return inst_shortcode
