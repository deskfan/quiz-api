import os
from typing import Optional

from sqlalchemy.sql.schema import UniqueConstraint
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Questions(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str


class Responses(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: Optional[int] = Field(default=None, foreign_key="questions.id")
    response_option: str
    correct_answer: Optional[bool]


DB_URL = os.environ["DATABASE_URL"].replace("postgres", "postgresql")

engine = create_engine(DB_URL, echo=True)


def create_questions():
    q_1 = Questions(question="What is the capital of France?")
    q_3 = Questions(question="Which is the fastest animal?")

    with Session(engine) as session:
        session.execute("SET search_path TO games")
        session.add(q_1)
        session.add(q_3)

        print("after adding questions to session")
        print("Question 1:", q_1.id)
        print("Question 3:", q_3.question)

        session.commit()

        print("after committing questions")
        print("Question 1:", q_1.id)
        print("Question 3:", q_3.question)

        session.refresh(q_1)
        session.refresh(q_3)
        print("after refreshing questions")

        print("Question 1:", q_1.id)
        print("Question 3:", q_3.question)


def create_responses():
    r_1_1 = Responses(question_id=1, response_option="Halifax", correct_answer=False)
    r_1_2 = Responses(question_id=1, response_option="Tokyo", correct_answer=False)
    r_1_3 = Responses(question_id=1, response_option="London", correct_answer=False)
    r_1_4 = Responses(question_id=1, response_option="Paris", correct_answer=True)

    r_2_1 = Responses(question_id=2, response_option="Earth", correct_answer=False)
    r_2_2 = Responses(question_id=2, response_option="Mars", correct_answer=False)
    r_2_3 = Responses(question_id=2, response_option="Mercury", correct_answer=True)
    r_2_4 = Responses(question_id=2, response_option="Venus", correct_answer=False)

    with Session(engine) as session:
        session.execute("SET search_path TO games")
        session.add(r_1_1)
        session.add(r_1_2)
        session.add(r_1_3)
        session.add(r_1_4)
        session.add(r_2_1)
        session.add(r_2_2)
        session.add(r_2_3)
        session.add(r_2_4)

        session.commit()


def select_questions():
    with Session(engine) as session:
        session.execute("SET search_path TO games")
        statement = select(Questions)
        results = session.exec(statement)
        questions = results.all()
        print(questions)


def select_responses():
    with Session(engine) as session:
        session.execute("SET search_path TO games")
        statement = select(Responses)
        results = session.exec(statement)
        responses = results.all()
        print(responses)


def create_question_pack(q, r_list):
    with Session(engine) as session:
        session.execute("SET search_path TO games")
        que = Questions(question=q)
        session.add(que)
        session.commit()
        for r in r_list:
            response = r["response"]
            correct = r["correct"]
            q_id = que.id
            response_obj = Responses(
                question_id=q_id, response_option=response, correct_answer=correct
            )
            session.add(response_obj)
        session.commit()


def main():
    q = "how old is mummy?"
    r = [
        {"response": "mummy is 39", "correct": False},
        {"response": "mummy is 42", "correct": False},
        {"response": "mummy is 41", "correct": False},
        {"response": "mummy is 40", "correct": True},
    ]
    create_question_pack(q, r)
    select_questions()
    select_responses()


if __name__ == "__main__":
    main()
