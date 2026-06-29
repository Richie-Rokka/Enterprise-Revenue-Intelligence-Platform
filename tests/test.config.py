from src.config.config import config

print(config.database.host)
print(config.database.database)
print(config.pipeline.version)
print(config.quality.minimum_quality_score)