from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseUserDtoSchema(Schema):
    first_name = fields.Str(required=True, allow_none=False)
    last_name = fields.Str(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)


class ResponseUserDto(ResponseDto, ResponseUserDtoSchema):
    __schema__ = ResponseUserDtoSchema
