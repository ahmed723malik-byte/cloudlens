import os
from app import create_app
from app.config import DevelopmentConfig, ProductionConfig

config = ProductionConfig if os.environ.get("FLASK_ENV") == "production" else DevelopmentConfig
app = create_app(config)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
