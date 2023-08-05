from rest_framework import serializers
from jsonschema import validate, ValidationError

from zippy_form.models import FormStep, FormField, Form
from zippy_form.utils import FIELD_TYPES, FIELD_RULES_DATE_FORMAT_ALLOWED, FIELD_RULES_TIME_FORMAT_ALLOWED, FORM_STATUS
from zippy_form.validation_rule_schema import get_text_box_field_validation_rule_schema, \
    get_textarea_field_validation_rule_schema, get_website_url_field_validation_rule_schema, \
    get_short_textarea_field_validation_rule_schema, get_number_field_validation_rule_schema, \
    get_email_field_validation_rule_schema, get_date_field_validation_rule_schema, \
    get_time_field_validation_rule_schema, get_dropdown_field_validation_rule_schema, \
    get_radio_field_validation_rule_schema, get_multiselect_checkbox_field_validation_rule_schema, \
    get_file_field_validation_rule_schema


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id', 'name']


class FormStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormStep
        fields = ['id', 'name', 'form']

    def validate_form(self, attrs):
        if attrs.status == FORM_STATUS[0][0]:
            raise serializers.ValidationError('Invalid Form ID.')

        return attrs

    def create(self, validated_data):
        step_order = 1
        last_form_step = FormStep.objects.filter(form_id=validated_data['form']).order_by('-step_order').first()
        if last_form_step:
            last_form_step_order = last_form_step.step_order
            step_order = last_form_step_order + 1

        validated_data['step_order'] = step_order
        return FormStep.objects.create(**validated_data)


class MapFieldToFormStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'field_type', 'form', 'form_step', 'field_order']


class ReOrderFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'field_order']


class UpdateFieldSettingsSerializer(serializers.ModelSerializer):
    def validate_validation_rule(self, value):
        if not value:
            raise serializers.ValidationError("Invalid Validation Rule.")

        filed_type = self.instance.field_type
        # print(filed_type)

        schema = None

        if filed_type == FIELD_TYPES[0][0]:
            schema = get_text_box_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[1][0]:
            schema = get_website_url_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[2][0]:
            schema = get_textarea_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[3][0]:
            schema = get_number_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[4][0]:
            schema = get_email_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[5][0]:
            schema = get_dropdown_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[6][0]:
            schema = get_radio_field_validation_rule_schema()
        # elif filed_type == FIELD_TYPES[7][0]:
        #     schema = get_radio_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[8][0]:
            schema = get_date_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[9][0]:
            schema = get_time_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[10][0]:
            schema = get_file_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[11][0]:
            schema = get_short_textarea_field_validation_rule_schema()
        elif filed_type == FIELD_TYPES[12][0]:
            schema = get_multiselect_checkbox_field_validation_rule_schema()

        if schema:
            try:
                validate(value, schema)
            except ValidationError as e:
                # print("Schema Error: ", e)
                raise serializers.ValidationError("Invalid Validation Rule..")

            if filed_type == FIELD_TYPES[8][0]:
                # additional validation for date field
                if value['date']:
                    date_format = value['date_format']
                    field_rules_date_format_allowed = FIELD_RULES_DATE_FORMAT_ALLOWED.keys()
                    if date_format not in field_rules_date_format_allowed:
                        allowed_date_format = ", "
                        allowed_date_format = allowed_date_format.join(field_rules_date_format_allowed)
                        msg = f"Only {allowed_date_format} allowed for date format"
                        raise serializers.ValidationError(msg)
            elif filed_type == FIELD_TYPES[9][0]:
                # additional validation for time field
                if value['time']:
                    time_format = value['time_format']
                    field_rules_time_format_allowed = FIELD_RULES_TIME_FORMAT_ALLOWED.keys()
                    if time_format not in field_rules_time_format_allowed:
                        allowed_time_format = ", "
                        allowed_time_format = allowed_time_format.join(field_rules_time_format_allowed)
                        msg = f"Only {allowed_time_format} hrs allowed for time format"
                        raise serializers.ValidationError(msg)

        return value

    def validate_options(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "value": {"type": "string"},
                    "label": {"type": "string"},
                    "order": {"type": "integer", "minimum": 0}
                },
                "required": ["value", "label", "order"],
                "additionalProperties": False
            }
        }

        try:
            validate(value, schema)
        except ValidationError as e:
            # print("Schema Error: ", e)
            raise serializers.ValidationError("Invalid Format.")

        return value

    def validate(self, attrs):
        options_field = attrs.get('options', None)
        is_unique_field = attrs.get('is_unique', False)

        errors = {}

        field_type = self.instance.field_type

        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            if options_field is None:
                errors["options"] = ["This field is required."]
        else:
            if options_field is not None:
                errors["options"] = ["Options not allowed for this field type."]

        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[10][0] or field_type == FIELD_TYPES[12][0]:
            if is_unique_field:
                errors["is_unique"] = ["Unique Validation not allowed for this field type."]

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    options = serializers.JSONField(required=False)

    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_size', 'placeholder', 'custom_class_name', 'validation_rule', 'is_mandatory',
                  'is_unique', 'options']
        extra_kwargs = {
            "label": {"required": True},
            "field_size": {"required": True},
            "placeholder": {"required": True, "allow_blank": True},
            "custom_class_name": {"required": True},
            "validation_rule": {"required": True},
            "is_mandatory": {"required": True},
            "is_unique": {"required": True},
        }
