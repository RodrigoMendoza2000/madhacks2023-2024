CREATE OR REPLACE JSON RELATIONAL DUALITY VIEW race_dv AS
SELECT JSON {'raceId' IS r.race_id,
            'name'   IS r.name,
            'laps'   IS r.laps WITH NOUPDATE,
            'date'   IS r.race_date,
            'podium' IS r.podium WITH NOCHECK,
            'result' IS
                [ SELECT JSON {'driverRaceMapId' IS drm.driver_race_map_id,
                                'position'        IS drm.position,
                                UNNEST
                                (SELECT JSON {'driverId' IS d.driver_id,
                                                'name'     IS d.name}
                                    FROM driver d WITH NOINSERT UPDATE NODELETE
                                    WHERE d.driver_id = drm.driver_id)}
                    FROM driver_race_map drm WITH INSERT UPDATE DELETE
                    WHERE drm.race_id = r.race_id ]}
    FROM race r WITH INSERT UPDATE DELETE;

/

INSERT INTO race_dv VALUES ('{"raceId" : 201,
                            "name"   : "Bahrain Grand Prix",
                            "laps"   : 57,
                            "date"   : "2022-03-20T00:00:00",
                            "podium" : {}}');


CREATE OR REPLACE JSON RELATIONAL DUALITY VIEW team_dv AS
SELECT JSON {'teamId'  IS t.team_id,
            'name'    IS t.name,
            'points'  IS t.points,
            'driver'  IS
                [ SELECT JSON {'driverId' IS d.driver_id,
                                'name'     IS d.name,
                                'points'   IS d.points WITH NOCHECK}
                    FROM driver d WITH INSERT UPDATE
                    WHERE d.team_id = t.team_id ]}
    FROM team t WITH INSERT UPDATE DELETE;


INSERT INTO team_dv VALUES ('{"teamId" : 301,
                          "name"   : "Red Bull",
                          "points" : 0,
                          "driver" : [ {"driverId" : 101,
                                        "name"     : "Max Verstappen",
                                        "points"   : 0},
                                       {"driverId" : 102,
                                        "name"     : "Sergio Perez",
                                        "points"   : 0} ]}');


/

CREATE OR REPLACE JSON RELATIONAL DUALITY VIEW aweme_dv AS
SELECT JSON {'aweme_id' IS a.aweme_id,
            'create_time'   IS a.CREATE_TIME,
            'desc' IS a.DESC_VIDEO,
            'desc_language' IS a.DESC_LANGUAGE,
            'added_sound_music_info' IS 
                [SELECT JSON {
                    'author' IS mi.AUTHOR,
                    'duration' IS mi.DURATION,
                    'title' IS mi.TITLE,
                    'audition_duration' IS mi.AUDITION_DURATION,
                    'id' IS mi.ID
                }
                FROM MUSIC_INFO mi WITH INSERT UPDATE
                WHERE a.aweme_id = mi.aweme_id]
            }
    FROM AWEME a WITH INSERT UPDATE DELETE;

INSERT INTO aweme_dv VALUES ('{"aweme_id": "7287528420869754144",
                          "create_time": 1696759938,
                            "desc": "Glow Up Alert\u2728#wine #homedecor #TikTokMadeMeBuyIt #fyp ",
                            "desc_language": "en",
                          "added_sound_music_info": [{
                                "author": "Emily",
                                "duration": 13,
                                "title": "original sound - ebroomy",
                                "audition_duration": 13,
                                "id": 7119936092459043626}]
                            }');
