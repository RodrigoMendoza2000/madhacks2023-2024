CREATE OR REPLACE JSON RELATIONAL DUALITY VIEW aweme_dv AS
SELECT JSON {'aweme_id' IS a.aweme_id,
            'create_time'   IS a.CREATE_TIME,           
            'desc' IS a.DESC_VIDEO,
            'desc_language' IS a.DESC_LANGUAGE,
            'added_sound_music_info' IS
                [
                    SELECT JSON {
                        'author' IS mi.AUTHOR,
                        'duration' IS mi.DURATION,
                        'title' IS mi.TITLE,
                        'audition_duration' IS mi.AUDITION_DURATION,
                        'id' IS mi.ID,
                        'identity_id' IS mi.IDENTITY_ID
                    }
                    FROM MUSIC_INFO mi WITH INSERT UPDATE
                    WHERE a.aweme_id = mi.aweme_id
                ],
            'author' IS
                [
                    SELECT JSON {
                        'follower_count' IS au.FOLLOWER_COUNT,
                        'nickname' IS au.NICKNAME,
                        'search_user_name' IS au.SEARCH_USERNAME,
                        'following_count' IS au.FOLLOWING_COUNT,
                        'uid' IS au.ID,
                        'identity_id' IS au.IDENTITY_ID
                    }
                    FROM AUTHOR au WITH INSERT UPDATE
                    WHERE a.aweme_id = au.aweme_id
                ],
            'share_info' IS
                [
                    SELECT JSON {
                        'share_url' IS si.SHARE_URL
                    }
                    FROM SHARE_INFO si WITH INSERT UPDATE
                    WHERE a.aweme_id = si.aweme_id
                ],
            'statistics' IS
                [
                    SELECT JSON {
                        'collect_count' IS st.collect_count,
                        'comment_count' IS st.comment_count,
                        'digg_count' IS st.digg_count,
                        'download_count' IS st.download_count,
                        'forward_count' IS st.forward_count,
                        'play_count' IS st.play_count,
                        'share_count' IS st.share_count,
                        'whatsapp_share_count' IS st.whatsapp_share_count,
                        'IDENTITY_ID' IS st.IDENTITY_ID
                    }
                    FROM STATISTICS st WITH INSERT UPDATE
                    WHERE a.aweme_id = st.aweme_id
                ],
            'video' IS
                [
                    SELECT JSON {
                        'duration' IS v.duration,
                        'identity_id' IS v.identity_id
                    }
                    FROM video v WITH INSERT UPDATE
                    WHERE a.aweme_id = v.aweme_id
                ],
            'download_addr' IS
                [
                    SELECT JSON {
                        'url' IS vu.url,
                        'identity_id' IS vu.identity_id
                    }
                    FROM video_url vu WITH INSERT UPDATE
                    WHERE a.aweme_id = vu.aweme_id
                ],
            'text_extra' IS
                [
                    SELECT JSON {
                        'hashtag_id' IS h.hashtag_id,
                        'hashtag_name' IS h.hashtag_name,
                        'identity_id' IS h.identity_id
                    }
                    FROM HASHTAGS h WITH INSERT UPDATE
                    WHERE a.aweme_id = h.aweme_id
                ]
            }
    FROM AWEME a WITH INSERT UPDATE DELETE;