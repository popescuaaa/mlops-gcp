curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [
      {
        "age": 35,
        "income": 60000,
        "credit_score": 720,
        "category1": "A",
        "category2": "X"
      }
    ]
  }'
