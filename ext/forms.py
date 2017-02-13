from googleapiclient import http
from grow.preprocessors import google_drive
from protorpc import messages
from protorpc import protojson
import grow
import io
import json
import urllib
import os
import bs4
import requests


class FieldType(messages.Enum):
    TEXT = 1
    TEXTAREA = 2
    CHECKBOX = 3
    RADIO = 4
    SCALE = 5


class Field(messages.Message):
    placeholder = messages.StringField(3)
    field_type = messages.EnumField(FieldType, 4)
    name = messages.StringField(5)
    value = messages.StringField(6)


class Item(messages.Message):
    label = messages.StringField(1)
    description = messages.StringField(2)
    fields = messages.MessageField(Field, 3, repeated=True)
    required = messages.BooleanField(4)


class Form(messages.Message):
    title = messages.StringField(1)
    description = messages.StringField(2)
    items = messages.MessageField(Item, 3, repeated=True)
    action = messages.StringField(4)


class GoogleFormsPreprocessor(google_drive.BaseGooglePreprocessor):
    KIND = 'google_forms'
    VIEW_URL = 'https://docs.google.com/forms/d/e/{}/viewform'
    ACTION_URL = 'https://docs.google.com/forms/d/e/{}/formResponse'

    class Config(messages.Message):
        id = messages.StringField(1)
        path = messages.StringField(2)

    def run(self, *args, **kwargs):
        url = GoogleFormsPreprocessor.VIEW_URL.format(self.config.id)
        resp = requests.get(url)
        assert resp.status_code == 200
        html = resp.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        soup_content = soup.find('div', {'class': 'freebirdFormviewerViewFormContent'})
        form_msg = self.parse_form(soup_content)
        msg_string_content = protojson.encode_message(form_msg)
        json_dict = json.loads(msg_string_content)
        self.pod.write_yaml(self.config.path, json_dict)
        self.pod.logger.info('Saved -> {}'.format(self.config.path))

    def get_text(self, soup, class_name):
        el = soup.find('div', {'class': class_name})
        return el.text if el else None

    def get_placeholder(self, soup):
        el = soup.find('div', {'class': 'quantumWizTextinputPaperinputPlaceholder'})
        return el.text if el else None

    def get_description(self, soup):
        el = soup.find('div', {'class': 'freebirdFormviewerViewItemsItemItemHelpText'})
        return el.text if el else None

    def get_choice_value(self, soup):
        el = soup.find('div', {'class': 'docssharedWizToggleLabeledPrimaryText'})
        return el.text if el else None

    def parse_form(self, soup):
        msg = Form()
        msg.title = self.get_text(soup, 'freebirdFormviewerViewHeaderTitle')
        msg.description = self.get_text(soup, 'freebirdFormviewerViewHeaderDescription')
        msg.action = GoogleFormsPreprocessor.ACTION_URL.format(self.config.id)
        msg.items = []
        items = soup.findAll('div', {'class': 'freebirdFormviewerViewItemsItemItem'})
        for item in items:
            item_msg = Item()
            item_msg.label = self.get_text(item, 'freebirdFormviewerViewItemsItemItemTitle')
            item_msg.description = self.get_description(item)
            item_msg.required = bool(item.find('span', {'class': 'freebirdFormviewerViewItemsItemRequiredAsterisk'}))
            item_msg.fields = []
            checkboxes = item.findAll('div', {'class': 'freebirdFormviewerViewItemsCheckboxChoice'})
            for checkbox in checkboxes:
                field_msg = Field()
                field_msg.field_type = FieldType.CHECKBOX
                field_msg.name = checkbox.parent.find('input').get('name')
                value = self.get_choice_value(checkbox)
                field_msg.value = value
                item_msg.fields.append(field_msg)
            scales = item.findAll('div', {'class': 'freebirdMaterialScalecontentLabel'})
            for scale in scales:
                field_msg = Field()
                field_msg.field_type = FieldType.SCALE
                field_msg.name = scale.parent.parent.parent.parent.parent.parent.find('input').get('name')
                value = scale.text
                field_msg.value = value
                item_msg.fields.append(field_msg)
            radios = item.findAll('label', {'class': 'freebirdFormviewerViewItemsRadioChoice'})
            for radio in radios:
                field_msg = Field()
                field_msg.field_type = FieldType.RADIO
                field_msg.name = radio.parent.parent.parent.parent.find('input').get('name')
                value = self.get_choice_value(radio)
                field_msg.value = value
                item_msg.fields.append(field_msg)
            textareas = item.findAll('div', {'class': 'freebirdFormviewerViewItemsTextLongText'})
            for text in textareas:
                field_msg = Field()
                field_msg.field_type = FieldType.TEXTAREA
                field_msg.placeholder = self.get_placeholder(text)
                field_msg.name = text.find('textarea').get('name')
                item_msg.fields.append(field_msg)
            texts = item.findAll('div', {'class': 'freebirdFormviewerViewItemsTextItemWrapper'})
            for text in texts:
                field_msg = Field()
                field_msg.field_type = FieldType.TEXT
                field_msg.placeholder = self.get_placeholder(text)
                field_msg.name = text.find('input').get('name')
                item_msg.fields.append(field_msg)
            msg.items.append(item_msg)
        return msg
