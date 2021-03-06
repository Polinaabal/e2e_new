
import joblib
import numpy

MODEL_PATH = 'model.pkl'
MODEL2_PATH = 'model2.pkl'
SCALER_X_PATH = 'scaler_x.pkl'
SCALER_Y_PATH = 'scaler_y.pkl'

from flask import Flask, request
app = Flask(__name__)
model = joblib.load(MODEL_PATH)
model2 = joblib.load(MODEL2_PATH)
sc_x = joblib.load(SCALER_X_PATH)
sc_y = joblib.load(SCALER_Y_PATH)
model_version = 0
result = 0
@app.route("/predict_price", methods = ['GET'])
def predict():
    args = request.args
    floor = args.get('floor', default=-1, type = int)
    rooms = args.get('rooms',default=-1, type = int)
    area = args.get('area', default=-1, type = float)
    house_price_sqm_median = args.get('house_price_sqm_median',  default=-1, type = float)
    model_version = args.get('model_version', default = -1,type = int)
    #response = "floor:{}, rooms:{}, area:{}, house_price_sqm_median:{}".format(floor,rooms,area,house_price_sqm_median)

    required_params = [floor, rooms, area,house_price_sqm_median]
    if model_version == 1:
        if any([param == -1 for param in required_params]):
            return "500 INTERNAL SERVER ERROR"
        x = numpy.array([floor, rooms, area, house_price_sqm_median]).reshape(1, -1)
        x = sc_x.transform(x)
        result = model.predict(x)
        result = sc_y.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])
    elif model_version == 2:
        if any([param == -1 for param in required_params]):
            return "500 INTERNAL SERVER ERROR"
        x = numpy.array([floor, rooms, area, house_price_sqm_median]).reshape(1, -1)
        x = sc_x.transform(x)
        result = model2.predict(x)
        result = sc_y.inverse_transform(result.reshape(1, -1))

        return str(result[0][0])

    else:
        return ("500 INTERNAL SERVER ERROR")


if __name__ == '__main__':
    app.run(debug=True, port=5444,host='0.0.0.0')