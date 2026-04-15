## Gender Prediction API

This API predicts user's gender based on the name input passed to genderize api running as a background prediction engine.

### Available endpoint
GET - `/api/classify/?name={name}` \
*replace {name} with actual name*

On successful processing, the api returns predicted gender, sample size, confidence state, as well as probability.



