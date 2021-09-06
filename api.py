import os
from typing import List, Optional

# from sqlalchemy.sql.schema import UniqueConstraint
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

DB_URL = os.environ["DATABASE_URL"].replace("postgres", "postgresql")

engine = create_engine(DB_URL, echo=True)


class Questions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    responses: List["Responses"] = Relationship(back_populates="question")


class Responses(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: Optional[int] = Field(default=None, foreign_key="questions.id")
    response_option: str
    correct_answer: Optional[bool]
    question: Optional[Questions] = Relationship(back_populates="responses")


def select_questions():
    with Session(engine) as session:
        session.execute("SET search_path TO games")
        #        statement = select(Questions, Responses).where(
        #            Questions.id == Responses.question_id
        #        )
        #        statement = select(Responses, Questions).join(Questions)
        statement = (
            select(Responses, Questions)
            .join(Questions)
            .where(Responses.question_id == 4)
        )
        results = session.exec(statement)
        questions = results.all()
        for i in questions:
            print(i)


#        print(questions)


def main():
    print("hello")
    select_questions()


if __name__ == "__main__":
    main()
