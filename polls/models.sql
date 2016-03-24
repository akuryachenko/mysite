
CREATE TABLE "polls_cuserchoice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cuser_id" integer NOT NULL REFERENCES "cuser_cuser" ("id"), "date_vote" date NOT NULL, "choice_id" integer NOT NULL REFERENCES "polls_choice" ("id"));
INSERT INTO "polls_cuserchoice" ("date_vote", "choice_id", "id", "cuser_id") SELECT "date_vote", "choice_id", "id", "cuser_id" FROM "polls_cuserchoice__old";

CREATE INDEX "polls_cuserchoice_1d0c3e03" ON "polls_cuserchoice" ("cuser_id");
CREATE INDEX "polls_cuserchoice_428bb064" ON "polls_cuserchoice" ("choice_id");


CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_img" varchar(100) NOT NULL, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
INSERT INTO "polls_question" ("question_img", "question_text", "pub_date", "id") SELECT '2016-03-23 06:54:56.552969+00:00', "question_text", "pub_date", "id" FROM "polls_question__old";
DROP TABLE "polls_question__old";
