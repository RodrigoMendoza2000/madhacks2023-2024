  CREATE TABLE "VIDEO" 
   (	"AWEME_ID" VARCHAR2(4000 CHAR), 
	"DURATION" NUMBER, 
	"IDENTITY_ID" NUMBER GENERATED BY DEFAULT ON NULL AS IDENTITY MINVALUE 1 MAXVALUE 9999999999999999999999999999 INCREMENT BY 1 START WITH 1 CACHE 20 NOORDER  NOCYCLE  NOKEEP  NOSCALE  NOT NULL ENABLE, 
	 CONSTRAINT "VIDEO_PK" PRIMARY KEY ("IDENTITY_ID")
  USING INDEX  ENABLE
   ) ;

  ALTER TABLE "VIDEO" ADD CONSTRAINT "VIDEO_FK" FOREIGN KEY ("AWEME_ID")
	  REFERENCES "AWEME" ("AWEME_ID") ENABLE;