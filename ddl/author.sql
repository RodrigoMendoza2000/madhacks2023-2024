  CREATE TABLE "AUTHOR" 
   (	"FOLLOWER_COUNT" NUMBER, 
	"NICKNAME" VARCHAR2(4000 CHAR), 
	"SEARCH_USERNAME" VARCHAR2(4000 CHAR), 
	"FOLLOWING_COUNT" NUMBER, 
	"ID" NUMBER, 
	"AWEME_ID" VARCHAR2(4000 CHAR), 
	"IDENTITY_ID" NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  NOT NULL ENABLE, 
	 CONSTRAINT "AUTHOR_PK" PRIMARY KEY ("IDENTITY_ID")
  USING INDEX  ENABLE
   ) ;

  ALTER TABLE "AUTHOR" ADD CONSTRAINT "AUTHOR_FK" FOREIGN KEY ("AWEME_ID")
	  REFERENCES "AWEME" ("AWEME_ID") ENABLE;