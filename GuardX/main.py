from flask import request, render_template, jsonify
from config import app, db
from models import Test
from aiwaf import AIWAF
import json

aiwaf = AIWAF()

@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/results", methods=["GET"])
def get_results():
    results = Test.query.all()
    json_results = list(map(lambda x: x.to_json(), results))
    with open('data.json', 'w') as file:
        json.dump(json_results, file, indent=4)
    return jsonify({"results": json_results}), 200

# thinking request to be as {"testType": "XSS", "payload": "Here."}

@app.route("/test_payload", methods=["POST"])
def payload_test():
    test_type = request.json.get("testType")
    payload = request.json.get("payload")

    if not test_type or not payload:
        return jsonify({"message": "You must include the content in the request"}), 400
    
    # Perform the test here and get the result.
    try:
        # Load the model and label encoder and produce result of each model
        aiwaf.load_model('logistic_regression_model.pkl', 'logistic_regression_label_encoder.pkl')
        logistic_regression_result = aiwaf.detect_payload(payload)

        aiwaf.load_model('random_forest_model_imbalanced.pkl', 'random_forest_label_encoder_imbalanced.pkl')
        random_forest_imbalance_result = aiwaf.detect_payload(payload)

        aiwaf.load_model('random_forest_model_balanced.pkl', 'random_forest_label_encoder_balanced.pkl')
        random_forest_balance_result = aiwaf.detect_payload(payload)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    new_test = Test(
        test_type=test_type, 
        payload=payload, 
        logistic_result=logistic_regression_result, 
        imbalance_result=random_forest_imbalance_result, 
        balance_result=random_forest_balance_result
    )
    try:
        db.session.add(new_test)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Test has been done!"}), 201

# We don't have the update function but we do have delete

@app.route("/delete_result/<int:user_id>", methods=["DELETE"])
def delete_test(user_id):
    test_result = Test.query.get(user_id)  # this code will say it is old but to make changes in it the whole structure need to be changed.

    if not test_result:
        return jsonify({"message": "Payload not found!"}), 404
    
    db.session.delete(test_result)
    db.session.commit()

    return jsonify({"message": "Payload Detected!"}), 200

@app.route("/generate_report", methods=["GET"])
def report_generating():
    try:
        from report_generator import gen_rep
        gen_rep()
        return jsonify({"message": "Successful in creation of Report"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

# Coded by Rohan Thapa