import logging
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_MODEL_PATH = "model_path"
CONF_SENSOR = "sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_MODEL_PATH): cv.string,
    vol.Required(CONF_SENSOR): cv.entity_id,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    name = config[CONF_NAME]
    model_path = config[CONF_MODEL_PATH]
    sensor = config[CONF_SENSOR]

    add_entities([EnergyIdentificationSensor(hass, name, model_path, sensor)], True)

class EnergyIdentificationSensor(Entity):
    def __init__(self, hass, name, model_path, sensor):
        self._hass = hass
        self._name = name
        self._model_path = model_path
        self._sensor = sensor
        self._state = None
        self._model = pd.read_pickle(model_path)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        usage_data = float(self._hass.states.get(self._sensor).state)
        prediction = self._model.predict([[usage_data]])
        self._state = prediction[0]
        _LOGGER.info(f"Identified appliance: {self._state}")