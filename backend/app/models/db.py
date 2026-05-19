from datetime import datetime
from sqlalchemy import String, Float, Text, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


class TravelGoal(Base):
    __tablename__ = "travel_goals"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_wallet: Mapped[str] = mapped_column(String, index=True)
    destination: Mapped[str] = mapped_column(String)
    origin: Mapped[str] = mapped_column(String)
    travel_date: Mapped[str] = mapped_column(String)
    budget_usd: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String, default="pending")
    final_report_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    solana_goal_pda: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sponsorships: Mapped[list["Sponsorship"]] = relationship(back_populates="goal")
    agent_logs: Mapped[list["AgentLog"]] = relationship(back_populates="goal")
    price_history: Mapped[list["PriceHistory"]] = relationship(back_populates="goal")


class Sponsorship(Base):
    __tablename__ = "sponsorships"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    goal_id: Mapped[str] = mapped_column(ForeignKey("travel_goals.id"))
    sponsor_wallet: Mapped[str] = mapped_column(String)
    amount_sol: Mapped[float] = mapped_column(Float)
    tx_signature: Mapped[str | None] = mapped_column(String, nullable=True)
    refunded: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    goal: Mapped["TravelGoal"] = relationship(back_populates="sponsorships")


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    goal_id: Mapped[str] = mapped_column(ForeignKey("travel_goals.id"))
    agent_name: Mapped[str] = mapped_column(String)
    input_json: Mapped[str] = mapped_column(Text)
    output_json: Mapped[str] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    goal: Mapped["TravelGoal"] = relationship(back_populates="agent_logs")


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    origin: Mapped[str] = mapped_column(String)
    destination: Mapped[str] = mapped_column(String)
    description_md: Mapped[str] = mapped_column(Text)
    tags: Mapped[str] = mapped_column(String)
    copy_count: Mapped[int] = mapped_column(Integer, default=0)
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=True)
    creator_wallet: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    goal_id: Mapped[str] = mapped_column(ForeignKey("travel_goals.id"))
    flight_price_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    hotel_price_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_buy_signal: Mapped[bool] = mapped_column(Boolean, default=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    goal: Mapped["TravelGoal"] = relationship(back_populates="price_history")


class User(Base):
    __tablename__ = "users"

    wallet_address: Mapped[str] = mapped_column(String, primary_key=True)
    display_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    total_sponsored_sol: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    wallet_address: Mapped[str] = mapped_column(String, index=True)
    event_type: Mapped[str] = mapped_column(String)
    meta_data: Mapped[dict] = mapped_column("sub_metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

