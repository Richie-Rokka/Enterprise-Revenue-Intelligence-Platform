from src.database.database_executor import DatabaseExecutor

executor = DatabaseExecutor()

result = executor.execute_sql(

    "SELECT 1;",

    "Connectivity Test",

)

print(result)