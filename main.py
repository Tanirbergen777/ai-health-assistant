from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import ai_logic
from database import engine, get_db

# Создаем таблицы в БД
models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # Вот эта строчка обязательна!


@app.get("/")
def home():
    return {"message": "AI Assistant Backend is Running"}


@app.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user_exists = db.query(models.User).filter(models.User.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Этот email уже занят")

    new_user = models.User(username=username, email=email, password_hash=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "user_id": new_user.id}


@app.post("/onboarding/{user_id}")
def create_profile(
        user_id: int,
        age: int,
        weight: float,
        height: float,
        activity_level: int,
        goal: str,
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    height_in_meters = height / 100
    bmi_value = round(weight / (height_in_meters ** 2), 2)

    ai_verdict = ai_logic.predict_difficulty(age, bmi_value, activity_level)

    new_profile = models.UserProfile(
        user_id=user_id,
        age=age,
        weight=weight,
        height=height,
        activity_level=activity_level,
        goal=goal,
        bmi=bmi_value
    )

    db.add(new_profile)
    db.commit()
    return {"status": "profile_created", "bmi": bmi_value,
        "ai_recommendation": ai_verdict,
        "message": f"AI подобрал вам уровень: {ai_verdict}"}