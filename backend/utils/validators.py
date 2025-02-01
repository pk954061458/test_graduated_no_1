from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class SpotSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    location = fields.Str(required=True)
    latitude = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=True, validate=validate.Range(min=-180, max=180))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    rating = fields.Float(validate=validate.Range(min=0, max=5))

    @validates_schema
    def validate_spot(self, data, **kwargs):
        validate_coordinates(data)

# 在API中使用
spot_schema = SpotSchema()

def validate_coordinates(data):
    if data.get('latitude') and data.get('longitude'):
        # 检查坐标是否在中国范围内
        if not (3.86 <= data['latitude'] <= 53.55 and 
                73.66 <= data['longitude'] <= 135.05):
            raise ValidationError('坐标必须在中国范围内') 