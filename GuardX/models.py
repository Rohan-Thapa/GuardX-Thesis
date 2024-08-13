from config import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_type = db.Column(db.String(15), unique=False, nullable=False)
    payload = db.Column(db.String(120), unique=False, nullable=False)
    logistic_result = db.Column(db.String(15), unique=False, nullable=False)
    imbalance_result = db.Column(db.String(15), unique=False, nullable=False)
    balance_result = db.Column(db.String(15), unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "testType": self.test_type,
            "payload": self.payload,
            "logistic": self.logistic_result,
            "imbalance": self.imbalance_result,
            "balance": self.balance_result
        }
