
DECLARE full_text CLOB;

BEGIN
full_text := '{
        "added_sound_music_info": [
            {
                "author": "conspiracyworld_2",
                "duration": 96,
                "title": "original sound - conspiracyworld_2",
                "audition_duration": 96,
                "id": 7281435097247517471
            }
        ],
        "author": [
            {
                "follower_count": 16709,
                "nickname": "conspiracyworld_2",
                "search_user_name": "conspiracyworld_2",
                "following_count": 3,
                "uid": "7276066910868816938"
            }
        ],
        "create_time": 1695341221,
        "desc": "\ud83c\udf77 Discover the world''s top 7 wines! From sweet Chateau de Kamp to elegant Dom Perignon, this video reveals the best flavors and origins. \ud83c\udf0d\ud83c\udfc6 #wine #top7 #ChateauDeKamp #OpusOne #Barolo #VegaSiciliaUnico #RomaniConti #DomPerignon #wineenthusiast",
        "desc_language": "en",
        "share_info": [
            {
                "share_url": "https://www.tiktok.com/@conspiracyworld_2/video/7281435071071014174?_r=1&u_code=e986d7707h1j3e&preview_pb=0&sharer_language=en&_d=e03j98de9ebdgh&share_item_id=7281435071071014174&source=h5_m"
            }
        ],
        "statistics": [
            {
                "collect_count": 13968,
                "comment_count": 1134,
                "digg_count": 22914,
                "download_count": 642,
                "forward_count": 0,
                "play_count": 1012962,
                "share_count": 6011,
                "whatsapp_share_count": 1610
            }
        ],
        "video": [
            {
                "duration": 96834
            }
        ],
        "text_extra": [
            {
                "hashtag_id": "22353",
                "hashtag_name": "wine"
            },
            {
                "hashtag_id": "4211847",
                "hashtag_name": "top7"
            },
            {
                "hashtag_id": "7280521308067069994",
                "hashtag_name": "chateaudekamp"
            },
            {
                "hashtag_id": "1633058793077762",
                "hashtag_name": "opusone"
            },
            {
                "hashtag_id": "21758598",
                "hashtag_name": "barolo"
            },
            {
                "hashtag_id": "7029644693331771398",
                "hashtag_name": "vegasiciliaunico"
            },
            {
                "hashtag_id": "7280521522303729710",
                "hashtag_name": "romaniconti"
            },
            {
                "hashtag_id": "8526464",
                "hashtag_name": "domperignon"
            },
            {
                "hashtag_id": "1614777671353350",
                "hashtag_name": "wineenthusiast"
            }
        ],
        "aweme_id": "7281435071071014171",
        "download_addr": [
            {
                "url": "https://v19.tiktokcdn-eu.com/6b8cc269957b74f6909b1807a863baac/652cc0b4/video/tos/maliva/tos-maliva-ve-0068c799-us/oYWMzDiDeIRugIjQYBelA28nAKVldEyvbNDElQ/?a=1233&ch=0&cr=13&dr=0&lr=all&cd=0%7C0%7C0%7C&cv=1&br=2534&bt=1267&bti=NTY6QGo0QHM0NzZANDQuYCMucCM1NTNg&cs=0&ds=3&ft=iueGqy_RZGs0PD1IHd~xg9wC3MDcBEeC~&mime_type=video_mp4&qs=0&rc=NDQ3ZTdoZzY1NzdoZDw8NEBpamV3czs6ZmZnbjMzaTczNEAtMzIwLV82XjExLV5jNWNgYSMvMi8tcjRvZTNgLS1kMTJzcw%3D%3D&l=20231015224714C7DB76922A6B05A80DB9&btag=e00090000"
            },
            {
                "url": "https://v58.tiktokcdn-eu.com/video/tos/maliva/tos-maliva-ve-0068c799-us/oYWMzDiDeIRugIjQYBelA28nAKVldEyvbNDElQ/?a=1233&ch=0&cr=13&dr=0&lr=all&cd=0%7C0%7C0%7C&cv=1&br=2534&bt=1267&bti=NTY6QGo0QHM0NzZANDQuYCMucCM1NTNg&cs=0&ds=3&ft=iueGqy_RZGs0PD1IHd~xg9wC3MDcBEeC~&mime_type=video_mp4&qs=0&rc=NDQ3ZTdoZzY1NzdoZDw8NEBpamV3czs6ZmZnbjMzaTczNEAtMzIwLV82XjExLV5jNWNgYSMvMi8tcjRvZTNgLS1kMTJzcw%3D%3D&l=20231015224714C7DB76922A6B05A80DB9&VExpiration=1697431732&VSignature=h-3ppRO9081nbZyvq4TkAA&btag=e00090000"
            },
            {
                "url": "https://api16-normal-c-useast2a.tiktokv.com/aweme/v1/play/?video_id=v15044gf0000ck6dhcrc77u80p2t5b2g&line=0&watermark=1&logo_name=tiktok_m&source=SEARCH&file_id=c1f989faae044442a39dbe043b546101&item_id=7281435071071014174&signv3=dmlkZW9faWQ7ZmlsZV9pZDtpdGVtX2lkLmNkMDc2ZjBiMTJiODhjNjAxNTQ5MDVjNmEzYWVhNTMz"
            }
        ]
    }';
    INSERT INTO aweme_dv VALUES (full_text);
END;