from sqlmodel import Session, select
from app.models import Config
from app.config.settings import CONFIG, ALPHA_VANTAGE_KEY

class ConfigService:
    @staticmethod
    def set_config(alpha_vantage_key: str, xticks_interval: int, session: Session):
        # Update or create alpha_vantage_key
        alpha_config = session.exec(
            select(Config).where(Config.key == "alpha_vantage_key")
        ).first()
        if alpha_config:
            alpha_config.value = alpha_vantage_key
        else:
            alpha_config = Config(
                key="alpha_vantage_key",
                value=alpha_vantage_key,
                description="Alpha Vantage API key for stock data"
            )
            session.add(alpha_config)

        # Update or create xticks_interval
        xticks_config = session.exec(
            select(Config).where(Config.key == "xticks_interval")
        ).first()
        if xticks_config:
            xticks_config.value = str(xticks_interval)  # Store as string
        else:
            xticks_config = Config(
                key="xticks_interval",
                value=str(xticks_interval),
                description="Interval for plot x-axis ticks (days)"
            )
            session.add(xticks_config)

        # Commit changes
        session.commit()

        # Update runtime config
        CONFIG["alpha_vantage"]["key"] = alpha_vantage_key
        CONFIG["plots"] = CONFIG.get("plots", {})
        CONFIG["plots"]["xticks_interval"] = xticks_interval

    @staticmethod
    def get_config(session: Session) -> dict:
        # Fetch all config entries
        configs = session.exec(select(Config)).all()
        config_dict = {c.key: c.value for c in configs}
        
        # Parse types as needed
        return {
            "alpha_vantage_key": config_dict.get("alpha_vantage_key", ALPHA_VANTAGE_KEY),
            "xticks_interval": int(config_dict.get("xticks_interval", "90"))  # Default to 90 if not set
        }

config_service = ConfigService()